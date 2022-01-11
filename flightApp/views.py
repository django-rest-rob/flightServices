from django.shortcuts import render
from flightApp.models import Flight, Passenger, Reservation
from flightApp.serializers import FlightSerializer, PassengerSerializer, ReservationSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

# Create your views here.
# Custom function-based view - must be marked as api_view to make it...
# ...a REST endpoint
@api_view(['POST'])
def find_flights(request):
    flights = Flight.objects.filter(departureCity=request.data['departureCity'], arrivalCity=request.data['arrivalCity'], dateOfDeparture=request.data['dateOfDeparture'])
    serializer = FlightSerializer(flights,many=True)
    return Response(serializer.data)

# Another custom fbv for creating a Reservation
@api_view(['POST'])
def create_reservation(request):
    # get Flight object using sent flightId from client
    flight = Flight.objects.get(id=request.data['flightId'])

    # create new Passenger object with sent in details
    passenger = Passenger()
    passenger.firstName = request.data['firstName']
    passenger.middleName = request.data['middleName']
    passenger.lastName = request.data['lastName']
    passenger.email = request.data['email']
    passenger.phone = request.data['phone']
    # save passenger
    passenger.save()

    # create new Reservation object
    reservation = Reservation()
    reservation.flight = flight
    reservation.passenger = passenger
    # call save on the reservation model object
    reservation.save()

    return Response(model_to_dict(reservation), status = status.HTTP_201_CREATED)



class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['departureCity','arrivalCity','dateOfDeparture']
    permission_classes = [IsAuthenticated]

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
