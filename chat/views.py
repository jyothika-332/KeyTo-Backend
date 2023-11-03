from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView


class ChatCreatingView(CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = None

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = Message.objects.filter(
            thread_name=thread_name
        )
        return queryset
    
from django.db.models import Q

class AddToChat(ListCreateAPIView):
    queryset = ChatList.objects.all()
    serializer_class = UserChatListSerializer

    def get_queryset(self):
        userid = self.kwargs.get('user_id')
        return ChatList.objects.filter(sender=userid).order_by('-timestamp')
    
class GetSellerRecentChat(ListAPIView):
    queryset = ChatList.objects.all()
    serializer_class = SellerChatListSerializer

    def get_queryset(self):
        receiver_id = self.kwargs.get('seller_id')
        return ChatList.objects.filter(receiver=receiver_id).order_by('-timestamp')
    
    