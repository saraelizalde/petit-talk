from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'total_eur', 'paid', 'created_at')
    list_filter = ('paid', 'created_at')
    search_fields = ('student__username', 'id')
