from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Event(models.Model):
    day = models.IntegerField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    title = models.CharField(max_length=64)

class Schedule(models.Model):
    events = models.ManyToManyField(Event, blank=True, related_name="eschedule")

class User(AbstractUser):
    uschedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name = "oschedule")