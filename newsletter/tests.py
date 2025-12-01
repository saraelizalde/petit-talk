from django.test import TestCase
from .models import Newsletter


class NewsletterSimpleTests(TestCase):

    def test_create_newsletter(self):
        """Test creating a newsletter subscriber."""
        subscriber = Newsletter.objects.create(
            email="test@example.com",
            first_name="Test"
        )
        self.assertEqual(subscriber.email, "test@example.com")
        self.assertEqual(subscriber.first_name, "Test")
        self.assertTrue(subscriber.is_active)

    def test_str_method(self):
        """Test the __str__ method of Newsletter."""
        subscriber = Newsletter.objects.create(email="str@example.com")
        self.assertEqual(str(subscriber), "str@example.com")

    def test_unsubscribe_flag(self):
        """Test unsubscribing by setting is_active to False."""
        subscriber = Newsletter.objects.create(email="unsubscribe@example.com")
        subscriber.is_active = False
        subscriber.save()
        subscriber.refresh_from_db()
        self.assertFalse(subscriber.is_active)

    def test_create_with_no_first_name(self):
        """Test creating a subscriber without a first name."""
        subscriber = Newsletter.objects.create(email="nofirst@example.com")
        self.assertEqual(subscriber.first_name, None)
        self.assertTrue(subscriber.is_active)
