from datetime import date, datetime

from django.db import models
from home.models import HostProfile, ParticipantProfile


class Event(models.Model):
    host = models.ForeignKey(HostProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_datetime = models.DateTimeField(default=datetime.now)
    end_datetime = models.DateTimeField(default=datetime.now)
    prize= models.CharField(max_length=500,default="Certificate")
    location = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

