from django.shortcuts import render
from offers.models import Offer
from userprofile.models import Profile
from comments.models import Comment
from comments.forms import CommentForm

def index(request):
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