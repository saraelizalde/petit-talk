from django import forms
from .models import Booking
from datetime import datetime, timedelta
from django.utils import timezone

class BookingForm(forms.ModelForm):
    scheduled_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'min': (datetime.now() + timedelta(hours=48)).strftime('%Y-%m-%dT%H:%M')
        }),
        label="Select Date & Time"
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
        fields = ['teacher', 'scheduled_time', 'purpose']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = (
            self.fields['teacher'].queryset.filter(profile__is_teacher=True)
        )

    def clean_scheduled_time(self):
        scheduled_time = self.cleaned_data['scheduled_time']
        if scheduled_time < timezone.now() + timedelta(hours=48):
            raise forms.ValidationError("Bookings must be made at least 48 hours in advance.")
        return scheduled_time
