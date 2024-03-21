from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cinemas.models import Cinema

class ScreeningRoom(models.Model):
    CAPACITY_CHOICES = [
        (100, '100 seats'),
        (80, '80 seats'),
        (50, '50 seats'),
    ]
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="screening_rooms")
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)
    seats_per_row = models.IntegerField(default=10) 

    def __str__(self):
        return f"{self.name} - {self.cinema.name}"

class Seat(models.Model):
    screening_room = models.ForeignKey(ScreeningRoom, related_name="seats", on_delete=models.CASCADE)
    row_letter = models.CharField(max_length=1)
    seat_number = models.IntegerField()

    class Meta:
        unique_together = (('screening_room', 'row_letter', 'seat_number'),)

    def __str__(self):
        return f"Fila {self.row_letter} Asiento {self.seat_number} - {self.screening_room.name}"

@receiver(post_save, sender=ScreeningRoom)
def create_seats_for_screening_room(sender, instance, created, **kwargs):
    if created:
        rows = instance.capacity // instance.seats_per_row
        seat_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:rows]

        for row_letter in seat_letters:
            for seat_number in range(1, instance.seats_per_row + 1):
                Seat.objects.create(
                    screening_room=instance,
                    row_letter=row_letter,
                    seat_number=seat_number,
                )