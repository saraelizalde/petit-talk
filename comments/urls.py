from django.urls import path
from .views import submit_comment

urlpatterns = [
    path("add/", submit_comment, name="submit_comment"),
]
