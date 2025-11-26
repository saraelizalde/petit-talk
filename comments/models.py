from django.db import models
from django.contrib.auth.models import User
from userprofile.models import Profile

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.username}"
