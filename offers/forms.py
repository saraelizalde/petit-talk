from django import forms
from .models import Offer


class OfferForm(forms.ModelForm):
    """
    Form used by administrators to create or update promotional offers.

    Allows editing:
        - Name, description
        - Discount type and value
        - Active state
        - Optional promotional image
    """
    class Meta:
        model = Offer
        fields = [
            'name', 'description',
            'discount_type', 'discount_value',
            'active', 'image'
        ]
