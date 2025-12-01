from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.db import IntegrityError


class ProfileForm(forms.ModelForm):
    """
    Form for regular users to update their own profile.

    Fields:
    - profile_image: Optional user profile picture
    - bio: Short biography
    - language_level: User's language proficiency level
    - goals: User language learning goals
    - favorite_word/movie/book/song: Optional fun personal info
    """
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
            'goals': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-control'
                }
            ),
            'language_level': forms.Select(attrs={'class': 'form-select'}),
        }


class TeacherProfileEditForm(forms.ModelForm):
    """
    Form for teachers to edit their profile, including an optional intro video.

    Fields:
    - profile_image
    - bio
    - favorite_word/movie/book/song
    - intro_video: optional video upload
    """
    class Meta:
        model = Profile
        fields = [
            'profile_image',
            'bio',
            'favorite_word',
            'favorite_movie',
            'favorite_book',
            'favorite_song',
            'intro_video',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'intro_video': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
        }


class AdminTeacherForm(forms.ModelForm):
    """
    Admin form to create a new teacher user with profile.

    Extra fields:
    - username, email, password: For creating the User object
    - bio, profile_image: Optional profile info
    """
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 3}
    ), required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']

    def clean_username(self):
        """
        Ensure the username is unique.
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """
        Ensure the email is unique.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        """
        Create the User and Profile objects, mark the profile as teacher,
        and save to database if commit=True.

        Returns:
            Profile instance
        """
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        bio = self.cleaned_data.get('bio', '')
        profile_image = self.cleaned_data.get('profile_image', None)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        except IntegrityError:
            raise

        profile, created = Profile.objects.get_or_create(user=user)

        profile.is_teacher = True
        profile.is_student = False
        profile.bio = bio or profile.bio
        if profile_image:
            profile.profile_image = profile_image

        if commit:
            profile.save()

        return profile


class AdminTeacherEditForm(forms.ModelForm):
    """
    Admin form to edit an existing teacher's user and profile details.

    Extra fields:
    - first_name, last_name, email: for updating the User object
    - bio, profile_image: for updating the Profile object
    """
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']

    def save(self, commit=True):
        """
        Save updates to both the User and Profile models.

        Returns:
            Profile instance
        """
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile
