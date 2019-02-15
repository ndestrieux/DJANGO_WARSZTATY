from django.db import models


# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=32)
    capacity = models.IntegerField()
    have_projector = models.BooleanField(default=False)


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)
