from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Booking
from .forms import BookingForm
from userprofile.models import Profile


@login_required
def book_lesson(request):
    """
    Handle the creation of a new lesson booking.

    GET:
        Displays an empty BookingForm and optionally pre-selects a teacher.

    POST:
        - Injects the student into the form before validation.
        - Validates scheduling rules (48h, teacher conflict, student conflict).
        - Saves the booking and redirects the user to their bag.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the booking form page or redirects to view_bag on success.
    """
    teacher_id = request.GET.get("teacher")
    
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)

        form.instance.student = request.user

        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            booking.scheduled_time = form.cleaned_data["scheduled_time"]
            booking.save()

            messages.success(
                request,
                f"Your booking with {booking.teacher.username} is confirmed for "
                f"{booking.scheduled_time.strftime('%Y-%m-%d %H:%M')}."
            )    
            return redirect("view_bag")
    else:
        form = BookingForm(user=request.user)

        if teacher_id:
            form.fields["teacher"].initial = teacher_id

    return render(request, "bookings/book_lesson.html", {"form": form})


@login_required
def student_dashboard(request):
    """
    Display the dashboard for a student showing their bookings.

    Supports filtering by:
        - 'upcoming': future bookings
        - 'past': past bookings
        - 'all': all bookings

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the student dashboard with filtered bookings.
    """
    filter_option = request.GET.get("filter", "all")
    now = timezone.now()

    bookings = Booking.objects.filter(student=request.user)

    if filter_option == "upcoming":
        bookings = bookings.filter(scheduled_time__gte=now).order_by("scheduled_time")

    elif filter_option == "past":
        bookings = bookings.filter(scheduled_time__lt=now).order_by("-scheduled_time")

    else:
        bookings = bookings.order_by("scheduled_time")

    return render(
        request,
        "bookings/student_dashboard.html",
        {
            "bookings": bookings,
            "filter": filter_option
        }
    )


@login_required
def teacher_dashboard(request):
    """
    Display the dashboard for teachers showing their bookings.

    Access is restricted to users marked as teachers.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the teacher dashboard or redirects unauthorized users.
    """
    if not request.user.profile.is_teacher:
        messages.error(request, "You are not authorized to access the teacher dashboard.")
        return redirect("home")
    bookings = Booking.objects.filter(teacher=request.user).order_by("-scheduled_time")
    return render(request, "bookings/teacher_dashboard.html", {"bookings": bookings})


@login_required
def confirm_booking(request, booking_id):
    """
    Allow a teacher to confirm a booking.

    Only the teacher associated with the booking can confirm it.

    Args:
        request (HttpRequest): The HTTP request object.
        booking_id (int): ID of the booking to confirm.

    Returns:
        HttpResponse: Redirects to the teacher dashboard with a success or error message.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.teacher:
        messages.error(request, "You are not allowed to confirm this booking.")
        return redirect("teacher_dashboard")

    booking.status = "confirmed"
    booking.save()

    messages.success(request, "This booking is confirmed")
    return redirect("teacher_dashboard")


@login_required
def decline_booking(request, booking_id):
    """
    Allow a teacher to decline a booking.

    Only the teacher associated with the booking can decline it.

    Args:
        request (HttpRequest): The HTTP request object.
        booking_id (int): ID of the booking to decline.

    Returns:
        HttpResponse: Redirects to the teacher dashboard with a success or error message.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.teacher:
        messages.error(request, "You are not allowed to decline this booking.")
        return redirect("teacher_dashboard")

    booking.status = "declined"
    booking.save()

    messages.success(request, "Booking declined.")
    return redirect("teacher_dashboard")

@staff_member_required
def admin_booking_dashboard(request):
    """
    Display all bookings for staff in an administrative dashboard.

    Bookings are sorted by scheduled time in descending order.
    Uses select_related to optimize student and teacher queries.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the admin dashboard with all bookings.
    """
    bookings = Booking.objects.select_related("student", "teacher").order_by("-scheduled_time")
    return render(request, "bookings/admin_dashboard.html", {"bookings": bookings})

@staff_member_required
def admin_update_booking_status(request, booking_id, new_status):
    """
    Allow staff to update the status of a booking.

    Args:
        request (HttpRequest): The HTTP request object.
        booking_id (int): ID of the booking to update.
        new_status (str): New status to assign to the booking.

    Returns:
        HttpResponse: Redirects to the admin dashboard with a success message.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = new_status
    booking.save()
    messages.success(request, f"Booking status updated to {new_status}.")
    return redirect("admin_booking_dashboard")

@staff_member_required
def admin_delete_booking(request, booking_id):
    """
    Allow staff to delete a booking from the system.

    Args:
        request (HttpRequest): The HTTP request object.
        booking_id (int): ID of the booking to delete.

    Returns:
        HttpResponse: Redirects to the admin dashboard with a success message.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.success(request, "Booking deleted.")
    return redirect("admin_booking_dashboard")