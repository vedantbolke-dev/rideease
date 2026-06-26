"""
RideEase Bike Rental System
Bookings App — Create, view, cancel bookings and submit reviews.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from apps.bikes.models import Bike
from .models import Booking, Review
from .forms import BookingForm, ReviewForm


@login_required
def booking_create(request, bike_id):
    """Create a new booking for a given bike."""
    bike = get_object_or_404(Bike, pk=bike_id)

    if not bike.is_available:
        messages.error(request, f"Sorry, {bike.brand} {bike.name} is currently not available.")
        return redirect('bikes:detail', pk=bike_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, bike=bike)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user           = request.user
            booking.bike           = bike
            booking.price_per_day  = bike.price_per_day
            booking.helmet_deposit = bike.helmet_deposit
            booking.status         = 'pending'
            booking.save()

            bike.is_available = False
            bike.save()

            messages.success(
                request,
                f"Booking #{booking.pk} submitted! We will confirm it shortly."
            )
            return redirect('bookings:detail', pk=booking.pk)
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = BookingForm(bike=bike, initial={'pickup_location': bike.location})

    return render(request, 'bookings/booking_form.html', {'form': form, 'bike': bike})


@login_required
def booking_detail(request, pk):
    """View details of a single booking."""
    booking    = get_object_or_404(Booking, pk=pk, user=request.user)
    has_review = hasattr(booking, 'review')
    return render(request, 'bookings/booking_detail.html', {
        'booking':    booking,
        'has_review': has_review,
    })


@login_required
def booking_cancel(request, pk):
    """Cancel a pending or confirmed booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        if booking.can_cancel():
            booking.status = 'cancelled'
            booking.save()
            booking.bike.is_available = True
            booking.bike.save()
            messages.success(request, f"Booking #{booking.pk} has been cancelled.")
        else:
            messages.error(request, "This booking cannot be cancelled at this stage.")
        return redirect('users:dashboard')

    return render(request, 'bookings/booking_cancel_confirm.html', {'booking': booking})


@login_required
def booking_invoice(request, pk):
    """Printable invoice / receipt for a booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/invoice.html', {'booking': booking})


@login_required
def booking_invoice_pdf(request, pk):
    """Download booking invoice as PDF using ReportLab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    import io
    from django.utils import timezone

    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=A4,
                               rightMargin=2*cm, leftMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)

    styles  = getSampleStyleSheet()
    orange  = colors.HexColor('#F97316')
    darkgrey = colors.HexColor('#374151')

    heading_style = ParagraphStyle('Heading', parent=styles['Normal'],
                                   fontSize=18, textColor=orange,
                                   fontName='Helvetica-Bold', alignment=TA_CENTER)
    sub_style     = ParagraphStyle('Sub', parent=styles['Normal'],
                                   fontSize=10, textColor=darkgrey, alignment=TA_CENTER)
    label_style   = ParagraphStyle('Label', parent=styles['Normal'],
                                   fontSize=10, fontName='Helvetica-Bold')
    normal_style  = styles['Normal']
    normal_style.fontSize = 10

    elements = []
    elements.append(Paragraph("RideEase Bike Rental System", heading_style))
    elements.append(Paragraph("Booking Invoice / Receipt", sub_style))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%d %B %Y, %I:%M %p')}", sub_style))
    elements.append(Spacer(1, 0.6*cm))

    data = [
        ['Booking ID',    f"#{booking.pk}"],
        ['Customer Name', booking.user.get_full_name() or booking.user.username],
        ['Email',         booking.user.email],
        ['Phone',         booking.user.phone_number or '—'],
        ['Bike',          str(booking.bike)],
        ['Category',      booking.bike.get_category_display()],
        ['Pickup Date',   booking.pickup_date.strftime('%d %b %Y')],
        ['Return Date',   booking.return_date.strftime('%d %b %Y')],
        ['Total Days',    str(booking.total_days)],
        ['Pickup Location', booking.pickup_location],
        ['Drop Location', booking.drop_location or '—'],
        ['Rate Per Day',  f"Rs. {booking.price_per_day}"],
        ['Helmet Deposit (Refundable)', f"Rs. {booking.helmet_deposit}"],
        ['Total Amount',  f"Rs. {booking.total_cost}"],
        ['Status',        booking.get_status_display()],
    ]

    table = Table(data, colWidths=[6*cm, 11*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFF7ED')),
        ('FONTNAME',   (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('PADDING',    (0, 0), (-1, -1), 8),
        ('FONTNAME',   (0, 13), (-1, 13), 'Helvetica-Bold'),
        ('TEXTCOLOR',  (0, 13), (-1, 13), orange),
        ('FONTSIZE',   (0, 13), (-1, 13), 12),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("Thank you for choosing RideEase!", sub_style))
    elements.append(Paragraph("RideEase Bike Rental System — Pune, Maharashtra", sub_style))

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="RideEase_Invoice_{booking.pk}.pdf"'
    return response


@login_required
def booking_review(request, pk):
    """Submit a review after a completed booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if booking.status != 'completed':
        messages.error(request, "Reviews can only be submitted for completed bookings.")
        return redirect('bookings:detail', pk=pk)

    if hasattr(booking, 'review'):
        messages.info(request, "You have already submitted a review for this booking.")
        return redirect('bookings:detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review          = form.save(commit=False)
            review.booking  = booking
            review.user     = request.user
            review.bike     = booking.bike
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('bookings:detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'bookings/review_form.html', {'form': form, 'booking': booking})
