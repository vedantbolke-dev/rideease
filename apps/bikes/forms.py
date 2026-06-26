"""
RideEase Bike Rental System
Bikes App — Admin bike form and contact form.
"""

from django import forms
from .models import Bike, ContactMessage


class BikeAdminForm(forms.ModelForm):
    """Admin form for adding / editing a bike listing."""

    class Meta:
        model  = Bike
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class ContactForm(forms.ModelForm):
    """Public contact form."""

    class Meta:
        model  = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
