from rest_framework import serializers
from .models import *



class Property_serializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'