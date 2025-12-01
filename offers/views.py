from django.shortcuts import render, redirect, get_object_or_404
from .models import Offer
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OfferForm


def active_offers(request):
    """
    Display all active offers
    """
    offers = Offer.objects.filter(active=True)
    return render(request, "offers/active_offers.html", {"offers": offers})


@staff_member_required
def admin_offers(request):
    """
    Admin dashboard to view and create offers.

    GET:
        - Displays all offers and an empty OfferForm.

    POST:
        - Validates and saves a new offer.
        - Redirects back to the admin offers page.

    Only staff members can access this view.
    """
    offers = Offer.objects.all()

    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('offers:admin_offers')
    else:
        form = OfferForm()

    return render(
        request,
        'offers/admin_offers.html',
        {
            'offers': offers,
            'form': form
        }
    )


@staff_member_required
def admin_edit_offer(request, pk):
    """
    Edit or delete an existing offer.

    GET:
        - Pre-fills the form with the existing offer.

    POST:
        If "delete_offer" is submitted:
            - Deletes the selected offer.
        Otherwise:
            - Updates the offer with form data.

    Args:
        pk (int): Primary key of the offer being modified.

    Returns:
        Redirects back to the offer admin dashboard after saving.
    """
    offer = get_object_or_404(Offer, pk=pk)

    if request.method == "POST":
        if "delete_offer" in request.POST:
            offer.delete()
            return redirect('offers:admin_offers')
        else:
            form = OfferForm(request.POST, request.FILES, instance=offer)
            if form.is_valid():
                form.save()
                return redirect('offers:admin_offers')
    else:
        form = OfferForm(instance=offer)

    return render(
        request,
        'offers/admin_edit_offer.html',
        {
            'form': form,
            'offer': offer
        }
    )
