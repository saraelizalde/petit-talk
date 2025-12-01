from django.test import TestCase
from django.contrib.auth.models import User
from bookings.forms import BookingForm
from django.utils import timezone
from datetime import timedelta


class BookingFormTest(TestCase):
    def setUp(self):
        # Create student and teacher users
        self.student = User.objects.create_user(
            username='student1',
            password='pass'
        )
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='pass'
        )

        # Mark teacher as a teacher if your form filters on profile__is_teacher
        if hasattr(self.teacher, 'profile'):
            self.teacher.profile.is_teacher = True
            self.teacher.profile.save()

    def test_booking_form_valid(self):
        """Simple test: form is valid with minimal required data"""
        future_date = (timezone.now() + timedelta(days=3)).date()
        form_data = {
            'teacher': self.teacher.id,
            'date': future_date,
            'hour': '10:00',
            'purpose': 'Test lesson'
        }
        form = BookingForm(data=form_data, user=self.student)

        # Assign the student to the instance so clean() passes
        form.instance.student = self.student

        self.assertTrue(form.is_valid())
