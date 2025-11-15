from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint

# Create your models here.
class User(AbstractUser):
    option = (
        ('user','user'),
        ('staff','staff')
    )
    phone=models.CharField(max_length=15)
    role=models.CharField(max_length=100,choices=option,default="user")
    profile=models.ImageField(upload_to="profile",default="profile/default.jpeg")
    otp=models.CharField(max_length=20)
    is_verified=models.BooleanField(default=False)

    #random otp generation
    def generate_otp(self):
        send_otp=str(randint(1000,9999))+str(self.id) # for making unique is , added userid at the end
        self.otp=send_otp
        self.save()