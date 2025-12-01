from django.db import models


class Offer(models.Model):
    """
    Represents a promotional offer that can apply discounts at checkout.

    Fields:
        name (str): Name of the offer.
        description (str): Optional detailed text about the promotion.
        discount_type (str): Type of discount (percentage or fixed amount).
        discount_value (Decimal): Value applied depending on discount type.
        image (ImageField): Optional offer banner.
        active (bool): Whether the offer is currently available.
        created_at (datetime): When the offer was created.
        updated_at (datetime): Last modification timestamp.

    Behavior:
        - Offers automatically order newest-first.
        - Provides helper methods for activation checks and applying discounts.
    """

    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    BUNDLE = "bundle"

    DISCOUNT_CHOICES = [
        (PERCENTAGE, "Percentage"),
        (FIXED_AMOUNT, "Fixed Amount"),
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
        """Return readable admin-friendly representation."""
        return f"{self.name} ({'Active' if self.active else 'Inactive'})"

    def is_active(self):
        """
        Return True if the offer is active.

        Useful for template checks and business logic.
        """

        return self.active

    def apply_discount(self, subtotal):
        """
        Apply the offer discount to a given subtotal.

        Args:
            subtotal (Decimal): The current order subtotal.

        Returns:
            Decimal: The new total after applying the discount.
        """
        if self.discount_type == 'percentage':
            return subtotal - (subtotal * (self.discount_value / 100))
        if self.discount_type == 'fixed_amount':
            return max(subtotal - self.discount_value, 0)
        return subtotal
