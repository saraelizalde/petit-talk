from django import forms
from .models import Booking
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Select Date"
    )

    hour = forms.ChoiceField(
        choices=[(f"{h:02d}:00", f"{h:02d}:00") for h in range(8, 20)],
        label="Select Hour"
    )

    purpose = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'What would you like to focus on during your lesson?'
        }),
        required=False,
        label="Lesson Goal or Focus"
    )

    class Meta:
        model = Booking
        fields = ["teacher", "date", "hour", "purpose"]
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = (
            self.fields['teacher'].queryset.filter(profile__is_teacher=True)
        )

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        hour_str = cleaned_data.get("hour")
        teacher = cleaned_data.get("teacher")

        if not date or not hour_str or not teacher:
            return cleaned_data

        hour_int = int(hour_str[:2])
        scheduled_time = datetime.combine(date, time(hour_int, 0))
        scheduled_time = timezone.make_aware(scheduled_time)

        # Save into the form instance
        cleaned_data["scheduled_time"] = scheduled_time
        self.instance.scheduled_time = scheduled_time

        # 48-hour rule
        if scheduled_time < timezone.now() + timedelta(hours=48):
            raise ValidationError("Bookings must be made at least 48 hours in advance.")

        # Allowed hours
        if not (8 <= hour_int <= 19):
            raise ValidationError(
                "Bookings are only available hourly between 08:00 and 20:00 (last start 19:00)."
            )

        # Check double booking for the same teacher
        conflict = Booking.objects.filter(
            teacher=teacher,
            scheduled_time=scheduled_time
        ).exclude(status__iexact='CANCELLED').exclude(status__iexact='COMPLETED')

        if self.instance.pk:
            conflict = conflict.exclude(pk=self.instance.pk)

        if conflict.exists():
            raise ValidationError("This time slot is already booked for this teacher.")

        return cleaned_data
