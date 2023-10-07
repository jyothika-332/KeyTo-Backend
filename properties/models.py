from django.db import models
from userapp.models import User

# Create your models here.

class Property(models.Model):
    CHOICES = (
        ('rent', 'rent'),
        ('sale', 'sale')
    )

    user =  models.ForeignKey(User, on_delete=models.CASCADE,default=None,null=True,blank=True)
    title = models.CharField(max_length=255,default=None,null=True,blank=True)
    location = models.CharField(max_length=255,default=None,null=True,blank=True)
    address = models.CharField(max_length=250,default=None,null=True,blank=True)
    total_cent = models.BigIntegerField(default=None,null=True,blank=True)
    price_per_cent = models.BigIntegerField(default=None,null=True,blank=True)
    latitude = models.FloatField(default=None,null=True,blank=True)
    longitude = models.FloatField(default=None,null=True,blank=True)
    description = models.CharField(max_length=255,blank=True,null=True,default=None)
    image = models.ImageField(upload_to='propertyImage',blank=True,default=None,null=True)
    type = models.CharField( max_length=30, default=None, choices=CHOICES,null=True,blank=True)


class PropertyImage(models.Model):
    property_id = models.ForeignKey(Property,on_delete=models.CASCADE)
    image = models.ImageField()