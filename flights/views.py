from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login  
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Flight, Booking

# ----------------------
# CUSTOMER VIEWS
# ----------------------

@login_required
def home(request):
    flights = Flight.objects.filter(seats_available__gt=0).order_by('departure')

    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    departure_date = request.GET.get('departure_date')

    if origin:
        flights = flights.filter(origin__icontains=origin)

    if destination:
        flights = flights.filter(destination__icontains=destination)

    if departure_date:
        flights = flights.filter(departure__date=departure_date)

    context = {
        'flights': flights,
        'origin': origin,
        'destination': destination,
        'departure_date': departure_date,
    }

    return render(request, 'flights/home.html', context)

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id, seats_available__gt=0)
    customer = request.user

    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        if seats <= 0:
            messages.error(request, "Please select at least 1 seat.")
        elif seats > flight.seats_available:
            messages.error(request, f"Only {flight.seats_available} seats left.")
        else:
            # Create booking and reduce seats
            booking = Booking.objects.create(
                customer=customer,
                flight=flight,
                seats=seats,
                status='booked'
            )
            flight.seats_available -= seats
            flight.save()
            messages.success(request, f"✅ Booking created! Seats: {seats}.")
            return redirect('flights:my_bookings')

    return render(request, 'flights/book_flight.html', {'flight': flight})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'flights/my_bookings.html', {'bookings': bookings})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user, status__in=['booked', 'paid'])

    if request.method == 'POST':
        old_seats = booking.seats
        seats = int(request.POST.get('seats', old_seats))

        if seats == 0:
            messages.error(request, "Please select at least 1 seat.")
        else:
            # Restore old seats, assign new
            flight = booking.flight
            flight.seats_available += old_seats
            if seats <= flight.seats_available + old_seats:
                flight.seats_available -= (seats - old_seats)
                flight.save()
                booking.seats = seats
                booking.status = 'booked'  # keep booked until paid again
                booking.save()
                messages.success(request, f"✅ Booking updated to {seats} seats!")
            else:
                messages.error(request, "Not enough seats available.")
    return render(request, 'flights/edit_booking.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    booking.status = 'cancelled'
    booking.flight.seats_available += booking.seats
    booking.flight.save()
    booking.save()
    messages.success(request, "✅ Booking cancelled!")
    return redirect('flights:my_bookings') 

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user, status='booked')
    if request.method == 'POST':
        # DUMMY payment logic (no real card)
        booking.status = 'paid'
        payment_id = f"P-{booking.id}-{booking.customer.id}"
        booking.payment_id = payment_id
        booking.save()
        messages.success(request, "✅ Payment processed (dummy gateway)!")
        return redirect('flights:my_bookings')
    return render(request, 'flights/payment.html', {'booking': booking})

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "✅ Account created!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})

# ----------------------
# AUTH / PROFILE
# ----------------------

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')
