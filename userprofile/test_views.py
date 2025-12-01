from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from userprofile.models import Profile


class UserProfileViewsTest(TestCase):
    """Tests for userprofile app views."""

    def setUp(self):
        """Create users for testing."""
        self.user = User.objects.create_user(
            username='student',
            password='password123'
        )
        self.teacher = User.objects.create_user(
            username='teacher',
            password='password123'
        )
        self.teacher.profile.is_teacher = True
        self.teacher.profile.save()
        self.staff = User.objects.create_user(
            username='admin',
            password='adminpass'
        )
        self.staff.is_staff = True
        self.staff.save()

    def test_profile_detail_requires_login(self):
        """Accessing profile_detail without login redirects to login."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # redirect to login

        self.client.login(username='student', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/profile_detail.html')

    def test_public_profile_view(self):
        """Public profile should render correctly."""
        response = self.client.get(reverse(
            'profile_detail',
            args=[self.teacher.id]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/profile_detail.html')

    def test_profile_edit_get_and_post(self):
        """Profile edit GET renders form, POST updates profile."""
        self.client.login(username='student', password='password123')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

        response = self.client.post(reverse('edit_profile'), {
            'bio': 'Updated bio',
            'language_level': 'B1',
            'goals': 'Learn Python',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')

    def test_teacher_profile_view(self):
        """Teacher profile public page should work."""
        response = self.client.get(reverse(
            'teacher_profile',
            args=[self.teacher.id]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/teacher_profile.html')

    def test_teacher_profile_edit_access(self):
        """Non-teachers cannot access teacher_profile_edit."""
        self.client.login(username='student', password='password123')
        response = self.client.get(reverse('teacher_profile_edit'))
        self.assertRedirects(response, reverse('profile'))

        self.client.login(username='teacher', password='password123')
        response = self.client.get(reverse('teacher_profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_admin_teachers_view(self):
        """Only staff can access admin_teachers."""
        self.client.login(username='student', password='password123')
        response = self.client.get(reverse('admin_teachers'))
        self.assertEqual(response.status_code, 302)  # redirect

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('admin_teachers'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('teachers', response.context)
        self.assertIn('form', response.context)

    def test_admin_edit_and_delete_teacher(self):
        """Staff can edit and delete teacher profiles."""
        self.client.login(username='admin', password='adminpass')
        # Edit
        response = self.client.get(reverse(
            'admin_edit_teacher',
            args=[self.teacher.profile.id]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

        response = self.client.post(reverse(
            'admin_edit_teacher',
            args=[self.teacher.profile.id]
            ), {
            'first_name': 'New',
            'last_name': 'Name',
            'email': 'new@example.com',
            'bio': 'Updated bio'
        })
        self.assertRedirects(response, reverse('admin_teachers'))
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.first_name, 'New')
        self.assertEqual(self.teacher.profile.bio, 'Updated bio')

        # Delete
        response = self.client.post(reverse(
            'admin_delete_teacher',
            args=[self.teacher.profile.id]
            )
        )
        self.assertRedirects(response, reverse('admin_teachers'))
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='teacher')
