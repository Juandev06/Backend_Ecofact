import cuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta,datetime


# Create your models here.

class User(AbstractUser):
    ROLES = [
        
        
        
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES)
    password = models.CharField(max_length=128, null=False, blank=False)
    
    
    def set_password(self, raw_password):
        return super().set_password(raw_password)
    
