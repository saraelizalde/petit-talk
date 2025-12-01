from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, TeacherProfileEditForm, AdminTeacherEditForm
from .forms import AdminTeacherForm
from django.db import IntegrityError


@login_required
def profile_detail(request):
    """
    Display the profile of the currently logged-in user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders 'userprofile/profile_detail.html'
        with the profile context.
    """
    profile = request.user.profile
    return render(
        request,
        'userprofile/profile_detail.html',
        {'profile': profile}
    )


def public_profile(request, user_id):
    """
    Display a public profile by user ID.

    Args:
        request (HttpRequest): The request object.
        user_id (int): ID of the user whose profile is being viewed.

    Returns:
        HttpResponse: Renders 'userprofile/profile_detail.html'
        with the profile context.
    """
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request,
        'userprofile/profile_detail.html',
        {'profile': profile}
    )


@login_required
def profile_edit(request):
    """
    Allow the logged-in user to edit their profile.

    - Students use ProfileForm.
    - Teachers use TeacherProfileEditForm.

    Handles POST to save changes and GET to display the form.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders 'userprofile/profile_edit.html'
        with the form context.
    """
    profile = request.user.profile

    form_class = TeacherProfileEditForm if profile.is_teacher else ProfileForm

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your profile has been updated successfully!"
            )
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = form_class(instance=profile)
    return render(request, 'userprofile/profile_edit.html', {'form': form})


def teacher_profile(request, user_id):
    """
    Display a public teacher profile by user ID.

    Args:
        request (HttpRequest): The request object.
        user_id (int): ID of the teacher user.

    Returns:
        HttpResponse: Renders 'userprofile/teacher_profile.html'
        with profile context.
    """
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user, is_teacher=True)
    return render(
        request,
        'userprofile/teacher_profile.html',
        {'profile': profile}
    )


@login_required
def teacher_profile_edit(request):
    """
    Allow a logged-in teacher to edit their own profile.

    Redirects non-teachers to 'profile' with an error message.

    Handles POST to save changes and GET to display the form.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders 'userprofile/teacher_profile_edit.html'
        with form context.
    """
    profile = request.user.profile
    if not profile.is_teacher:
        messages.error(
            request,
            "You are not authorized to edit a teacher profile."
        )
        return redirect("profile")

    if request.method == 'POST':
        form = TeacherProfileEditForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your teacher profile has been updated successfully!"
            )
            return redirect('teacher_profile', user_id=request.user.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeacherProfileEditForm(instance=profile)

    return render(
        request,
        'userprofile/teacher_profile_edit.html',
        {'form': form}
    )


@staff_member_required
def admin_teachers(request):
    """
    Admin view to list all teachers and create new ones.

    Handles POST to create a teacher using AdminTeacherForm.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders 'userprofile/admin_teachers.html'
        with teachers list and form context.
    """
    teachers = Profile.objects.filter(is_teacher=True)

    if request.method == 'POST':
        form = AdminTeacherForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Teacher created successfully!")
                return redirect('admin_teachers')
            except IntegrityError:
                form.add_error(None, "Username or email already exists.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AdminTeacherForm()

    return render(request, 'userprofile/admin_teachers.html', {
        'teachers': teachers,
        'form': form
    })


@staff_member_required
def admin_edit_teacher(request, pk):
    """
    Admin view to edit an existing teacher's profile.

    Args:
        request (HttpRequest): The request object.
        pk (int): Primary key of the teacher's Profile.

    Returns:
        HttpResponse: Renders 'userprofile/admin_edit_teacher.html'
        with form and profile context.
    """
    profile = get_object_or_404(Profile, pk=pk, is_teacher=True)

    if request.method == 'POST':
        form = AdminTeacherEditForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated successfully!")
            return redirect('admin_teachers')
    else:
        form = AdminTeacherEditForm(instance=profile, initial={
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email': profile.user.email,
        })

    return render(request, 'userprofile/admin_edit_teacher.html', {
        'form': form,
        'profile': profile
    })


@staff_member_required
def admin_delete_teacher(request, pk):
    """
    Admin view to delete a teacher and their associated User account.

    Args:
        request (HttpRequest): The request object.
        pk (int): Primary key of the teacher's Profile.

    Returns:
        HttpResponse: Redirects to 'admin_teachers' with a success message.
    """
    profile = get_object_or_404(Profile, pk=pk, is_teacher=True)
    profile.user.delete()
    messages.success(request, "Teacher deleted successfully!")
    return redirect('admin_teachers')
