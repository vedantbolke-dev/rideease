"""
RideEase Bike Rental System
Bikes App — Public bike listing, detail, home, about, contact views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Avg

from .models import Bike, ContactMessage
from .forms import ContactForm
from apps.bookings.models import Review


def home(request):
    """Homepage with featured bikes and stats."""
    featured_bikes = Bike.objects.filter(is_featured=True, is_available=True)[:6]
    bikes_with_image = Bike.objects.filter(is_available=True, image__isnull=False).exclude(image='')
    hero_bike = bikes_with_image.order_by('-is_featured', '-created_at').first()
    total_bikes = Bike.objects.count()
    available_bikes = Bike.objects.filter(is_available=True).count()

    categories = [
        {'key': 'scooter', 'label': 'Scooters', 'icon': 'bi-scooter'},
        {'key': 'sport', 'label': 'Sport Bikes', 'icon': 'bi-lightning-charge'},
        {'key': 'cruiser', 'label': 'Cruisers', 'icon': 'bi-wind'},
        {'key': 'electric', 'label': 'Electric',    'icon': 'bi-ev-front'},
        {'key': 'mountain', 'label': 'Adventure', 'icon': 'bi-geo-alt'},
    ]

    return render(request, 'home.html', {
        'hero_bike': hero_bike,
        'featured_bikes': featured_bikes,
        'total_bikes': total_bikes,
        'available_bikes': available_bikes,
        'categories': categories,
    })


def bike_list(request):
    """Bike listing page with search and category filter."""
    bikes = Bike.objects.all()

    # Keyword search
    q = request.GET.get('q', '').strip()
    if q:
        bikes = bikes.filter(
            Q(name__icontains=q) | Q(brand__icontains=q) |
            Q(description__icontains=q) | Q(category__icontains=q)
        )

    # Category filter
    category = request.GET.get('category', '')
    if category:
        bikes = bikes.filter(category=category)

    # Availability filter
    availability = request.GET.get('availability', '')
    if availability == 'available':
        bikes = bikes.filter(is_available=True)
    elif availability == 'unavailable':
        bikes = bikes.filter(is_available=False)

    context = {
        'bikes':           bikes,
        'search_query':    q,
        'selected_cat':    category,
        'selected_avail':  availability,
        'category_choices': Bike.CATEGORY_CHOICES,
    }
    return render(request, 'bikes/bike_list.html', context)


def bike_detail(request, pk):
    """Bike detail page — shows full specs and recent reviews."""
    bike    = get_object_or_404(Bike, pk=pk)
    reviews = Review.objects.filter(bike=bike).select_related('user').order_by('-created_at')[:5]
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    context = {
        'bike':       bike,
        'reviews':    reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
    }
    return render(request, 'bikes/bike_detail.html', context)


def about(request):
    """About us page."""
    return render(request, 'about.html')


def contact(request):
    """Contact page — saves message to DB."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been received. We will get back to you shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
