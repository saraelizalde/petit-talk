from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_student', 'is_teacher', 'language_level')
    list_filter = ('is_student', 'is_teacher', 'language_level')