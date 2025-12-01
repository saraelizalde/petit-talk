from django.shortcuts import redirect, render, get_object_or_404
import stripe
from django.contrib import messages
from django.conf import settings
from offers.models import Offer
from order.models import Order
from bookings.models import Booking
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


def validate_booking_availability(order, request):
    """
    Re-check all bookings in an order to ensure they are still valid.

    This includes:
        - Ensuring bookings comply with the 48-hour advance rule.
        - Checking that the teacher still exists and is available.
        - Checking for booking conflicts with the teacher’s schedule.

    If a booking fails any check, it is deleted and an error message is
    added to the request.

    Args:
        order (Order): The order containing bookings to validate.
        request (HttpRequest): The HTTP request object, used to add messages.

    Returns:
        bool: True if all bookings are valid, False if any booking is invalid.
    """
    now = timezone.now()

    for booking in order.bookings.all():
        teacher = booking.teacher
        scheduled_time = booking.scheduled_time

        # 48-hour rule re-check
        if scheduled_time < now + timedelta(hours=48):
            messages.error(
                request,
                (
                    f"Your lesson with {teacher.username} at "
                    f"{scheduled_time.strftime('%Y-%m-%d %H:%M')} "
                    "is now too close. Bookings must be 48h in advance."
                ),
            )
            booking.delete()
            return False

        # Check if teacher still exists and is teacher
        if (
            not hasattr(teacher, "profile")
            or not teacher.profile.is_teacher
        ):
            messages.error(
                request,
                f"{teacher.username} is no longer available.",
            )
            booking.delete()
            return False

        # Check if another booking now conflicts
        conflict = Booking.objects.filter(
            teacher=teacher,
            scheduled_time=scheduled_time
        ).exclude(id=booking.id).exclude(status__in=["CANCELLED", "COMPLETED"])

        if conflict.exists():
            messages.error(
                request,
                (
                    f"Your booking with {teacher.username} at "
                    f"{scheduled_time.strftime('%Y-%m-%d %H:%M')} "
                    "is no longer available."
                ),
            )
            booking.delete()
            return False

    return True


def create_checkout_session(request, order_id):
    """
    Create a Stripe PaymentIntent for a given order and redirect
    to the payment page.

    Steps:
        1. Validate booking availability.
        2. Ensure the order has unpaid bookings.
        3. Apply any active offer.
        4. Create a Stripe PaymentIntent.
        5. Save PaymentIntent ID in the order.
        6. Redirect to the payment page.

    Args:
        request (HttpRequest): The HTTP request object.
        order_id (int): ID of the order to process payment for.

    Returns:
        HttpResponseRedirect: Redirects to the payment page or
        view_bag on error.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order = get_object_or_404(Order, id=order_id, student=request.user)

    if not validate_booking_availability(order, request):
        return redirect("view_bag")

    pending_bookings = order.bookings.filter(status__in=["UNPAID", "PENDING"])
    if not pending_bookings.exists():
        messages.error(request, "There are no unpaid bookings in this order.")
        return redirect("view_bag")

    active_offer = Offer.objects.filter(active=True).first()
    order.offer = active_offer if active_offer else None
    order.refresh_total()

    if order.total_eur <= 0:
        messages.error(request, "Checkout failed — invalid order total.")
        return redirect("view_bag")

    # Create PaymentIntent (no Checkout Session!)
    intent = stripe.PaymentIntent.create(
        amount=int(order.total_eur * 100),
        currency="eur",
        metadata={
            "order_id": order.id,
            "offer_id": order.offer.id if order.offer else None,
        },
        receipt_email=request.user.email,
    )

    order.stripe_payment_intent = intent.id
    order.save(update_fields=[
        "stripe_payment_intent",
        "offer",
        "total_eur",
        "subtotal"
        ]
    )

    return redirect("payment_page", order_id=order.id)


def payment_page(request, order_id):
    """
    Render a custom Stripe payment page using PaymentIntent
    and Stripe Elements.

    Steps:
        1. Validate booking availability.
        2. Refresh order totals and active offer.
        3. Create or retrieve Stripe PaymentIntent.
        4. Render the payment page template with client_secret.

    Args:
        request (HttpRequest): The HTTP request object.
        order_id (int): ID of the order to pay.

    Returns:
        HttpResponse: Renders the Stripe payment page or redirects on error.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    order = get_object_or_404(Order, id=order_id, student=request.user)

    if not validate_booking_availability(order, request):
        return redirect("view_bag")

    # Refresh offer & total
    active_offer = Offer.objects.filter(active=True).first()
    order.offer = active_offer if active_offer else None
    order.refresh_total()

    if order.total_eur <= 0:
        messages.error(request, "Checkout failed — invalid order total.")
        return redirect("view_bag")

    # Create or reuse PaymentIntent
    if not order.stripe_payment_intent:
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_eur * 100),
            currency="eur",
            metadata={
                "order_id": order.id,
                "offer_id": order.offer.id if order.offer else None,
            },
            receipt_email=request.user.email,
        )
        order.stripe_payment_intent = intent.id
        order.save(update_fields=["stripe_payment_intent"])
    else:
        intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)

    context = {
        "order": order,
        "client_secret": intent.client_secret,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, "checkout/payment_page.html", context)


def success(request):
    """
    Render the success page after a successful payment.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the payment success template.
    """
    return render(request, "checkout/success.html")


def error(request):
    """
    Render the error page when a payment fails or is canceled.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the payment error template.
    """
    return render(request, "checkout/error.html")
