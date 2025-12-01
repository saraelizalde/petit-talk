from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CommentForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Comment


def submit_comment(request):
    """
    Handle submission of a new user comment.

    - Only authenticated users can submit comments.
    - The comment is saved with `is_approved=False` to await moderation.
    - On successful submission, the user is redirected to the home page
      with a success message.
    - If the user is not authenticated or the form is invalid,
      they are redirected to the home page with an error message.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponseRedirect: Redirects the user to the home page.
    """
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect("home")

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.is_approved = False
            new_comment.save()

            messages.success(
                request,
                "Your comment was submitted and is awaiting approval."
            )
            return redirect("home")

    return redirect("home")


@staff_member_required
def comments_dashboard(request):
    """
    Display the admin dashboard listing all comments.

    - Accessible only to staff via the `staff_member_required` decorator.
    - Shows all comments ordered by newest first.
    - Useful for approving or deleting comments.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Renders the comments dashboard template.
    """
    comments = Comment.objects.select_related(
        "user",
        "profile"
    ).order_by("-created_at")

    return render(
        request,
        "comments/comments_dashboard.html",
        {"comments": comments}
    )


@staff_member_required
def approve_comment(request, comment_id):
    """
    Approve a pending comment.

    - Marks the selected comment as approved.
    - Available only to staff users.
    - Displays a success message upon approval.

    Args:
        request (HttpRequest): The incoming HTTP request.
        comment_id (int): The ID of the comment to approve.

    Returns:
        HttpResponseRedirect: Redirects back to the comments dashboard.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    messages.success(request, "Comment approved!")
    return redirect("comments_dashboard")


@staff_member_required
def delete_comment(request, comment_id):
    """
    Delete an existing comment.

    - Removes the specified comment from the database.
    - Accessible only to staff members.
    - Success message is shown after deletion.

    Args:
        request (HttpRequest): The incoming HTTP request.
        comment_id (int): The ID of the comment to delete.

    Returns:
        HttpResponseRedirect: Redirects to the comments dashboard.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect("comments_dashboard")
