from rest_framework import serializers
from .models import *



class Banner_serializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'