from django.urls import path
from .views import submit_comment
from . import views

urlpatterns = [
    path("add/", submit_comment, name="submit_comment"),
    path("dashboard/", views.comments_dashboard, name="comments_dashboard"),
    path("approve/<int:comment_id>/", views.approve_comment,
         name="approve_comment"),
    path("delete/<int:comment_id>/", views.delete_comment,
         name="delete_comment"),
]
