"""
RideEase Bike Rental System
Bookings App — Booking and review forms.
"""

from django import forms
from django.utils import timezone
from .models import Booking, Review


class BookingForm(forms.ModelForm):
    """Booking form — date picker + location fields."""

    class Meta:
        model  = Booking
        fields = ['pickup_date', 'return_date', 'pickup_location', 'drop_location', 'special_requests']
        widgets = {
            'pickup_date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control',
            }),
            'return_date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control',
            }),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control'}),
            'drop_location':   forms.TextInput(attrs={'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, bike=None, **kwargs):
        self.bike = bike
        super().__init__(*args, **kwargs)
        # Pre-fill pickup location from bike
        if bike:
            self.fields['pickup_location'].initial = bike.location

    def clean(self):
        cleaned = super().clean()
        pickup = cleaned.get('pickup_date')
        ret    = cleaned.get('return_date')
        today  = timezone.now().date()

        if pickup and pickup < today:
            self.add_error('pickup_date', "Pickup date cannot be in the past.")
        if pickup and ret:
            if ret <= pickup:
                self.add_error('return_date', "Return date must be after pickup date.")
        return cleaned


class ReviewForm(forms.ModelForm):
    """Review form after a completed booking."""

    class Meta:
        model  = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating':  forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience...'}),
        }
