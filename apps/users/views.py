"""
RideEase Bike Rental System
Users App — Views for auth, profile, and user dashboard.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from apps.bookings.models import Booking


def register(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to RideEase, {user.first_name}! Your account has been created.")
            return redirect('users:dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Login page with role-based redirect."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_blocked:
                messages.error(request, "Your account has been suspended. Please contact support.")
                return redirect('users:login')
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            if user.is_staff:
                return redirect('dashboard:home')
            return redirect('users:dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    """Log out and redirect to home."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def user_dashboard(request):
    """Customer dashboard — shows their bookings."""
    bookings = Booking.objects.filter(user=request.user).select_related('bike').order_by('-created_at')
    active   = bookings.filter(status__in=['pending', 'confirmed'])
    past     = bookings.filter(status__in=['completed', 'cancelled', 'rejected'])

    return render(request, 'users/dashboard.html', {
        'bookings':       bookings,
        'active_bookings': active,
        'past_bookings':   past,
        'total_bookings':  bookings.count(),
        'active_count':    active.count(),
        'completed_count': bookings.filter(status='completed').count(),
    })


@login_required
def user_profile(request):
    """View / update user profile."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('users:profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})
