"""
RideEase Bike Rental System
Dashboard App — Admin analytics, bike CRUD, user management, booking management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from functools import wraps
import json, csv, io

from apps.bikes.models import Bike, ContactMessage
from apps.bikes.forms import BikeAdminForm
from apps.bookings.models import Booking

User = get_user_model()


# ── Access control ─────────────────────────────────────────────────────────

def admin_required(view_func):
    """Decorator: must be logged in AND staff."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.conf import settings
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Helpers ────────────────────────────────────────────────────────────────

def sync_bike_availability():
    """
    Auto-update bike availability based on active bookings.
    Called each time the admin dashboard loads so stats stay accurate.
    """
    from datetime import date
    today = date.today()

    # Auto-complete bookings whose return date has passed
    expired = Booking.objects.filter(
        status__in=['confirmed', 'pending'],
        return_date__lt=today
    )
    for b in expired:
        b.status = 'completed'
        b.save()

    # Bikes still on active future bookings
    rented_ids = set(
        Booking.objects.filter(
            status__in=['confirmed', 'pending'],
            return_date__gte=today
        ).values_list('bike_id', flat=True)
    )
    Bike.objects.filter(id__in=rented_ids).update(is_available=False)
    Bike.objects.exclude(id__in=rented_ids).update(is_available=True)


# ── Admin Dashboard ────────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    sync_bike_availability()

    total_bikes    = Bike.objects.count()
    available_bikes = Bike.objects.filter(is_available=True).count()
    rented_bikes   = total_bikes - available_bikes
    total_users    = User.objects.filter(is_staff=False).count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_revenue  = Booking.objects.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(total=Sum('total_cost'))['total'] or 0

    recent_bookings = Booking.objects.select_related('user', 'bike').order_by('-created_at')[:8]

    cat_data = (
        Bike.objects
        .values('category')
        .annotate(count=Count('id'))
        .order_by('category')
    )
    cat_labels = [Bike(category=c['category']).get_category_display() for c in cat_data]
    cat_counts = [c['count'] for c in cat_data]

    six_months_ago = timezone.now() - timezone.timedelta(days=180)
    monthly_data = (
        Booking.objects
        .filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    monthly_labels = [d['month'].strftime('%b %Y') for d in monthly_data]
    monthly_counts = [d['count'] for d in monthly_data]

    status_counts = {
        'Pending':   Booking.objects.filter(status='pending').count(),
        'Confirmed': Booking.objects.filter(status='confirmed').count(),
        'Completed': Booking.objects.filter(status='completed').count(),
        'Cancelled': Booking.objects.filter(status='cancelled').count(),
        'Rejected':  Booking.objects.filter(status='rejected').count(),
    }

    return render(request, 'dashboard/admin_dashboard.html', {
        'total_bikes':      total_bikes,
        'available_bikes':  available_bikes,
        'rented_bikes':     rented_bikes,
        'total_users':      total_users,
        'total_bookings':   total_bookings,
        'pending_bookings': pending_bookings,
        'total_revenue':    total_revenue,
        'recent_bookings':  recent_bookings,
        'cat_labels':       json.dumps(cat_labels),
        'cat_counts':       json.dumps(cat_counts),
        'monthly_labels':   json.dumps(monthly_labels),
        'monthly_counts':   json.dumps(monthly_counts),
        'status_labels':    json.dumps(list(status_counts.keys())),
        'status_counts':    json.dumps(list(status_counts.values())),
    })


# ── Bike Management ────────────────────────────────────────────────────────

@admin_required
def admin_bikes(request):
    """List all bikes with search."""
    q = request.GET.get('q', '').strip()
    bikes = Bike.objects.all()
    if q:
        bikes = bikes.filter(Q(name__icontains=q) | Q(brand__icontains=q))
    return render(request, 'dashboard/admin_bikes.html', {'bikes': bikes, 'q': q})


@admin_required
def admin_bike_add(request):
    """Add a new bike."""
    if request.method == 'POST':
        form = BikeAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Bike added successfully!")
            return redirect('dashboard:bikes')
        messages.error(request, "Please fix the errors below.")
    else:
        form = BikeAdminForm()
    return render(request, 'dashboard/admin_bike_form.html', {'form': form, 'action': 'Add'})


@admin_required
def admin_bike_edit(request, pk):
    """Edit an existing bike."""
    bike = get_object_or_404(Bike, pk=pk)
    if request.method == 'POST':
        form = BikeAdminForm(request.POST, request.FILES, instance=bike)
        if form.is_valid():
            form.save()
            messages.success(request, f"{bike.brand} {bike.name} updated successfully!")
            return redirect('dashboard:bikes')
        messages.error(request, "Please fix the errors below.")
    else:
        form = BikeAdminForm(instance=bike)
    return render(request, 'dashboard/admin_bike_form.html', {'form': form, 'bike': bike, 'action': 'Edit'})


@admin_required
def admin_bike_delete(request, pk):
    """Delete a bike."""
    bike = get_object_or_404(Bike, pk=pk)
    if request.method == 'POST':
        name = str(bike)
        bike.delete()
        messages.success(request, f"{name} has been removed.")
        return redirect('dashboard:bikes')
    return render(request, 'dashboard/admin_bike_delete.html', {'bike': bike})


@admin_required
def admin_bike_toggle(request, pk):
    """Quick toggle availability from the bike list."""
    bike = get_object_or_404(Bike, pk=pk)
    bike.is_available = not bike.is_available
    bike.save()
    state = "available" if bike.is_available else "unavailable"
    messages.success(request, f"{bike.brand} {bike.name} marked as {state}.")
    return redirect('dashboard:bikes')


# ── Booking Management ────────────────────────────────────────────────────

@admin_required
def admin_bookings(request):
    """List all bookings with status filter."""
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.select_related('user', 'bike').order_by('-created_at')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'dashboard/admin_bookings.html', {
        'bookings':       bookings,
        'status_filter':  status_filter,
        'status_choices': Booking.STATUS_CHOICES,
    })


