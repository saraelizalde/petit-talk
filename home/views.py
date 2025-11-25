from django.shortcuts import render
from offers.models import Offer
from userprofile.models import Profile

def index(request):
    active_offer = Offer.objects.filter(active=True).first()
    teachers = Profile.objects.filter(is_teacher=True)
    context = {
        "active_offer": active_offer,
        "teachers": teachers,
    }
    return render(request, 'home/index.html', context)