from django.db import models

# Create your models here.

class Banner(models.Model):
    heading = models.CharField(max_length=255,default=None)
    image = models.ImageField(upload_to='bannerImage',blank=True,default=None)
    priority = models.IntegerField()
    description = models.CharField(max_length=255,default=None)