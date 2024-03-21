from django.db import models
from django.conf import settings
from screeningrooms.models import Seat, ScreeningRoom
from showtimes.models import Showtime

class Booking(models.Model):
  """
  The Booking model represents a user's booking for a specific showtime.
  """
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
  showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
  booking_time = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return f'Booking #{self.id} by {self.user.username} for {self.showtime}'

  class Meta:
    verbose_name = 'Booking'
    verbose_name_plural = 'Bookings'

class SeatReservation(models.Model):
  """
  The SeatReservation model represents a seat reservation for a specific showtime.
  """
  seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='reservations')
  showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='reservations')
  booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='seat_reservations')
  is_reserved = models.BooleanField(default=True)

  class Meta:
    unique_together = (('seat', 'showtime'),)

  def __str__(self):
    return f"{self.seat} reserved for {self.showtime}"