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
    Receive and handle incoming webhook events from Stripe.

    This view:
        - Verifies the webhook signature to ensure authenticity.
        - Parses the incoming event payload.
        - Delegates the event to the appropriate handler method
          inside the StripeWH_Handler class.

    Supported Event Types:
        - `payment_intent.succeeded`: Fired when a PaymentIntent
          successfully completes.
        - `checkout.session.completed`: Fired when a Checkout Session
          finishes successfully.

    Any unhandled events are passed to a generic fallback handler.

    Args:
        request (HttpRequest):
            The raw HTTP request sent by Stripe, containing the
            webhook JSON payload and signature header.

    Returns:
        HttpResponse:
            A response acknowledging receipt of the event.
            If verification fails, a 400 response is returned.
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
        "payment_intent.succeeded":
            handler.handle_payment_intent_succeeded,
        "checkout.session.completed":
            handler.handle_checkout_session_completed,
    }

    # Get the correct handler or fall back to the generic handler
    event_handler = event_map.get(event["type"], handler.handle_event)

    return event_handler(event)
