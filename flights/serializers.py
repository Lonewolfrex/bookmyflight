from rest_framework import serializers
from .models import Flight, Booking

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['customer']


class PaymentSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    amount = serializers.FloatField()
    payment_mode = serializers.CharField()