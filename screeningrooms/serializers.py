from rest_framework import serializers
from .models import ScreeningRoom, Seat

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class ScreeningRoomSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = ScreeningRoom
        fields = '__all__'