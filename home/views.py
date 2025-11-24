from django.shortcuts import render
from offers.models import Offer

def index(request):
    active_offer = Offer.objects.filter(active=True).first()
    context = {
        "active_offer": active_offer,
    }
    return render(request, 'home/index.html', context)