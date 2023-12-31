from rest_framework import serializers
from .models import *
from userapp.models import *
from userapp.serializers import *


class Property_serializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = '__all__'
    
    def get_user(self,obj):
      
        if obj.user == None:
            return None
        else:
            v_obj = User.objects.filter(id=obj.user.id)
            v_qs = User_serializer(v_obj, many=True)
        
        return v_qs.data
    

class Comments_serializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    property = serializers.SerializerMethodField()
    class Meta:
        model = Comments
        fields = '__all__'   
        
    def get_user(self,obj):
      
        if obj.user == None:
            return None
        else:
            v_obj = User.objects.filter(id=obj.user.id)
            v_qs = User_serializer(v_obj, many=True)
        
        return v_qs.data 
    def get_property(self,obj):
      
        if obj.user == None:
            return None
        else:
            v_obj = Property.objects.filter(id=obj.user.id)
            v_qs = Property_serializer(v_obj, many=True)
        
        return v_qs.data 