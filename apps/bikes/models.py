"""
RideEase Bike Rental System
Bikes App — Bike listings, categories, and availability tracking.
"""

from django.db import models


class Bike(models.Model):
    CATEGORY_CHOICES = [
        ('scooter',  'Scooter'),
        ('sport',    'Sport Bike'),
        ('cruiser',  'Cruiser'),
        ('electric', 'Electric'),
        ('mountain', 'Mountain / Adventure'),
    ]
    FUEL_CHOICES = [
        ('petrol',   'Petrol'),
        ('electric', 'Electric'),
        ('hybrid',   'Hybrid'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual',    'Manual'),
        ('automatic', 'Automatic / CVT'),
    ]

    name       = models.CharField(max_length=100, verbose_name="Bike Name")
    brand      = models.CharField(max_length=100, verbose_name="Brand")
    model_year = models.PositiveIntegerField(verbose_name="Model Year")
    category   = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='scooter')
    fuel_type  = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual')
    engine_cc  = models.CharField(max_length=30, blank=True, help_text="e.g., 350cc")
    mileage    = models.CharField(max_length=30, blank=True, help_text="e.g., 45 km/l")
    color      = models.CharField(max_length=50, blank=True)
    top_speed  = models.CharField(max_length=30, blank=True, help_text="e.g., 120 km/h")

    price_per_day  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price Per Day (INR)")
    helmet_deposit = models.DecimalField(max_digits=8, decimal_places=2, default=500.00,
                                          verbose_name="Helmet Deposit (INR)")

    description = models.TextField(blank=True)
    features    = models.TextField(blank=True, help_text="Comma-separated features")
    image       = models.ImageField(upload_to='bikes/', blank=True, null=True)

    is_available = models.BooleanField(default=True)
    is_featured  = models.BooleanField(default=False)
    location     = models.CharField(max_length=200, default='Pune, Maharashtra')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.name} ({self.model_year})"

    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split(',')]
        return []

    class Meta:
        verbose_name = "Bike"
        verbose_name_plural = "Bikes"
        ordering = ['-created_at']


class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general',   'General Inquiry'),
        ('booking',   'Booking Help'),
        ('complaint', 'Complaint'),
        ('other',     'Other'),
    ]
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=15, blank=True)
    subject    = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.created_at.strftime('%d %b %Y')})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
