import stripe
from django.conf import settings
from django.http import HttpResponse
from order.models import Order
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")
        return mark_order_as_paid(order_id)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        
        sessions = stripe.checkout.Session.list(payment_intent=intent["id"])
        if sessions and sessions.data:
            session = sessions.data[0]
            order_id = session["metadata"].get("order_id")
            return mark_order_as_paid(order_id)
        
    return HttpResponse(status=200)
        
def mark_order_as_paid(order_id):
    if not order_id:
        return HttpResponse(status=400)
        
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
        
    order.paid = True
    order.save()

    for b in order.bookings.all():
        b.status = "PAID"
        b.save()

    return HttpResponse(status=200)
