from django.shortcuts import render
from .models import Offer

def active_offers(request):
    """Display all active offers (to be used in index.html)."""
    offers = Offer.objects.filter(active=True)
    return render(request, "offers/active_offers.html", {"offers": offers})
