from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import ValidationError



class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if not user.is_active:
            raise ValidationError('User is not active', code='inactive_user')

        # Add custom claims
        token['id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        token['name'] = f'{user.first_name} {user.last_name}'
        token['is_active'] = user.is_active

        return token    


# class VerifyAccountSerializer(serializers.Serializer):
#     email = serializers.EmailField()    
#     otp = serializers.CharField()    