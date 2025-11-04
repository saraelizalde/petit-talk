from django.db import models
from django.contrib.auth.models import User

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    favorite_word = models.CharField(max_length=100, blank=True)
    favorite_movie = models.CharField(max_length=100, blank=True)
    favorite_book = models.CharField(max_length=100, blank=True)
    favorite_song = models.CharField(max_length=100, blank=True)
    intro_video = models.URLField(blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True)
    language_level = models.CharField(max_length=2, choices=LEVELS, blank=True)
    goals = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"