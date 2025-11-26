from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CommentForm

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
