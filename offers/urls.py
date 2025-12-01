from django.urls import path
from . import views

app_name = "offers"

urlpatterns = [
    path("active/", views.active_offers, name="active_offers"),
    path('offer-dashboard/', views.admin_offers, name='admin_offers'),
    path('offer-dashboard/edit/<int:pk>/', views.admin_edit_offer,
         name='admin_edit_offer'),
]
