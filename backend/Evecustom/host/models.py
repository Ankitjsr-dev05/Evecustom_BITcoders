from datetime import date

from django.db import models
from home.models import HostProfile, ParticipantProfile


class Event(models.Model):
    host = models.ForeignKey(HostProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(default=date.today)
    start_time= models.TimeField(null=True, blank=True)
    end_time= models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    