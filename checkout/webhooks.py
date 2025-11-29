import stripe
from django.conf import settings
from django.http import HttpResponse
from order.models import Order
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import StripeWH_Handler

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def stripe_webhook(request):
    """
    Handle incoming Stripe webhook events.

    Event sent:
    - payment_intent.succeeded
    - checkout.session.completed
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        # Invalid payload or invalid signature
        return HttpResponse(status=400)

    handler = StripeWH_Handler(request)

    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "checkout.session.completed": handler.handle_checkout_session_completed,
    }

    # Get the correct handler or fall back to the generic handler
    event_handler = event_map.get(event["type"], handler.handle_event)

    return event_handler(event)
