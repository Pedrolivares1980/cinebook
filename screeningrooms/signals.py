from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ScreeningRoom, Seat

@receiver(post_save, sender=ScreeningRoom)
def create_seats_for_screeningroom(sender, instance, created, **kwargs):
    if created:
        total_rows = instance.capacity // instance.seats_per_row
        seat_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:total_rows]

        try:
            # Proceed only if no seats exist for this screening room
            if not Seat.objects.filter(screening_room=instance).exists():
                for row_letter in seat_letters:
                    for seat_number in range(1, instance.seats_per_row + 1):
                        Seat.objects.create(
                            screening_room=instance,
                            row_letter=row_letter,
                            seat_number=seat_number
                        )
        except Exception as e:
            # logging the exception details here
            print(f"Error creating seats for screening room '{instance.name}': {e}")
