from rest_framework import serializers
from .models import Showtime
from movies.serializers import MovieSerializer
from screeningrooms.serializers import ScreeningRoomSerializer

class ShowtimeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    screening_room = ScreeningRoomSerializer(read_only=True)

    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'screening_room', 'showtime',  'available_seats']


