from rest_framework import serializers
from flightApp.models import Flight, Passenger, Reservation
import re

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'
    # CUSTOM Validators: WAY ONE:
    # Convention for custom validators: validate_<model_field_name>
    def validate_flightNumber(self, flightNumber):
        print('>>>> validate_flightNumber()')
        if (re.match('^[a-zA-Z0-9]*$', flightNumber)==None):
            raise serializers.ValidationError('Invalid Flight Number. Please make it alpha-numeric')
        return flightNumber

    # CUSTOM Validators: WAY TWO:
    def validate(self, data):
        print('>>>> validate()')
        if (re.match('^[a-zA-Z0-9]*$', data['flightNumber'])==None):
            raise serializers.ValidationError('Invalid Flight Number. Please make it alpha-numeric')
        return data


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
