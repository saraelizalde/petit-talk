from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CommentForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Comment

def submit_comment(request):
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

            messages.success(request, "Your comment was submitted and is awaiting approval.")
            return redirect("home")

    return redirect("home")


@staff_member_required
def comments_dashboard(request):
    comments = Comment.objects.select_related("user", "profile").order_by("-created_at")
    return render(request, "comments/comments_dashboard.html", {"comments": comments})


@staff_member_required
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    messages.success(request, "Comment approved!")
    return redirect("comments_dashboard")


@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect("comments_dashboard")
