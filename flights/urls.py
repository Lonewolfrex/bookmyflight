from django.urls import path
from . import views

app_name = 'flights'

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('sign-up/', views.sign_up, name='sign_up'),
]
