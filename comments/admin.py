from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('user__username', 'content')

admin.site.register(Comment, CommentAdmin)
