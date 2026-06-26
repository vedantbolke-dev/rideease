"""
RideEase Bike Rental System — Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.bikes import views as bike_views

urlpatterns = [
    # Django built-in admin
    path('admin/', admin.site.urls),

    # Home page
    path('', bike_views.home, name='home'),

    # Static pages
    path('about/', bike_views.about, name='about'),
    path('contact/', bike_views.contact, name='contact'),

    # User auth and profile
    path('users/', include('apps.users.urls', namespace='users')),

    # Bike listings
    path('bikes/', include('apps.bikes.urls', namespace='bikes')),

    # Booking system
    path('bookings/', include('apps.bookings.urls', namespace='bookings')),

    # Admin dashboard
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),

    # Built-in password reset
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve uploaded media in development.
# Static assets are already served by django.contrib.staticfiles during
# development, so mapping /static/ to STATIC_ROOT here can hide source files
# from STATICFILES_DIRS and make the custom CSS/JS appear missing.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site branding
admin.site.site_header  = "RideEase Administration"
admin.site.site_title   = "RideEase Admin Portal"
admin.site.index_title  = "Welcome to RideEase Admin Panel"
