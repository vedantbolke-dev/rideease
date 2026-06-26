from django.urls import path
from . import views

app_name = 'bikes'

urlpatterns = [
    path('',            views.bike_list,   name='list'),
    path('<int:pk>/',   views.bike_detail, name='detail'),
]
