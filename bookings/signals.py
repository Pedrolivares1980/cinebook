from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking, SeatReservation
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import qrcode
from io import BytesIO
import base64

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str


def send_booking_confirmation_email(booking):
    subject = "Booking Confirmation"
    showtime_formatted = booking.showtime.showtime.strftime("%A, %d of %B %Y at %H:%M")
    movie_image_url = booking.showtime.movie.poster_path
    seats_details = ", ".join([f"{seat_reservation.seat.seat_number}{seat_reservation.seat.row_letter}" for seat_reservation in booking.seat_reservations.all()])    
    
    qr_data = f"Username: {booking.user.username}, Email: {booking.user.email}, Movie: {booking.showtime.movie.title}, Showtime: {showtime_formatted}, Seats: {seats_details}"
    qr_code_image_base64 = generate_qr_code(qr_data)


    html_content = render_to_string('email/booking_confirmation.html', {
        'username': booking.user.username,
        'showtime_formatted': showtime_formatted,
        'movie_title': booking.showtime.movie.title,
        'movie_image_url': movie_image_url,
		'seats_details': seats_details,
        'qr_code': qr_code_image_base64
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


def send_booking_cancellation_email(booking, seats_details):
    """
    Sends an email to the user notifying them that their booking has been cancelled.
    """
    subject = "Booking Cancellation"
    showtime_formatted = booking.showtime.showtime.strftime("%A, %d of %B %Y at %H:%M")
    movie_image_url = booking.showtime.movie.poster_path

    html_content = render_to_string('email/booking_cancellation.html', {
        'username': booking.user.username,
        'showtime_formatted': showtime_formatted,
        'movie_title': booking.showtime.movie.title,
        'movie_image_url': movie_image_url,
		'seats_details': seats_details
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
