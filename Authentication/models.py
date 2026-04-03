from django.db import models
from django.contrib.auth.models import AbstractUser

class User_Details(AbstractUser):
    Mobiele_Number = models.CharField(max_length=15, null=True, blank=True)    #---> optional  Null , ""
    Age = models.PositiveIntegerField(null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    State = models.CharField(max_length=50, null=True, blank=True)
    Country = models.CharField(max_length=50, null=True, blank=True)       
     
    def __str__(self):
        return self.username