"""
RideEase Bike Rental System
Users App — Forms for registration, login, and profile update.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    """Registration form — collects basic user details."""
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model  = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'password1', 'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class UserLoginForm(AuthenticationForm):
    """Login form with Bootstrap styling."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })


class UserProfileForm(forms.ModelForm):
    """Profile update form."""

    class Meta:
        model  = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'address', 'city', 'state', 'pincode',
            'driving_license', 'profile_picture',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['profile_picture'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*',
        })
