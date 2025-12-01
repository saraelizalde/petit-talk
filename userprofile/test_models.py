from django.test import TestCase
from django.contrib.auth.models import User
from userprofile.models import Profile


class ProfileModelTest(TestCase):
    """Test the Profile model and signals."""

    def test_profile_created_on_user_creation(self):
        """A Profile is automatically created when a User is created."""
        user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.assertTrue(hasattr(user, 'profile'))
        self.assertTrue(user.profile.is_student)
        self.assertFalse(user.profile.is_teacher)

    def test_profile_str(self):
        """__str__ returns username's Profile"""
        user = User.objects.create_user(
            username="alice",
            password="password123"
        )
        profile = user.profile
        self.assertEqual(str(profile), "alice's Profile")

    def test_profile_can_be_updated(self):
        """Profile fields can be updated and saved"""
        user = User.objects.create_user(username="bob", password="password123")
        profile = user.profile
        profile.bio = "This is a test bio"
        profile.language_level = "B1"
        profile.goals = "Learn Python"
        profile.save()
        updated_profile = Profile.objects.get(user=user)
        self.assertEqual(updated_profile.bio, "This is a test bio")
        self.assertEqual(updated_profile.language_level, "B1")
        self.assertEqual(updated_profile.goals, "Learn Python")
