"""
RideEase Bike Rental System
Bookings App — Booking model with status tracking and cost auto-calculation.
"""

from django.db import models
from django.conf import settings
from apps.bikes.models import Bike


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected',  'Rejected'),
    ]

    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    # Booking dates
    pickup_date = models.DateField(verbose_name="Pickup Date")
    return_date = models.DateField(verbose_name="Return Date")
    pickup_location = models.CharField(max_length=200, default='Pune, Maharashtra')
    drop_location   = models.CharField(max_length=200, blank=True)

    # Pricing
    total_days    = models.PositiveIntegerField(default=1)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rate Per Day (INR)")
    helmet_deposit = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    total_cost    = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Cost (INR)")

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Extra info
    special_requests = models.TextField(blank=True)
    admin_notes      = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.pk} — {self.user.username} | {self.bike} | {self.pickup_date}"

    def save(self, *args, **kwargs):
        """Auto-calculate total days and cost before saving."""
        if self.pickup_date and self.return_date:
            delta = self.return_date - self.pickup_date
            self.total_days = delta.days if delta.days > 0 else 1
        if self.price_per_day:
            self.total_cost = (self.price_per_day * self.total_days) + self.helmet_deposit
        super().save(*args, **kwargs)

    def can_cancel(self):
        """Only pending or confirmed bookings can be cancelled."""
        return self.status in ['pending', 'confirmed']

    def get_status_badge_class(self):
        """Bootstrap badge class for the status pill."""
        badge_map = {
            'pending':   'bg-warning text-dark',
            'confirmed': 'bg-success',
            'completed': 'bg-secondary',
            'cancelled': 'bg-danger',
            'rejected':  'bg-dark',
        }
        return badge_map.get(self.status, 'bg-secondary')

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']


class Review(models.Model):
    """Star rating + comment left after a completed booking."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    booking    = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    user       = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='reviews')
    bike       = models.ForeignKey('bikes.Bike', on_delete=models.CASCADE, related_name='reviews')
    rating     = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.bike} — {self.rating}★"

    class Meta:
        ordering = ['-created_at']
