from django.urls import path
from . import views

urlpatterns = [
    path("book/", views.book_lesson, name="book_lesson"),
    path("dashboard/student/", views.student_dashboard, name="student_dashboard"),
    path("dashboard/teacher/", views.teacher_dashboard, name="teacher_dashboard"),
]
