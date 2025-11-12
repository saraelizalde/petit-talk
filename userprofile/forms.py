from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_image',
            'bio',
            'language_level',
            'goals',
            'favorite_word',
            'favorite_movie',
            'favorite_book',
            'favorite_song',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'goals': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'language_level': forms.Select(attrs={'class': 'form-select'}),
        }

class TeacherProfileForm(ProfileForm):
    class Meta(ProfileForm.Meta):
        fields = ProfileForm.Meta.fields + ['intro_video']
        widgets = {**ProfileForm.Meta.widgets,
                   'intro_video': forms.ClearableFileInput(attrs={'class': 'form-control'})}
