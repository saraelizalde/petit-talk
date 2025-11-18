from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking
from django.db import transaction
from decimal import Decimal

CLASS_PRICE_EUR = Decimal("20.00")

class Order(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    bookings = models.ManyToManyField(Booking, related_name='orders')
    total_eur = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} — {self.student.username} — €{self.total_eur}"

    def calculate_total(self): # to update when offer is created
        self.total_eur = CLASS_PRICE_EUR * self.bookings.count()
        return self.total_eur
        
    def refresh_total(self):
        self.calculate_total()
        self.save(update_fields=['total_eur'])
        return self.total_eur

    @classmethod
    def get_or_create_basket(cls, user):
        # returns an unpaid order (basket) for user
        order, created = cls.objects.get_or_create(student=user, paid=False)
        return order