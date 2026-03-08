from django.db import models
from home.models import ParticipantProfile

class createteam(models.Model):
    event = models.ForeignKey('host.Event', on_delete=models.CASCADE)
    username= models.ForeignKey(ParticipantProfile, on_delete=models.CASCADE)
    team_code= models.CharField(max_length=8, unique=True)
    team_name = models.CharField(max_length=100)
    team_leader= models.CharField(max_length=100)
    email= models.EmailField()
    gitaccount= models.CharField(max_length=100)   
    team_members = models.CharField(max_length=500)  # Comma-separated list of team members
    tnc= models.BooleanField(default=False)
    def __str__(self):
        return f"{self.event} - {self.team_name} ({self.team_code})"

class jointeam(models.Model):
    event = models.ForeignKey('host.Event', on_delete=models.CASCADE)
    username= models.ForeignKey(ParticipantProfile, on_delete=models.CASCADE)
    team_code= models.CharField(max_length=8)
    team_name = models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    email= models.EmailField()
    gitaccount= models.CharField(max_length=100)
    tnc= models.BooleanField(default=False)
    def __str__(self):
        return f"{self.event} - {self.team_name} ({self.team_code})"