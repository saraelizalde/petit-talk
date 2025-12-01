from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

from bookings.models import Booking


def make_booking(student, teacher, status="UNPAID"):
    """Create a minimal valid booking for tests."""
    return Booking.objects.create(
        student=student,
        teacher=teacher,
        status=status,
        scheduled_time=make_aware(datetime.now() + timedelta(days=1)),
    )


class OrderViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

        # create student and teacher because teacher_id is required
        self.user = User.objects.create_user(
            username="student",
            password="pass123"
        )
        self.teacher = User.objects.create_user(
            username="teacher",
            password="pass456"
        )

    # View bag tests
    def test_view_bag_requires_login(self):
        response = self.client.get(reverse("view_bag"))
        self.assertEqual(response.status_code, 302)

    def test_view_bag_logged_in(self):
        self.client.login(username="student", password="pass123")
        response = self.client.get(reverse("view_bag"))
        self.assertEqual(response.status_code, 200)

    # Remove from bag test
    def test_remove_from_bag_requires_login(self):
        booking = make_booking(self.user, self.teacher)
        response = self.client.get(reverse(
            "remove_from_bag", args=[booking.id]))
        self.assertEqual(response.status_code, 302)

    def test_remove_from_bag_logged_in(self):
        self.client.login(username="student", password="pass123")

        booking = make_booking(self.user, self.teacher)

        response = self.client.get(reverse(
            "remove_from_bag", args=[booking.id]))
        self.assertEqual(response.status_code, 302)

        # booking should be deleted
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())
