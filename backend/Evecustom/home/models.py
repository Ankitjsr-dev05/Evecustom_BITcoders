from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class HostProfile(models.Model):
    role=models.CharField(max_length=100,default='host')
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone=models.CharField(max_length=10)
    organization=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    role=models.CharField(max_length=100,default='user')
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone=models.CharField(max_length=10)
    college=models.CharField(max_length=100)
    year=models.IntegerField(default=0000)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.username
    
