from rest_framework.serializers import ModelSerializer
from .models import Message,ChatList
from rest_framework import serializers


class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email','timestamp']



class UserChatListSerializer(serializers.ModelSerializer):
    receiver_profile = serializers.ImageField(source='receiver.profile_image', read_only=True)
    receiver_id = serializers.CharField(source='receiver.id', read_only=True)
    receiver_first_name = serializers.CharField(source='receiver.first_name', read_only=True)
    receiver_email = serializers.EmailField(source='receiver.email', read_only=True)
    
    class Meta:
        model = ChatList
        fields = '__all__'        


class SellerChatListSerializer(serializers.ModelSerializer):
    sender_profile = serializers.ImageField(source='sender.profile_image', read_only=True)
    sender_id = serializers.CharField(source='sender.id', read_only=True)
    sender_first_name = serializers.CharField(source='sender.first_name', read_only=True)
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    
    class Meta:
        model = ChatList
        fields = '__all__'        

        

