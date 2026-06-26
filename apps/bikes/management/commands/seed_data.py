"""
RideEase Bike Rental System
Management Command: seed_data
Creates sample admin, users, and bikes for demo purposes.
Run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.bikes.models import Bike

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample bikes and user accounts'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('\n=== RideEase Seed Data ===\n'))

        # ── Create Admin ──────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@rideease.com',
                password='Admin@123',
                first_name='Admin',
                last_name='RideEase',
                is_staff=True,
            )
            self.stdout.write(self.style.SUCCESS('  [+] Admin user created: admin / Admin@123'))
        else:
            self.stdout.write('  [=] Admin already exists')

        # ── Create Sample Customers ────────────────────────────────────
        sample_users = [
            {'username': 'rahul_sharma', 'first_name': 'Rahul', 'last_name': 'Sharma',
             'email': 'rahul@gmail.com', 'phone_number': '9876543210',
             'city': 'Pune', 'state': 'Maharashtra', 'driving_license': 'MH12-2020-1234'},
            {'username': 'priya_patil', 'first_name': 'Priya', 'last_name': 'Patil',
             'email': 'priya@gmail.com', 'phone_number': '9823456789',
             'city': 'Pune', 'state': 'Maharashtra', 'driving_license': 'MH14-2019-5678'},
            {'username': 'amit_desai', 'first_name': 'Amit', 'last_name': 'Desai',
             'email': 'amit@gmail.com', 'phone_number': '9765432109',
             'city': 'Nashik', 'state': 'Maharashtra', 'driving_license': 'MH15-2021-9012'},
        ]
        for data in sample_users:
            uname = data.pop('username')
            email = data.get('email')
            if not User.objects.filter(username=uname).exists():
                User.objects.create_user(username=uname, password='User@123', **data)
                self.stdout.write(self.style.SUCCESS(f'  [+] User created: {uname} / User@123'))
            else:
                self.stdout.write(f'  [=] User already exists: {uname}')

        # ── Create Sample Bikes ────────────────────────────────────────
        bikes_data = [
            # Scooters
            {'brand': 'Honda', 'name': 'Activa 6G', 'model_year': 2023, 'category': 'scooter',
             'fuel_type': 'petrol', 'transmission': 'automatic', 'engine_cc': '110cc',
             'mileage': '60 km/l', 'color': 'Pearl Sparkling Blue', 'top_speed': '95 km/h',
             'price_per_day': 299, 'helmet_deposit': 300,
             'features': 'USB Charging, LED Headlight, Digital Console, Under-seat Storage',
             'description': 'India\'s most trusted scooter. Ideal for city commuting.',
             'is_available': True, 'is_featured': True, 'location': 'Pune, Maharashtra'},

            {'brand': 'TVS', 'name': 'Jupiter Classic', 'model_year': 2023, 'category': 'scooter',
             'fuel_type': 'petrol', 'transmission': 'automatic', 'engine_cc': '110cc',
             'mileage': '62 km/l', 'color': 'Coral Red', 'top_speed': '90 km/h',
             'price_per_day': 279, 'helmet_deposit': 300,
             'features': 'Mobile Connectivity, Pass Light, Econometer',
             'description': 'Feature-packed scooter with a classic look.',
             'is_available': True, 'is_featured': False, 'location': 'Pune, Maharashtra'},

            # Sport Bikes
            {'brand': 'Bajaj', 'name': 'Pulsar NS200', 'model_year': 2023, 'category': 'sport',
             'fuel_type': 'petrol', 'transmission': 'manual', 'engine_cc': '199.5cc',
             'mileage': '40 km/l', 'color': 'Pewter Grey', 'top_speed': '136 km/h',
             'price_per_day': 499, 'helmet_deposit': 500,
             'features': 'Liquid Cooled, Perimeter Frame, Clip-on Handlebars, USD Forks',
             'description': 'High-performance naked sport bike for thrill seekers.',
             'is_available': True, 'is_featured': True, 'location': 'Pune, Maharashtra'},

            {'brand': 'KTM', 'name': 'Duke 200', 'model_year': 2022, 'category': 'sport',
             'fuel_type': 'petrol', 'transmission': 'manual', 'engine_cc': '199.5cc',
             'mileage': '35 km/l', 'color': 'Orange', 'top_speed': '135 km/h',
             'price_per_day': 549, 'helmet_deposit': 500,
             'features': 'WP Suspension, Slipper Clutch, LED Lights, TFT Display',
             'description': 'The legendary street fighter. Born to be wild.',
             'is_available': True, 'is_featured': True, 'location': 'Pune, Maharashtra'},

            # Cruisers
            {'brand': 'Royal Enfield', 'name': 'Classic 350', 'model_year': 2023, 'category': 'cruiser',
             'fuel_type': 'petrol', 'transmission': 'manual', 'engine_cc': '349cc',
             'mileage': '36 km/l', 'color': 'Halcyon Black', 'top_speed': '120 km/h',
             'price_per_day': 799, 'helmet_deposit': 500,
             'features': 'Tripper Navigation, Dual Channel ABS, Chrome Accents',
             'description': 'The timeless classic. Perfect for highway cruising.',
             'is_available': True, 'is_featured': True, 'location': 'Pune, Maharashtra'},

            {'brand': 'Royal Enfield', 'name': 'Meteor 350', 'model_year': 2023, 'category': 'cruiser',
             'fuel_type': 'petrol', 'transmission': 'manual', 'engine_cc': '349cc',
             'mileage': '36 km/l', 'color': 'Fireball', 'top_speed': '130 km/h',
             'price_per_day': 849, 'helmet_deposit': 500,
             'features': 'Tripper Pod, Bluetooth, ABS, Semi-digital Console',
             'description': 'Modern cruiser with connected features for the long road.',
             'is_available': False, 'is_featured': True, 'location': 'Pune, Maharashtra'},

            # Electric
            {'brand': 'Ola', 'name': 'S1 Pro', 'model_year': 2023, 'category': 'electric',
             'fuel_type': 'electric', 'transmission': 'automatic', 'engine_cc': 'Electric Motor',
             'mileage': '195 km/charge', 'color': 'Jet Black', 'top_speed': '120 km/h',
             'price_per_day': 449, 'helmet_deposit': 300,
             'features': '4G Connected, Proximity Unlock, Hill Hold, Reverse Mode, 75L Boot',
             'description': 'Smart, connected electric scooter with impressive range.',
             'is_available': True, 'is_featured': True, 'location': 'Pune, Maharashtra'},

            {'brand': 'Ather', 'name': '450X Gen 3', 'model_year': 2023, 'category': 'electric',
             'fuel_type': 'electric', 'transmission': 'automatic', 'engine_cc': 'Electric Motor',
             'mileage': '146 km/charge', 'color': 'Space Grey', 'top_speed': '90 km/h',
             'price_per_day': 399, 'helmet_deposit': 300,
             'features': 'Touchscreen Dashboard, OTA Updates, GPS Navigation, Fast Charging',
             'description': 'Premium electric scooter with smart technology built in.',
             'is_available': True, 'is_featured': False, 'location': 'Pune, Maharashtra'},

            # Adventure / Mountain
            {'brand': 'Royal Enfield', 'name': 'Himalayan 450', 'model_year': 2024, 'category': 'mountain',
             'fuel_type': 'petrol', 'transmission': 'manual', 'engine_cc': '452cc',
             'mileage': '30 km/l', 'color': 'Slate Himalayan Salt', 'top_speed': '150 km/h',
             'price_per_day': 1099, 'helmet_deposit': 500,
             'features': 'Google Maps Navigation, Long Travel Suspension, Alloy Wheels, ABS',
             'description': 'Built for the mountains. Perfect for Sahyadri trips from Pune.',
             'is_available': True, 'is_featured': True, 'location': 'Pune, Maharashtra'},

            {'brand': 'Hero', 'name': 'Xpulse 200 4V', 'model_year': 2023, 'category': 'mountain',
             'fuel_type': 'petrol', 'transmission': 'manual', 'engine_cc': '199.6cc',
             'mileage': '37 km/l', 'color': 'Typhoon Blue', 'top_speed': '115 km/h',
             'price_per_day': 599, 'helmet_deposit': 500,
             'features': 'Long Suspension Travel, 21" Front Wheel, Rally Kit Ready, USB Charger',
             'description': 'Affordable adventure bike ready for off-road exploration.',
             'is_available': True, 'is_featured': False, 'location': 'Pune, Maharashtra'},
        ]

        created_count = 0
        for b in bikes_data:
            if not Bike.objects.filter(brand=b['brand'], name=b['name']).exists():
                Bike.objects.create(**b)
                self.stdout.write(self.style.SUCCESS(f"  [+] Bike added: {b['brand']} {b['name']}"))
                created_count += 1
            else:
                self.stdout.write(f"  [=] Bike exists: {b['brand']} {b['name']}")

        self.stdout.write('\n' + self.style.SUCCESS(
            f'Seed complete! {created_count} new bikes added.\n'
            f'Login credentials:\n'
            f'  Admin:    admin / Admin@123\n'
            f'  Customer: rahul_sharma / User@123\n'
        ))
