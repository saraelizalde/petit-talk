from django.test import TestCase
from .models import Offer
from decimal import Decimal


class SimpleOfferTest(TestCase):
    def test_offer_creation(self):
        """Simple test to ensure an Offer can be created."""
        offer = Offer.objects.create(
            name="Simple Offer",
            discount_type=Offer.PERCENTAGE,
            discount_value=Decimal("10.00")
        )
        self.assertEqual(offer.name, "Simple Offer")
        self.assertTrue(offer.active)
