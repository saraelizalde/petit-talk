from django.test import TestCase
from django.contrib.auth.models import User
from userprofile.models import Profile
from comments.forms import CommentForm


class CommentFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="formuser",
            password="testpass"
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user)

    def test_form_valid(self):
        form_data = {"content": "Form test comment"}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_empty(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
