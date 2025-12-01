import stripe
from django.http import HttpResponse
from order.models import Order


class StripeWH_Handler:
    """
    Handle Stripe webhooks events.

    This class processes incoming webhook events sent by Stripe and
    updates orders/bookings accordingly. Each event type is routed
    to a corresponding handler method.
    """

    def __init__(self, request):
        """
        Initialize the webhook handler.

        Args:
            request (HttpRequest): The raw incoming webhook request
            from Stripe.
        """
        self.request = request

    def handle_event(self, event):
        """
        Handle unknown or unregistered Stripe events.

        This acts as a fallback for any event types that do not have
        a specific handler method implemented.

        Args:
            event (dict): Parsed webhook event payload from Stripe.

        Returns:
            HttpResponse: Acknowledgement that the event was received.
        """
        return HttpResponse(
            content=f"Unhandled event type {event['type']}",
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook event.

        Triggered when Stripe successfully processes a PaymentIntent.
        Extracts the order ID from metadata and marks the order + its
        bookings as paid.

        Args:
            event (dict): Webhook event data from Stripe.

        Returns:
            HttpResponse: Result of order processing.
        """
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")

        return self._mark_order_as_paid(order_id, event["type"])

    def handle_checkout_session_completed(self, event):
        """
        Handle the checkout.session.completed webhook event.

        Fired when a Stripe Checkout Session completes successfully.
        Extracts the associated order ID and marks the order
        + bookings as paid.

        Args:
            event (dict): Webhook event containing checkout session data.

        Returns:
            HttpResponse: Result of order processing.
        """
        session = event["data"]["object"]
        order_id = session.get("metadata", {}).get("order_id")

        return self._mark_order_as_paid(order_id, event["type"])

    def _mark_order_as_paid(self, order_id, event_type):
        """
        Mark an order and its bookings as paid.

        This method:
            - Validates the order exists.
            - Sets order.paid = True.
            - Updates each linked booking's status to "PAID".

        Args:
            order_id (str or int): ID of the order to update.
            event_type (str): The type of webhook event triggering this update.

        Returns:
            HttpResponse: Status message indicating success or failure.
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
