import stripe
from django.conf import settings
from django.http import HttpResponse
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.completed":
        intent = event["data"]["object"]
        order_id = intent["metadata"]["order_id"]

        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()

        for b in order.bookings.all():
            b.status = "PAID"
            b.save()

    return HttpResponse(status=200)
