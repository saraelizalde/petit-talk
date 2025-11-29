import stripe
from django.http import HttpResponse
from order.models import Order


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle unexpected or unregistered events
        """
        return HttpResponse(
            content=f"Unhandled event type {event['type']}",
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle payment_intent.succeeded webhook.
        """
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")

        return self._mark_order_as_paid(order_id, event["type"])

    def handle_checkout_session_completed(self, event):
        """
        Handle checkout.session.completed webhook.
        """
        session = event["data"]["object"]
        order_id = session.get("metadata", {}).get("order_id")

        return self._mark_order_as_paid(order_id, event["type"])

    def _mark_order_as_paid(self, order_id, event_type):
        """
        Update the order + bookings as paid.
        """
        if not order_id:
            return HttpResponse(
                content=f"Webhook {event_type}: Missing order_id",
                status=400
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponse(
                content=f"Webhook {event_type}: Order not found",
                status=404
            )

        # Mark order as paid
        order.paid = True
        order.save(update_fields=["paid"])

        # Mark all bookings as paid
        for booking in order.bookings.all():
            booking.status = "PAID"
            booking.save(update_fields=["status"])

        return HttpResponse(
            content=f"Webhook {event_type}: Order {order_id} marked as PAID",
            status=200
        )
