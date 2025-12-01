from django.shortcuts import render
from offers.models import Offer
from userprofile.models import Profile
from comments.models import Comment
from comments.forms import CommentForm
from django.http import HttpResponse
from django.template import loader


def index(request):
    """
    Render the homepage.

    Includes:
        - Active promotional offer (if any).
        - List of teacher profiles.
        - Approved comments for display.
        - Comment submission form.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered homepage template.
    """
    active_offer = Offer.objects.filter(active=True).first()
    teachers = Profile.objects.filter(is_teacher=True)
    comments = Comment.objects.filter(is_approved=True).order_by('-created_at')
    form = CommentForm()
    context = {
        "active_offer": active_offer,
        "teachers": teachers,
        "comments": comments,
        "form": form,
    }
    return render(request, 'home/index.html', context)


def contact(request):
    """
    Render the contact page.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered contact page.
    """
    return render(request, 'home/contact.html')


def robots_txt(request):
    """
    Serve the robots.txt file.

    This determines how search engine crawlers may interact
    with the site. The file is rendered as plain text.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The robots.txt file with text/plain content type.
    """
    template = loader.get_template("robots.txt")
    return HttpResponse(template.render(), content_type="text/plain")
