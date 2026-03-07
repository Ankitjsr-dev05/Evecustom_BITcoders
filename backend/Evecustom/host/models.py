from django.db import models
from home.models import HostProfile

class Event(models.Model):
    host = models.ForeignKey(HostProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
