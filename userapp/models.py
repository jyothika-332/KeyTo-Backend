from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('seller', 'seller'),
        ('admin', 'admin')
    )
    first_name = models.CharField(max_length=255,null=True,blank=True,default=None)
    last_name = models.CharField(max_length=255,null=True,blank=True,default=None)
    password = models.CharField(max_length=255,null=True,blank=True,default=None)
    phone = models.CharField(max_length=10,null=True,blank=True,default=None)
    email = models.CharField(max_length=255,null=True,blank=True,default=None)
    role = models.CharField( max_length=30, default='user', choices=ROLE_CHOICES)
    is_premium = models.BooleanField(null=True,blank=True,default=False)
    premium_starting = models.DateField(null=True,default=None,blank=True)
    premium_ending = models.DateField(null=True,default=None,blank=True)
    is_active = models.BooleanField(null=True,blank=True,default=True)
    address = models.TextField(null=True,blank=True,default=None)
    location = models.TextField(null=True,blank=True,default=None)
    profile_image = models.ImageField(upload_to='profileImage',null=True,blank=True,default=None)
    id_card_image = models.ImageField(upload_to='IDcard',null=True,blank=True,default=None)


class User_otp(models.Model):
    email = models.CharField(max_length=250,null=True,blank=True,default=None)
    otp = models.BigIntegerField(null=True)