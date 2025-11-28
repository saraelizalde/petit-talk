from django.urls import path
from . import views

app_name = "newsletter"

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path("unsubscribe/<str:email>/", views.unsubscribe, name="unsubscribe"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
