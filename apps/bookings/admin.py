from django.contrib import admin
from .models import Booking, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'user', 'bike', 'pickup_date', 'return_date', 'total_cost', 'status', 'created_at')
    list_filter   = ('status', 'pickup_date')
    search_fields = ('user__username', 'user__email', 'bike__name', 'bike__brand')
    list_editable = ('status',)
    raw_id_fields = ('user', 'bike')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('user', 'bike', 'rating', 'created_at')
    list_filter   = ('rating',)
    search_fields = ('user__username', 'bike__name')
