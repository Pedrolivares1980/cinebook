from django import forms
from .models import Booking, Showtime, Seat, SeatReservation

class BookingForm(forms.ModelForm):
	"""
	Custom form for handling Booking creation.
	"""
	class Meta:
		model = Booking
		fields = ['showtime']

	seats = forms.ModelMultipleChoiceField(
		queryset=Seat.objects.none(), 
		required=False, 
		widget=forms.CheckboxSelectMultiple()
	)

	def __init__(self, *args, **kwargs):
		showtime_id = kwargs.pop('showtime_id', None)
		super(BookingForm, self).__init__(*args, **kwargs)

		if showtime_id:
			self.showtime_instance = Showtime.objects.get(id=showtime_id)
			self.fields['showtime'].initial = self.showtime_instance
			self.fields['showtime'].widget = forms.HiddenInput()

			# Filter seats to exclude those that are already reserved.
			reserved_seat_ids = SeatReservation.objects.filter(
				showtime=self.showtime_instance, 
				is_reserved=True
			).values_list('seat_id', flat=True)

			# Update the queryset for 'seats' to exclude reserved seats.
			self.fields['seats'].queryset = Seat.objects.filter(
				screening_room=self.showtime_instance.screening_room
			).exclude(id__in=reserved_seat_ids)
		else:
			raise ValueError("Showtime ID is required to initialize BookingForm.")

	def clean_seats(self):
		seats = self.cleaned_data.get('seats')

		for seat in seats:
			if SeatReservation.objects.filter(seat=seat, showtime=self.showtime_instance, is_reserved=True).exists():
				self.add_error('seats', f"Seat {seat} is not available for this showtime.")

		return seats

	def save(self, commit=True):
		booking = super().save(commit=False)
		booking.showtime = self.showtime_instance

		if commit:
			booking.save()
			self.save_m2m()  # Save many-to-many data for the form.
			for seat in self.cleaned_data['seats']:
				SeatReservation.objects.create(seat=seat, showtime=self.showtime_instance, booking=booking, is_reserved=True)

		return booking
