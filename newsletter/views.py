from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import NewsletterForm
from .models import Newsletter
from django.contrib.admin.views.decorators import staff_member_required


def subscribe(request):
    """
    Handle newsletter subscription requests.

    POST:
        - Validates the subscription form.
        - Creates a new subscriber or reactivates an inactive one.
        - Returns success, warning, or error messages accordingly.
        - Redirects back to the referring page (or home as fallback).

    GET:
        Redirects to the home page since direct form display is
        handled elsewhere.

    Returns:
        HttpResponseRedirect to the previous page or the home page.
    """
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
                    messages.success(
                        request,
                        "Welcome back! You have been resubscribed."
                    )
                else:
                    messages.warning(
                        request,
                        "This email is already subscribed."
                    )
                return redirect(request.META.get('HTTP_REFERER', 'index'))

            messages.success(
                request,
                "Successfully subscribed to the newsletter!"
            )
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        messages.error(request, "Please enter a valid email.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    return redirect('index')


def unsubscribe(request, email):
    """
    Unsubscribe a user based on their email address.

    Instead of deleting the subscriber, this view sets `is_active=False`
    to allow reactivation without losing data.

    Args:
        email (str): Email of the subscriber to deactivate.

    Returns:
        Redirect to the newsletter admin dashboard with a success or
        error message.
    """
    try:
        subscriber = Newsletter.objects.get(email=email)
        subscriber.is_active = False
        subscriber.save()
        messages.success(request, "You have been unsubscribed.")
    except Newsletter.DoesNotExist:
        messages.error(request, "Subscription not found.")

    return redirect('newsletter:admin_dashboard')


@staff_member_required
def admin_dashboard(request):
    """
    Display the newsletter admin dashboard.

    Shows:
        - All subscribers (active and inactive)
        - Ordered by newest subscription first

    Access:
        Staff-only.

    Returns:
        Rendered admin dashboard template with subscriber list.
    """
    subscribers = Newsletter.objects.all().order_by("-created_at")
    return render(request, "newsletter/admin_newsletter_dashboard.html", {
        "subscribers": subscribers
    })
