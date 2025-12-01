from django.db import models
from django.contrib.auth.models import User
from userprofile.models import Profile


class Comment(models.Model):
    """
    Stores a comment written by a user about a profile.

    Fields:
        user (ForeignKey):
            The user who wrote the comment.

        profile (ForeignKey):
            The profile the comment is associated with.
            Optional — can be null if needed for future flexibility.

        content (TextField):
            The actual comment text.

        created_at (DateTimeField):
            Timestamp automatically set when the comment is created.

        is_approved (BooleanField):
            Indicates whether the comment has been reviewed and approved.
            Useful for moderation workflows.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the Comment instance.

        Returns:
            str: A short label showing which user wrote the comment.
        """
        return f"Comment by {self.user.username}"
