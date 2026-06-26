"""
RideEase Bike Rental System
Users App — Custom user model with profile fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extended user model with extra fields for the bike rental system.
    Inherits Django's AbstractUser so we get auth out of the box.
    """

    # Contact info
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address      = models.TextField(blank=True, null=True)
    city         = models.CharField(max_length=100, blank=True, null=True)
    state        = models.CharField(max_length=100, blank=True, null=True)
    pincode      = models.CharField(max_length=10, blank=True, null=True)

    # Profile photo
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    # Driving / riding license
    driving_license = models.CharField(max_length=50, blank=True, null=True)

    # Admin can block a user account
    is_blocked = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_active_bookings_count(self):
        """Returns count of active / pending bookings for this user."""
        return self.bookings.filter(
            status__in=['pending', 'confirmed']
        ).count()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
