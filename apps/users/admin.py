from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_blocked', 'date_joined')
    list_filter   = ('is_staff', 'is_superuser', 'is_blocked', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering      = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': ('phone_number', 'address', 'city', 'state', 'pincode', 'driving_license', 'profile_picture', 'is_blocked')
        }),
    )
