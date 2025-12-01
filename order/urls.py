from django.urls import path
from . import views

urlpatterns = [
    path('bag/', views.view_bag, name='view_bag'),
    path('bag/remove/<int:booking_id>/',
         views.remove_from_bag, name='remove_from_bag'),
]
