from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, CLASS_PRICE_EUR
from bookings.models import Booking
from django.db import transaction

@login_required
def view_bag(request):
    """Show student's unpaid / pending bookings."""
    order = Order.get_or_create_basket(request.user)
    bag_bookings = Booking.objects.filter(student=request.user, status='PENDING')
    order.bookings.set(bag_bookings)
    if not bag_bookings.exists():
        order.offer = None
        order.subtotal = 0
        order.total_eur = 0
        order.save(update_fields=['offer', 'subtotal', 'total_eur'])
        discount = 0
    else:
        order.auto_apply_offer()
        order.refresh_total()
        discount = order.subtotal - order.total_eur

    return render(request, "order/bag.html", {
        "order": order,
        "bookings": bag_bookings,
        "price_per": CLASS_PRICE_EUR,
        "total": order.total_eur,
        "discount": discount,
    })

@login_required
def remove_from_bag(request, booking_id):
    """Remove booking from bag."""
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    if booking.status != 'PENDING':
        messages.error(request, "Only unpaid/pending bookings can be removed from bag.")
        return redirect('view_bag')

    booking.delete()

    messages.success(request, "Booking removed from your bag.")
    return redirect('view_bag')

#@login_required
#@transaction.atomic
#def create_order(request):
    #bag_bookings = Booking.objects.filter(student=request.user, status='PENDING')
    #if not bag_bookings.exists():
        #messages.error(request, "There are no items in your bag.")
        #return redirect('view_bag')

    #order = Order.objects.create(student=request.user)
    #order.bookings.set(bag_bookings)
    #order.calculate_total()
    #order.save()

    #return redirect("create_checkout_session", order_id=order.id)


