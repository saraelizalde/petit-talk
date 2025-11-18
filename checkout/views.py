from django.shortcuts import redirect, render, get_object_or_404
import stripe
from django.conf import settings
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id, student=request.user)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        customer_email=request.user.email,
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "unit_amount": int(order.total_eur * 100),
                    "product_data": {"name": f"{order.bookings.count()} Lessons"},
                },
                "quantity": 1,
            }
        ],
        metadata={"order_id": order.id},
        success_url=request.build_absolute_uri("/checkout/success/"),
        cancel_url=request.build_absolute_uri("/checkout/error/"),
    )

    order.stripe_payment_intent = session.payment_intent
    order.stripe_session_id = session.id
    order.save()

    return redirect(session.url)

