from django import forms
from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    """
    Form for users to subscribe to the site's newsletter.

    This form collects:
        - Email address (required)
        - First name (optional)

    The form uses Bootstrap-friendly widgets for styling and
    integrates with the Newsletter model for storage.
    """
    class Meta:
        model = Newsletter
        fields = ['email', 'first_name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name (optional)'
            }),
        }
