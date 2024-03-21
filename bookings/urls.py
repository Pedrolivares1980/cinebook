from django.urls import path
from . import views

urlpatterns = [
  # Create a new booking and reserve seats.
  path('create/<int:showtime_id>/', views.create_booking, name='create_booking'),
  # Delete an existing booking and release reserved seats.
  path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
  # Check the availability of seats for a given showtime.
  path('seats/<int:showtime_id>/', views.seat_availability, name='seat_availability'),
]
