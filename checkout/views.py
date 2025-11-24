from django.shortcuts import redirect, render, get_object_or_404
import stripe
from django.contrib import messages
from django.conf import settings
from offers.models import Offer
from order.models import Order
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id, student=request.user)

    pending_bookings = order.bookings.filter(status="PENDING")
    if not pending_bookings.exists():
        messages.error(request, "There are no unpaid bookings in this order.")
        return redirect("view_bag")
    
    active_offer = Offer.objects.filter(active=True).first()
    order.offer = active_offer if active_offer else None
    order.refresh_total()
    
    if order.total_eur <= 0:
        messages.error(request, "Checkout failed — invalid order total.")
        return redirect("view_bag")

    amount_cents = int(order.total_eur * 100)
    
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        customer_email=request.user.email,
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "unit_amount": int(order.total_eur * 100),
                    "product_data": {"name": f"{pending_bookings.count()} Lessons"},
                },
                "quantity": 1,
            }
        ],
        metadata={
            "order_id": order.id,
            "offer_id": order.offer.id if order.offer else None,
            "subtotal": str(order.subtotal),
            "total": str(order.total_eur),
        },
        success_url=request.build_absolute_uri(reverse("checkout_success")),
        cancel_url=request.build_absolute_uri(reverse("checkout_error")),
    )

    order.stripe_payment_intent = session.payment_intent
    order.stripe_session_id = session.id
    order.save(update_fields=["offer", "total_eur", "subtotal",
                              "stripe_payment_intent", "stripe_session_id"])

    return redirect(session.url)

def success(request):
    return render(request, "checkout/success.html")

def error(request):
    return render(request, "checkout/error.html")

