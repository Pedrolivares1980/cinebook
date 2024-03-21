# bookings/serializers.py
from rest_framework import serializers
from .models import Booking
from showtimes.models import Showtime
from screeningrooms.models import Seat  
from django.contrib.auth import get_user_model

User = get_user_model()

class SeatSerializer(serializers.ModelSerializer):
  class Meta:
    model = Seat
    fields = ['id', 'row', 'number', 'is_reserved']

class ShowtimeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Showtime
    fields = ['id', 'movie', 'showtime', 'screening_room']

class BookingSerializer(serializers.ModelSerializer):
  seats = SeatSerializer(many=True, read_only=True)
  user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
  showtime = ShowtimeSerializer(read_only=True)

  class Meta:
    model = Booking
    fields = ['id', 'user', 'showtime', 'seats']
