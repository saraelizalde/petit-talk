from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from userprofile.models import Profile
from comments.models import Comment


class CommentViewsTest(TestCase):
    def setUp(self):
        # Users
        self.user = User.objects.create_user(
            username="normaluser",
            password="pass123"
        )
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="pass123",
            is_staff=True
        )

        # Profiles
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.staff_profile, _ = Profile.objects.get_or_create(
            user=self.staff_user
        )

        # Client
        self.client = Client()

        # A comment to test approve/delete
        self.comment = Comment.objects.create(
            user=self.user,
            profile=self.profile,
            content="Test comment"
        )

    def test_submit_comment_unauthenticated(self):
        response = self.client.post(
            reverse("submit_comment"),
            {"content": "Hi"}
        )
        # Redirects to home
        self.assertEqual(response.status_code, 302)

    def test_submit_comment_authenticated(self):
        self.client.login(username="normaluser", password="pass123")
        response = self.client.post(
            reverse("submit_comment"),
            {"content": "Hello"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content="Hello").exists())

    def test_comments_dashboard_staff(self):
        self.client.login(username="staffuser", password="pass123")
        response = self.client.get(reverse("comments_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_comments_dashboard_non_staff(self):
        self.client.login(username="normaluser", password="pass123")
        response = self.client.get(reverse("comments_dashboard"))
        # Redirected because not staff
        self.assertEqual(response.status_code, 302)

    def test_approve_comment(self):
        self.client.login(username="staffuser", password="pass123")
        response = self.client.get(
            reverse("approve_comment",
                    args=[self.comment.id])
                )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertTrue(self.comment.is_approved)

    def test_delete_comment(self):
        self.client.login(username="staffuser", password="pass123")
        response = self.client.get(
            reverse("delete_comment",
                    args=[self.comment.id])
                )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
