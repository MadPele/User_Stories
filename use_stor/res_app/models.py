from django.db import models


class Room(models.Model):
    name = models.CharField(
        verbose_name="Name",
        max_length=30)

    capacity = models.PositiveSmallIntegerField(
        verbose_name="Capacity",)

    projector = models.BooleanField(
        default=False,
        verbose_name='Projector')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class Reservation(models.Model):
    date = models.DateField(
        verbose_name='Date',)

    room = models.ForeignKey(
        Room,
        verbose_name='Room',
        on_delete=models.SET_NULL,
        null=True)

    comment = models.TextField(
        verbose_name='Comment')

    def __str__(self):
        return f'Reservation {self.room.name} at {self.date}'

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        unique_together = ("date", "room")

