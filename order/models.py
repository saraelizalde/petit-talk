from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking
from django.db import transaction
from decimal import Decimal
from offers.models import Offer

CLASS_PRICE_EUR = Decimal("20.00")


class Order(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    bookings = models.ManyToManyField(Booking, related_name='orders')
    offer = models.ForeignKey(
        Offer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    subtotal = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_eur = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} — {self.student.username} — €{self.total_eur}"

    def calculate_subtotal(self):
        """Price before discount."""
        # If all bookings cost 20€:
        self.subtotal = CLASS_PRICE_EUR * self.bookings.count()
        return self.subtotal

    def calculate_total(self):
        """Apply offer (if any) to subtotal."""
        self.subtotal = CLASS_PRICE_EUR * self.bookings.count()

        if self.offer and self.offer.active:
            self.total_eur = self.offer.apply_discount(self.subtotal)
        else:
            self.total_eur = self.subtotal

        return self.total_eur

    def refresh_total(self):
        """Recalculate and save."""
        self.calculate_total()
        self.save(update_fields=['subtotal', 'total_eur'])
        return self.total_eur

    def auto_apply_offer(self):
        """Attach the currently active offer automatically."""
        active_offer = Offer.objects.filter(active=True).first()
        if not active_offer or self.offer == active_offer:
            return
        self.offer = active_offer
        self.refresh_total()
        self.save(update_fields=['offer', 'subtotal', 'total_eur'])

    @classmethod
    def get_or_create_basket(cls, user):
        """Returns an unpaid order (basket) for user."""
        order, created = cls.objects.get_or_create(student=user, paid=False)
        return order
