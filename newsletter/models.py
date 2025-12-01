from django.db import models


class Newsletter(models.Model):
    """
    Represents a newsletter subscription entry.

    Fields:
        email (EmailField):
            Unique email used to identify the subscriber.

        first_name (CharField):
            Optional first name of the subscriber.

        created_at (DateTimeField):
            Timestamp of when the subscription was created.

        is_active (BooleanField):
            Indicates whether the user is actively subscribed.
            Used instead of deletion so unsubscribed users can be reactivated.

    __str__:
        Returns the subscriber's email for admin and debugging clarity.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
