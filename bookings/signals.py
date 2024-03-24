from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking, SeatReservation
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
    subject = "Booking Confirmation"
    showtime_formatted = booking.showtime.showtime.strftime("%A, %d of %B %Y at %H:%M")
    movie_image_url = booking.showtime.movie.poster_path
    seat_reservations = booking.seat_reservations.all()

    html_content = render_to_string('email/booking_confirmation.html', {
        'username': booking.user.username,
        'showtime_formatted': showtime_formatted,
        'movie_title': booking.showtime.movie.title,
        'movie_image_url': movie_image_url,
		'seat_reservations': seat_reservations,
    })

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[booking.user.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()


def send_booking_cancellation_email(booking):
    """
    Sends an email to the user notifying them that their booking has been cancelled.
    """
    subject = "Booking Cancellation"
    showtime_formatted = booking.showtime.showtime.strftime("%A, %d of %B %Y at %H:%M")
    movie_image_url = booking.showtime.movie.poster_path
    seat_reservations = booking.seat_reservations.all()
    for seat_reservation in seat_reservations:
        print(f"Row: {seat_reservation.seat.row_letter}, Seat: {seat_reservation.seat.seat_number}")


    html_content = render_to_string('email/booking_cancellation.html', {
        'username': booking.user.username,
        'showtime_formatted': showtime_formatted,
        'movie_title': booking.showtime.movie.title,
        'movie_image_url': movie_image_url,
		'seat_reservations': seat_reservations,
    })

    text_content = strip_tags(html_content)

    email= EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[booking.user.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()




@receiver(post_delete, sender=Booking)
def handle_booking_deletion(sender, instance, **kwargs):
	"""
	Deletes SeatReservation instances associated with the booking being deleted.
	This ensures seats become available again once a booking is cancelled.
	"""
	SeatReservation.objects.filter(booking=instance).delete()
	send_booking_cancellation_email(instance)