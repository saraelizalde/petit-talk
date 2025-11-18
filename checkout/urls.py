from django.urls import path
from . import views, webhooks

urlpatterns = [
    path("create-checkout/<int:order_id>/", views.create_checkout_session, name="create_checkout_session"),
    path("success/", views.success, name="checkout_success"),
    path("error/", views.error, name="checkout_error"),
    path("webhook/", webhooks.stripe_webhook, name="stripe_webhook"),
]
