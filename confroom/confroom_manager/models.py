from django.db import models


# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=32)
    capacity = models.IntegerField()
    have_projector = models.BooleanField()


class Reservation(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField()