@admin_required
def admin_booking_update_status(request, pk):
    """Update the status of a booking (confirm / reject / complete)."""
    booking    = get_object_or_404(Booking, pk=pk)
    new_status = request.POST.get('status')
    valid = [s[0] for s in Booking.STATUS_CHOICES]

    if new_status in valid:
        old_status  = booking.status
        booking.status = new_status
        booking.save()

        if new_status in ['rejected', 'cancelled', 'completed']:
            booking.bike.is_available = True
            booking.bike.save()
        elif new_status == 'confirmed':
            booking.bike.is_available = False
            booking.bike.save()

        messages.success(request, f"Booking #{booking.pk} status updated to {booking.get_status_display()}.")
    else:
        messages.error(request, "Invalid status value.")

    return redirect('dashboard:bookings')


# ── User Management ────────────────────────────────────────────────────────

@admin_required
def admin_users(request):
    """List all non-staff users."""
    q = request.GET.get('q', '').strip()
    users = User.objects.filter(is_staff=False).order_by('-date_joined')
    if q:
        users = users.filter(
            Q(username__icontains=q) | Q(email__icontains=q) |
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
    return render(request, 'dashboard/admin_users.html', {'users': users, 'q': q})


@admin_required
def admin_user_toggle_block(request, pk):
    """Block or unblock a user account."""
    user = get_object_or_404(User, pk=pk)
    if user.is_staff:
        messages.error(request, "Admin accounts cannot be blocked.")
        return redirect('dashboard:users')
    user.is_blocked = not user.is_blocked
    user.save()
    state = "blocked" if user.is_blocked else "unblocked"
    messages.success(request, f"User {user.username} has been {state}.")
    return redirect('dashboard:users')


@admin_required
def admin_user_delete(request, pk):
    """Delete a user account."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user.is_staff:
            messages.error(request, "Admin accounts cannot be deleted from here.")
            return redirect('dashboard:users')
        user.delete()
        messages.success(request, "User account deleted.")
        return redirect('dashboard:users')
    return render(request, 'dashboard/admin_user_delete.html', {'target_user': user})


# ── Contact Messages ───────────────────────────────────────────────────────

@admin_required
def admin_contact_messages(request):
    """View all contact messages."""
    msgs = ContactMessage.objects.all().order_by('-created_at')
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    return render(request, 'dashboard/admin_contact_messages.html', {'contact_msgs': msgs})


# ── CSV Export ─────────────────────────────────────────────────────────────

@admin_required
def export_bikes_csv(request):
    """Export full bike list as CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rideease_bikes.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Brand', 'Name', 'Year', 'Category', 'Fuel', 'Engine CC',
                     'Mileage', 'Price/Day (INR)', 'Helmet Deposit (INR)', 'Available', 'Location'])
    for b in Bike.objects.all():
        writer.writerow([
            b.pk, b.brand, b.name, b.model_year, b.get_category_display(),
            b.get_fuel_type_display(), b.engine_cc, b.mileage,
            b.price_per_day, b.helmet_deposit, 'Yes' if b.is_available else 'No', b.location,
        ])
    return response


