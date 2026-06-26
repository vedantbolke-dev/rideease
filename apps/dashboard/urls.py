from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',                         views.admin_dashboard,             name='home'),
    # Bikes
    path('bikes/',                   views.admin_bikes,                  name='bikes'),
    path('bikes/add/',               views.admin_bike_add,               name='bike_add'),
    path('bikes/<int:pk>/edit/',     views.admin_bike_edit,              name='bike_edit'),
    path('bikes/<int:pk>/delete/',   views.admin_bike_delete,            name='bike_delete'),
    path('bikes/<int:pk>/toggle/',   views.admin_bike_toggle,            name='bike_toggle'),
    # Bookings
    path('bookings/',                views.admin_bookings,               name='bookings'),
    path('bookings/<int:pk>/status/', views.admin_booking_update_status, name='booking_status'),
    # Users
    path('users/',                   views.admin_users,                  name='users'),
    path('users/<int:pk>/block/',    views.admin_user_toggle_block,      name='user_block'),
    path('users/<int:pk>/delete/',   views.admin_user_delete,            name='user_delete'),
    # Contact
    path('messages/',                views.admin_contact_messages,       name='messages'),
    # Exports
    path('export/bikes/csv/',        views.export_bikes_csv,             name='export_bikes_csv'),
    path('export/bikes/pdf/',        views.export_bikes_pdf,             name='export_bikes_pdf'),
    path('export/bookings/csv/',     views.export_bookings_csv,          name='export_bookings_csv'),
    path('export/bookings/pdf/',     views.export_bookings_pdf,          name='export_bookings_pdf'),
    path('export/users/csv/',        views.export_users_csv,             name='export_users_csv'),
]
