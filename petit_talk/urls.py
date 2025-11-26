from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path("bookings/", include("bookings.urls")),
    path("checkout/", include("checkout.urls")),
    path("newsletter/", include("newsletter.urls")),
    path("offers/", include("offers.urls", namespace="offers")),
    path('order/', include('order.urls')),
    path('profile/', include('userprofile.urls')),
    path('', include('home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)