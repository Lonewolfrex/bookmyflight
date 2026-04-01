from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer, PaymentSerializer


# GET /api/flights/
class FlightListAPI(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


# GET /api/flights/{id}/
class FlightDetailAPI(generics.RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


# POST /api/bookings/create/
class BookingCreateAPI(generics.CreateAPIView):
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# GET /api/bookings/
class BookingListAPI(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)


# PUT /api/bookings/{id}/
class BookingUpdateAPI(generics.UpdateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)


# DELETE /api/bookings/{id}/delete/
class BookingDeleteAPI(generics.DestroyAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)


# POST /api/payment/{id}/
class PaymentAPI(APIView):

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(id=pk, customer=request.user)

            payment_data = {
                "booking_id": booking.id,
                "amount": booking.total_price,
                "payment_mode": request.data.get("payment_mode")
            }

            serializer = PaymentSerializer(payment_data)

            return Response({
                "message": "Payment successful",
                "payment": payment_data
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)