from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seats_available = models.IntegerField(default=100)
    airline = models.CharField(max_length=100)

    def remaining_seats(self):
        return self.seats_available

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"

    class Meta:
        ordering = ['departure']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')
    booking_date = models.DateTimeField(default=timezone.now)
    payment_id = models.CharField(max_length=50, null=True, blank=True)

    def total_price(self):
        return self.seats * self.flight.price

    def get_absolute_url(self):
        return reverse('flights:my_bookings')

    def __str__(self):
        return f"{self.customer.username} - {self.flight.flight_number} ({self.status})"
