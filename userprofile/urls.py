from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_detail, name='profile'),
    path('edit/', views.profile_edit, name='edit_profile'),
    path('profile/<int:user_id>/', views.public_profile,
         name='profile_detail'),
    path('teacher/<int:user_id>/', views.teacher_profile,
         name='teacher_profile'),
    path('teacher/edit/', views.teacher_profile_edit,
         name='teacher_profile_edit'),
    path('teacher-dashboard/', views.admin_teachers,
         name='admin_teachers'),
    path('teacher-dashboard/edit/<int:pk>/', views.admin_edit_teacher,
         name='admin_edit_teacher'),
    path('teacher-dashboard/delete/<int:pk>/', views.admin_delete_teacher,
         name='admin_delete_teacher'),
]