@admin_required
def export_bookings_csv(request):
    """Export all bookings as CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rideease_bookings.csv"'
    writer = csv.writer(response)
    writer.writerow(['Booking ID', 'Customer', 'Email', 'Bike', 'Pickup Date',
                     'Return Date', 'Days', 'Rate/Day (INR)', 'Helmet Deposit (INR)',
                     'Total (INR)', 'Status', 'Booked On'])
    for b in Booking.objects.select_related('user', 'bike').all():
        writer.writerow([
            b.pk, b.user.get_full_name() or b.user.username,
            b.user.email, str(b.bike), b.pickup_date, b.return_date,
            b.total_days, b.price_per_day, b.helmet_deposit,
            b.total_cost, b.get_status_display(),
            b.created_at.strftime('%d %b %Y'),
        ])
    return response


@admin_required
def export_users_csv(request):
    """Export user list as CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rideease_users.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Username', 'Full Name', 'Email', 'Phone', 'City', 'License', 'Joined'])
    for u in User.objects.filter(is_staff=False):
        writer.writerow([
            u.pk, u.username, u.get_full_name(), u.email,
            u.phone_number or '', u.city or '', u.driving_license or '',
            u.date_joined.strftime('%d %b %Y'),
        ])
    return response


# ── PDF Export ─────────────────────────────────────────────────────────────

@admin_required
def export_bikes_pdf(request):
    """Export full bike list as PDF."""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                               rightMargin=1.5*cm, leftMargin=1.5*cm,
                               topMargin=2*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    orange = colors.HexColor('#F97316')

    h_style = ParagraphStyle('H', fontSize=16, textColor=orange,
                             fontName='Helvetica-Bold', alignment=TA_CENTER)
    s_style = ParagraphStyle('S', fontSize=9, alignment=TA_CENTER,
                             parent=styles['Normal'])
    elements = []
    elements.append(Paragraph("RideEase Bike Rental System", h_style))
    elements.append(Paragraph("Complete Bike Inventory Report", s_style))
    elements.append(Paragraph(f"Generated: {timezone.now().strftime('%d %B %Y')}", s_style))
    elements.append(Spacer(1, 0.5*cm))

    headers = ['ID', 'Brand', 'Name', 'Year', 'Category', 'Fuel', 'Engine', 'Rate/Day', 'Available']
    rows    = [headers]
    for b in Bike.objects.all():
        rows.append([
            str(b.pk), b.brand, b.name, str(b.model_year),
            b.get_category_display(), b.get_fuel_type_display(),
            b.engine_cc or '—', f"Rs.{b.price_per_day}",
            'Yes' if b.is_available else 'No',
        ])

    col_widths = [1*cm, 3*cm, 4*cm, 2*cm, 3.5*cm, 3*cm, 3*cm, 3*cm, 2.5*cm]
    table = Table(rows, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), orange),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF7ED')]),
        ('GRID',       (0, 0), (-1, -1), 0.4, colors.HexColor('#E5E7EB')),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('PADDING',    (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("RideEase Bike Rental System — Confidential", s_style))

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="RideEase_Bikes.pdf"'
    return response


@admin_required
def export_bookings_pdf(request):
    """Export all bookings as PDF."""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                               rightMargin=1.5*cm, leftMargin=1.5*cm,
                               topMargin=2*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    orange = colors.HexColor('#F97316')
    h_style = ParagraphStyle('H', fontSize=16, textColor=orange,
                             fontName='Helvetica-Bold', alignment=TA_CENTER)
    s_style = ParagraphStyle('S', fontSize=9, alignment=TA_CENTER, parent=styles['Normal'])

    elements = []
    elements.append(Paragraph("RideEase Bike Rental System", h_style))
    elements.append(Paragraph("Bookings Report", s_style))
    elements.append(Paragraph(f"Generated: {timezone.now().strftime('%d %B %Y')}", s_style))
    elements.append(Spacer(1, 0.5*cm))

    headers = ['#', 'Customer', 'Bike', 'Pickup', 'Return', 'Days', 'Total (INR)', 'Status']
    rows    = [headers]
    for b in Booking.objects.select_related('user', 'bike').all():
        rows.append([
            str(b.pk),
            b.user.get_full_name() or b.user.username,
            f"{b.bike.brand} {b.bike.name}",
            b.pickup_date.strftime('%d %b %Y'),
            b.return_date.strftime('%d %b %Y'),
            str(b.total_days),
            f"Rs.{b.total_cost}",
            b.get_status_display(),
        ])

    col_widths = [1.2*cm, 5*cm, 5*cm, 3*cm, 3*cm, 1.5*cm, 3.5*cm, 3*cm]
    table = Table(rows, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), orange),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF7ED')]),
        ('GRID',       (0, 0), (-1, -1), 0.4, colors.HexColor('#E5E7EB')),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('PADDING',    (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("RideEase Bike Rental System — Confidential", s_style))

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="RideEase_Bookings.pdf"'
    return response
