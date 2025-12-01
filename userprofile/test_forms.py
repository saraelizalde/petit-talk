from django.test import TestCase
from django.contrib.auth.models import User
from userprofile.forms import (
    ProfileForm,
    TeacherProfileEditForm,
    AdminTeacherForm,
    AdminTeacherEditForm
)
from userprofile.models import Profile


class ProfileFormsTest(TestCase):
    """Test cases for userprofile forms."""

    def setUp(self):
        """Create a sample user and profile for testing."""
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.profile = self.user.profile
        self.profile.is_teacher = True
        self.profile.save()

    def test_profile_form_valid(self):
        """ProfileForm should be valid with proper data."""
        form_data = {
            'bio': 'Hello world',
            'language_level': 'B1',
            'goals': 'Learn Python',
            'favorite_word': 'serendipity',
            'favorite_movie': 'Inception',
            'favorite_book': '1984',
            'favorite_song': 'Imagine',
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_teacher_profile_edit_form_valid(self):
        """TeacherProfileEditForm should be valid with proper data."""
        form_data = {
            'bio': 'Teacher bio',
            'favorite_word': 'ephemeral',
            'favorite_movie': 'Interstellar',
            'favorite_book': 'Dune',
            'favorite_song': 'Bohemian Rhapsody',
        }
        form = TeacherProfileEditForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_admin_teacher_form_creates_user_and_profile(self):
        """AdminTeacherForm should create a new User
        and Profile with teacher role."""
        form_data = {
            'username': 'teacher1',
            'email': 'teacher1@example.com',
            'password': 'securepassword',
            'bio': 'Bio for teacher1',
        }
        form = AdminTeacherForm(data=form_data)
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.assertEqual(profile.user.username, 'teacher1')
        self.assertTrue(profile.is_teacher)
        self.assertFalse(profile.is_student)

    def test_admin_teacher_form_unique_username_email(self):
        """AdminTeacherForm should raise validation
        error for duplicate username or email."""
        User.objects.create_user(
            username='duplicate',
            email='dup@example.com',
            password='pass123'
        )
        form_data = {
            'username': 'duplicate',
            'email': 'dup@example.com',
            'password': 'newpass',
        }
        form = AdminTeacherForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)

    def test_admin_teacher_edit_form_updates_user_and_profile(self):
        """AdminTeacherEditForm should update the User and Profile fields."""
        form_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'bio': 'Updated bio',
        }
        form = AdminTeacherEditForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.user.first_name, 'Alice')
        self.assertEqual(updated_profile.user.last_name, 'Smith')
        self.assertEqual(updated_profile.user.email, 'alice@example.com')
        self.assertEqual(updated_profile.bio, 'Updated bio')
