from django.contrib import admin
from .models import Flight, Booking

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination', 'departure', 'price', 'seats_available', 'airline')
    list_filter = ('airline', 'departure')
    search_fields = ('flight_number', 'origin', 'destination')
    ordering = ('departure',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'flight', 'seats', 'status', 'total_price', 'booking_date')
    list_filter = ('status', 'booking_date', 'flight__airline')
    search_fields = ('customer__username', 'flight__flight_number')
    readonly_fields = ('booking_date', 'total_price')
    
    def total_price(self, obj):
        return f"₹{obj.seats * obj.flight.price}"
    total_price.short_description = 'Total'
