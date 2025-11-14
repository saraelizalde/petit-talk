from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Booking
from .forms import BookingForm
from userprofile.models import Profile


@login_required
def book_lesson(request):
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            teacher = booking.teacher
            existing = Booking.objects.filter(
                teacher=teacher,
                scheduled_time=booking.scheduled_time,
                status__in=["pending", "confirmed"]
            ).exists()

            if existing:
                messages.error(request, "This time slot is already booked. Please choose another.")
            else:
                booking.save()
                messages.success(
                    request,
                    f"Your booking with {teacher.username} is confirmed for {booking.scheduled_time.strftime('%Y-%m-%d %H:%M')}."
                )
                return redirect("student_dashboard")
    else:
        form = BookingForm(user=request.user)

    return render(request, "bookings/book_lesson.html", {"form": form})


@login_required
def student_dashboard(request):
    bookings = Booking.objects.filter(student=request.user).order_by("-created_at")
    return render(request, "bookings/student_dashboard.html", {"bookings": bookings})


@login_required
def teacher_dashboard(request):
    if not request.user.profile.is_teacher:
        messages.error(request, "You are not authorized to access the teacher dashboard.")
        return redirect("home")
    bookings = Booking.objects.filter(teacher=request.user).order_by("-scheduled_time")
    return render(request, "bookings/teacher_dashboard.html", {"bookings": bookings})


@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.teacher:
        messages.error(request, "You are not allowed to confirm this booking.")
        return redirect("teacher_dashboard")

    booking.status = "confirmed"
    booking.save()

    messages.success(request, "Booking confirmed successfully.")
    return redirect("teacher_dashboard")


@login_required
def decline_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.teacher:
        messages.error(request, "You are not allowed to decline this booking.")
        return redirect("teacher_dashboard")

    booking.status = "declined"
    booking.save()

    messages.success(request, "Booking declined.")
    return redirect("teacher_dashboard")