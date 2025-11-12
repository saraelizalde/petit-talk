from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_detail, name='profile'),
    path('edit/', views.profile_edit, name='edit_profile'),
    path('<int:user_id>/', views.teacher_profile, name='teacher_profile'),
]

