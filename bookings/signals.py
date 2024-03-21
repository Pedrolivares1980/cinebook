from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking, SeatReservation
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Booking)
def handle_new_booking(sender, instance, created, **kwargs):
	"""
	This signal is triggered after a new booking is saved.
	Assumes that seat reservations are managed in the view before calling save on a Booking instance.
	"""
	if created:
			send_booking_confirmation_email(instance)

@receiver(post_delete, sender=Booking)
def handle_booking_deletion(sender, instance, **kwargs):
	"""
	Deletes SeatReservation instances associated with the booking being deleted.
	This ensures seats become available again once a booking is cancelled.
	"""
	SeatReservation.objects.filter(booking=instance).delete()

def send_booking_confirmation_email(booking):
	"""
	Sends an email to the user confirming their booking.
	"""
	subject = "Booking Confirmation"
	message = f"Dear {booking.user.username}, your booking for {booking.showtime.movie.title} on {booking.showtime.showtime} has been confirmed."
	recipient_list = [booking.user.email]
	send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

def send_booking_cancellation_email(booking):
	"""
	Sends an email to the user notifying them that their booking has been cancelled.
	"""
	subject = "Booking Cancellation"
	message = f"Dear {booking.user.username}, your booking for {booking.showtime.movie.title} on {booking.showtime.showtime} has been cancelled."
	recipient_list = [booking.user.email]
	send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@receiver(post_delete, sender=Booking)
def handle_booking_deletion(sender, instance, **kwargs):
	"""
	Deletes SeatReservation instances associated with the booking being deleted.
	This ensures seats become available again once a booking is cancelled.
	"""
	SeatReservation.objects.filter(booking=instance).delete()
	send_booking_cancellation_email(instance)