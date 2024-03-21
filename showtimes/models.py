from django.db import models
from movies.models import Movie
from screeningrooms.models import ScreeningRoom
from django.utils import timezone

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    screening_room = models.ForeignKey(ScreeningRoom, on_delete=models.CASCADE, verbose_name="Screening Room")
    showtime = models.DateTimeField(verbose_name="Showtime")


    def __str__(self):
        return f"{self.movie} at {self.showtime} in {self.screening_room}"

    def has_passed(self):
        """Checks if the showtime has already occurred."""
        return self.showtime < timezone.now()
