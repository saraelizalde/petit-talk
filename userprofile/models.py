from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Language level choices
LEVELS = [
    ('A1', 'A1 - Beginner'),
    ('A2', 'A2 - Elementary'),
    ('B1', 'B1 - Intermediate'),
    ('B2', 'B2 - Upper Intermediate'),
    ('C1', 'C1 - Advanced'),
    ('C2', 'C2 - Proficiency'),
]


class Profile(models.Model):
    """
    Profile model extending the built-in Django User.

    Attributes:
        user (OneToOneField): Linked User instance.
        is_student (bool): Flag for student role.
        is_teacher (bool): Flag for teacher role.
        bio (str): Optional biography text.
        profile_image (ImageField): Optional profile picture.
        favorite_word/movie/book/song (str): Optional personal info fields.
        intro_video (FileField): Optional introductory video for teachers.
        language_level (str): Choice field for user's language proficiency.
        goals (str): Optional text for user goals.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    favorite_word = models.CharField(max_length=100, blank=True)
    favorite_movie = models.CharField(max_length=100, blank=True)
    favorite_book = models.CharField(max_length=100, blank=True)
    favorite_song = models.CharField(max_length=100, blank=True)
    intro_video = models.FileField(
        upload_to='profile_videos/',
        blank=True,
        null=True
    )
    language_level = models.CharField(max_length=2, choices=LEVELS, blank=True)
    goals = models.TextField(blank=True)

    def __str__(self):
        """
        Return a readable string representation of the Profile.
        """
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create or update a Profile whenever
    a User is saved.

    Args:
        sender (Model): The model class (User).
        instance (User): The actual instance being saved.
        created (bool): True if a new User was created.
        **kwargs: Additional keyword arguments.

    Behavior:
        - If a new User is created, create a Profile and mark as student
        by default.
        - If an existing User is updated, ensure a Profile exists and save it.
    """
    if created:
        Profile.objects.create(user=instance, is_student=True)
    else:
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()
