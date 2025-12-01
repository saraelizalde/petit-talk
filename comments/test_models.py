from django.test import TestCase
from django.contrib.auth.models import User
from userprofile.models import Profile
from comments.models import Comment


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.comment = Comment.objects.create(
            user=self.user,
            profile=self.profile,
            content="This is a test comment."
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "This is a test comment.")
        self.assertFalse(self.comment.is_approved)
        self.assertEqual(str(self.comment), f"Comment by {self.user.username}")
