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
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
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

    def apply_discount(self, subtotal):
        """Return discounted total based on offer type."""
        if self.discount_type == 'percentage':
            return subtotal - (subtotal * (self.discount_value / 100))
        if self.discount_type == 'fixed_amount':
            return max(subtotal - self.discount_value, 0)
        #if self.discount_type == 'bundle':
            #return subtotal  
        return subtotal


