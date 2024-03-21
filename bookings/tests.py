# bookings/tests.py

from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from .models import Booking, SeatReservation, Showtime, Seat
from .views import create_booking, delete_booking, seat_availability
from .serializers import BookingSerializer, ShowtimeSerializer, SeatSerializer
from .forms import BookingForm


class ModelsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testuser1234"
        )
        self.showtime = Showtime.objects.create(
            movie=None,
            showtime=timezone.now(),
            screening_room=None,
        )
        self.seat = Seat.objects.create(
            seat_number=1,
            screening_room=None,
        )

    def test_booking_model(self):
        booking = Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
        )
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.showtime, self.showtime)

    def test_seat_reservation_model(self):
        seat_reservation = SeatReservation.objects.create(
            booking=Booking.objects.create(
                user=self.user,
                showtime=self.showtime,
            ),
            seat=self.seat,
        )
        self.assertEqual(seat_reservation.booking.user, self.user)
        self.assertEqual(seat_reservation.booking.showtime, self.showtime)
        self.assertEqual(seat_reservation.seat, self.seat)

    def test_showtime_model(self):self.assertTrue(self.showtime)

    def test_seat_model(self):
        self.assertTrue(self.seat)


class ViewsTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username="testuser",
            password="testuser1234"
        )
        self.client.force_login(user)

    def test_create_booking_view(self):
        response = self.client.get(
            reverse('create_booking', args=[self.showtime.id],)
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_booking_view(self):
        booking = Booking.objects.create(
            user=self.client.user,
            showtime=self.showtime,
        )
        response = self.client.get(
            reverse('delete_booking', args=[booking.id],)
        )
        self.assertEqual(response.status_code, 200)

    def test_seat_availability_view(self):
        response = self.client.get(
            reverse('seat_availability', args=[self.showtime.id])
        )
        self.assertEqual(response.status_code, 200)


class SerializersTests(TestCase):

    def test_booking_serializer(self):
        user = User.objects.create_user(
            username="testuser",
            password="testuser1234"
        )
        showtime = Showtime.objects.create(
            movie=None,
            showtime=timezone.now(),
            screening_room=None,
        )

        booking = Booking.objects.create(
            user=user,
            showtime=showtime,
        )

        serializer = BookingSerializer(booking)
        self.assertTrue(serializer.data)

    def test_showtime_serializer(self):
        showtime = Showtime.objects.create(
            movie=None,
            showtime=timezone.now(),
            screening_room=None,
        )

        serializer = ShowtimeSerializer(showtime)
        self.assertTrue(serializer.data)

    def test_seat_serializer(self):
        seat = Seat.objects.create(
            seat_number=1,
            screening_room=None,
        )

        serializer = SeatSerializer(seat)
        self.assertTrue(serializer.data)


class URLsTests(TestCase):

    def test_url_patterns(self):
        self.assertTrue(
            reverse('create_booking', args=[self.showtime.id])
            in settings.ROOT_URLCONF
        )
        self.assertTrue(
            reverse('delete_booking', args=[self.showtime.id])
            in settings.ROOT_URLCONF
        )
        self.assertTrue(
            reverse('seat_availability', args=[self.showtime.id])
            in settings.ROOT_URLCONF
        )


class FormsTests(TestCase):

    def test_booking_form(self):
        form = BookingForm({'showtime': self.showtime.id})
        self.assertTrue(form.is_valid())

        # Test form with invalid data
        form = BookingForm({'showtime': 0})
        self.assertFalse(form.is_valid())
