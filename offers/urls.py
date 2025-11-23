from django.urls import path
from . import views

app_name = "offers"

urlpatterns = [
    path("active/", views.active_offers, name="active_offers"),
]
