from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, Http404
from .models import Booking, SeatReservation
from .signals import send_booking_confirmation_email, send_booking_cancellation_email
from .forms import BookingForm
from django.contrib import messages
from django.apps import apps
from users.utils import is_staff


Showtime = apps.get_model('showtimes', 'Showtime')
Seat = apps.get_model('screeningrooms', 'Seat')

@login_required
def create_booking(request, showtime_id):
  """
  Create a new booking and reserve seats for the user.
  """
  showtime = get_object_or_404(Showtime, pk=showtime_id)

  if request.method == "POST":
    form = BookingForm(request.POST, showtime_id=showtime_id)
    if form.is_valid():
      # Create a new booking instance without saving to the database.
      booking = form.save(commit=False)
      booking.user = request.user

      # Save the booking to the database.
      booking.save()

      # Process reserved seats from the form.
      reserved_seats = form.cleaned_data["seats"]
      for seat in form.cleaned_data["seats"]:
          SeatReservation.objects.create(
              seat=seat, showtime=showtime, booking=booking, is_reserved=True
          )

      send_booking_confirmation_email(booking)

      messages.success(request, "Booking successfully created.")
      return redirect("profile")
  else:
    # Create a new booking form with the specified showtime.
    form = BookingForm(showtime_id=showtime_id)

  return render(
    request, "bookings/create_booking.html", {"form": form, "showtime": showtime}
  )

@login_required
def seats_reserved_count(request, showtime_id):
    """
    Calculate the seats number booking for the user in a single showtime     """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)


    seats_count = SeatReservation.objects.filter(booking__user=request.user, showtime_id=showtime_id).count()

    return JsonResponse({'seats_count': seats_count})


@login_required
def delete_booking(request, booking_id):
    """
    Handles booking cancellation and seat release.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.user or is_staff(request.user):
      if request.method == "POST":
          # Collect seat details before deleting the booking
          seats_details = ", ".join([f"{seat.seat.row_letter}{seat.seat.seat_number}" for seat in booking.seat_reservations.all()])
          
          # Release the reserved seats for the booking being deleted.
          SeatReservation.objects.filter(booking=booking).update(is_reserved=False)
          
          # Send cancellation email before deleting the booking to have access to seat reservations
          send_booking_cancellation_email(booking, seats_details)

          # Delete the booking after sending the email
          booking.delete()

          messages.success(request, "Your booking has been cancelled successfully.")
          # Redirect staff users back to the admin dashboard and regular users to their profile.
          if request.user.is_staff:
              return redirect("admin_dashboard")
          return redirect("profile")
      else:
          # Display confirmation for booking deletion.
          return render(request, "bookings/confirm_delete.html", {"booking": booking})
    else:
      messages.error(request, "You do not have permission to cancel this booking.")
      return redirect("profile")

def seat_availability(request, showtime_id):
  """
  Fetch the seat availability for the specified showtime ID.
  """
  try:
    showtime = Showtime.objects.filter(pk=showtime_id).first()

    if not showtime:
      raise Http404("Showtime not found")

    seats = Seat.objects.filter(screening_room=showtime.screening_room).order_by(
      "row_letter", "seat_number"
    )

    reservations = SeatReservation.objects.filter(
      showtime=showtime, is_reserved=True
    ).values_list("seat_id", flat=True)

    seat_data = []

    for seat in seats:
      is_reserved = seat.id in reservations

      seat_info = {
        "id": seat.id,
        "row_letter": seat.row_letter,
        "seat_number": seat.seat_number,
        "is_reserved": is_reserved,
      }

      seat_data.append(seat_info)

    return JsonResponse({"seats": seat_data})

  # Catch any exceptions and return a JSON response with an error.
  except Exception as e:
    return JsonResponse({"error": "Error fetching seat availability"}, status=500)
