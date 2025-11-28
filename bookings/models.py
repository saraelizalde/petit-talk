from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

BOOKING_STATUS = [
    ('UNPAID', 'Unpaid'),
    ('PAID', 'Paid'),
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled'),
    ('COMPLETED', 'Completed'),
]


class Booking(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='student_bookings'
    )
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='teacher_bookings'
    )
    scheduled_time = models.DateTimeField()
    purpose = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=BOOKING_STATUS,
        default='UNPAID'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_time']
        unique_together = ('teacher', 'scheduled_time')  #Avoid double-booking for teachers

    def __str__(self):
        return f"{self.student.username} with {self.teacher.username} at {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        """
        Custom validation: prevent double booking and ensure 48-hour notice.
        """
        from django.core.exceptions import ValidationError

        # Check 48 hours in the future
        if self.scheduled_time < timezone.now() + timedelta(hours=48):
            raise ValidationError("Bookings must be made at least 48 hours in advance.")

        # Avoid double-booking
        overlap = Booking.objects.filter(
            teacher=self.teacher, scheduled_time=self.scheduled_time
        ).exclude(pk=self.pk)
        if overlap.exists():
            raise ValidationError("This time slot is already booked for this teacher.")
