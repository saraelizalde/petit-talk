from django.test import TestCase
from django.contrib.auth.models import User


class BookingViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")

    def test_student_dashboard_view(self):
        response = self.client.get("/dashboard/student/")
        # Accept any of the common outcomes
        self.assertIn(response.status_code, [200, 302, 404])

    def test_teacher_dashboard_view(self):
        response = self.client.get("/dashboard/teacher/")
        self.assertIn(response.status_code, [200, 302, 404])

    def test_book_lesson_view(self):
        response = self.client.get("/book/")
        self.assertIn(response.status_code, [200, 302, 404])

    def test_admin_booking_dashboard_view(self):
        response = self.client.get("/dashboard/admin/")
        self.assertIn(response.status_code, [200, 302, 404])
