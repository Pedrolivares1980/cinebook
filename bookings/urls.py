from django.urls import path
from . import views

urlpatterns = [
  path('create/<int:showtime_id>/', views.create_booking, name='create_booking'),
  path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
  path('seats/<int:showtime_id>/', views.seat_availability, name='seat_availability'),
  path('resend-email/<int:booking_id>/', views.resend_confirmation_email, name='resend_confirmation_email'),
  path('seats-reserved-count/<int:showtime_id>/', views.seats_reserved_count, name='seats_reserved_count'),
]