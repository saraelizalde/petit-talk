from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, TeacherProfileEditForm

@login_required
def profile_detail(request):
    profile = request.user.profile
    return render(request, 'userprofile/profile_detail.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile = request.user.profile
    
    form_class = TeacherProfileEditForm if profile.is_teacher else ProfileForm
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = form_class(instance=profile)
    return render(request, 'userprofile/profile_edit.html', {'form': form})


def teacher_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user, is_teacher=True)
    return render(request, 'userprofile/teacher_profile.html', {'profile': profile})

@login_required
def teacher_profile_edit(request):
    profile = request.user.profile
    if not profile.is_teacher:
        messages.error(request, "You are not authorized to edit a teacher profile.")
        return redirect("profile")

    if request.method == 'POST':
        form = TeacherProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your teacher profile has been updated successfully!")
            return redirect('teacher_profile', user_id=request.user.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeacherProfileEditForm(instance=profile)

    return render(request, 'userprofile/teacher_profile_edit.html', {'form': form})