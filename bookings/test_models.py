from django.test import TestCase
from django.contrib.auth.models import User
from .models import Booking
from django.utils import timezone
from datetime import timedelta


class BookingModelTest(TestCase):
    def setUp(self):
        # Create a student and teacher user
        self.student = User.objects.create_user(
            username='student1',
            password='pass'
        )
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='pass'
        )

    def test_booking_creation(self):
        """Test a simple booking creation."""
        scheduled_time = timezone.now() + timedelta(days=3)
        booking = Booking.objects.create(
            student=self.student,
            teacher=self.teacher,
            scheduled_time=scheduled_time,
            purpose='Test lesson',
            status='UNPAID'
        )
        # Simple asserts to ensure it was created
        self.assertEqual(booking.student.username, 'student1')
        self.assertEqual(booking.teacher.username, 'teacher1')
        self.assertEqual(booking.status, 'UNPAID')
        self.assertEqual(
            str(booking),
            f"student1 with teacher1 at {scheduled_time.strftime(
                '%Y-%m-%d %H:%M'
                )}")
