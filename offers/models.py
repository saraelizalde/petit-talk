from django.db import models

class Offer(models.Model):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    BUNDLE = "bundle"

    DISCOUNT_CHOICES = [
        (PERCENTAGE, "Percentage"),
        (FIXED_AMOUNT, "Fixed Amount"),
        (BUNDLE, "Bundle"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES)
    discount_value = models.DecimalField(max_digits=8, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({'Active' if self.active else 'Inactive'})"

    def is_active(self):
        """Return True if the offer is active."""
        return self.active


