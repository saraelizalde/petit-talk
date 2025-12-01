from django.contrib import admin
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Offer model.

    Features:
        - Displays key offer fields in the admin list view.
        - Provides filtering and search capabilities.
        - Includes bulk actions to activate or deactivate offers.
    """
    list_display = (
        "name",
        "discount_type",
        "discount_value",
        "active",
        "created_at",
        )
    list_filter = ("active", "discount_type", "created_at")
    search_fields = ("name", "description")
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        """
        Admin action to mark selected offers as active.

        Args:
            request: The current admin request.
            queryset: The selected Offer objects.

        Displays a confirmation message with the number of updated items.
        """
        updated = queryset.update(active=True)
        self.message_user(request, f"{updated} offer(s) marked as active.")
    make_active.short_description = "Mark selected offers as active"

    def make_inactive(self, request, queryset):
        """
        Admin action to mark selected offers as inactive.

        Args:
            request: The current admin request.
            queryset: The selected Offer objects.

        Displays a confirmation message with the number of updated items.
        """
        updated = queryset.update(active=False)
        self.message_user(request, f"{updated} offer(s) marked as inactive.")
    make_inactive.short_description = "Mark selected offers as inactive"
