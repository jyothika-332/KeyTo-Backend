from django.db import models
from userapp.models import User

# Create your models here.

class Property(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,default=None,null=True,blank=True)
    location = models.CharField(max_length=255,default=None)
    address = models.CharField(max_length=250,default=None)
    total_cent = models.BigIntegerField(default=None)
    price_per_cent = models.BigIntegerField(default=None)
    description = models.CharField(max_length=255,blank=True,null=True,default=None)
    image = models.ImageField(upload_to='propertyImage',blank=True,default=None)
    is_rent = models.BooleanField(default=None)
    is_sell = models.BooleanField(default=None)

class PropertyImage(models.Model):
    property_id = models.ForeignKey(Property,on_delete=models.CASCADE)
    image = models.ImageField()    