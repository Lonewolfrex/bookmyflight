from django.urls import path
from .api_views import *

urlpatterns = [
    path('flights/', FlightListAPI.as_view()),
    path('flights/<int:pk>/', FlightDetailAPI.as_view()),
    path('bookings/create/', BookingCreateAPI.as_view()),
    path('bookings/', BookingListAPI.as_view()),
    path('bookings/<int:pk>/', BookingUpdateAPI.as_view()),
    path('bookings/<int:pk>/delete/', BookingDeleteAPI.as_view()),
    path('payment/<int:pk>/', PaymentAPI.as_view()),
]