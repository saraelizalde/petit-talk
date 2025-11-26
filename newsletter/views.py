from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import NewsletterForm
from .models import Newsletter

def subscribe(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data.get('first_name', '')

            subscriber, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name}
            )

            if not created:
                if not subscriber.is_active:
                    subscriber.is_active = True
                    subscriber.first_name = first_name
                    subscriber.save()
                    messages.success(request, "Welcome back! You have been resubscribed.")
                else:
                    messages.warning(request, "This email is already subscribed.")
                return redirect(request.META.get('HTTP_REFERER', 'index'))

            messages.success(request, "Successfully subscribed to the newsletter!")
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        messages.error(request, "Please enter a valid email.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    return redirect('index')

def unsubscribe(request, email):
    try:
        subscriber = Newsletter.objects.get(email=email)
        subscriber.is_active = False
        subscriber.save()
        messages.success(request, "You have been unsubscribed.")
    except Newsletter.DoesNotExist:
        messages.error(request, "Subscription not found.")

    return redirect('index')
