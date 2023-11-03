from django.db import models
from userapp.models import User
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="sender_message_set")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="reciever_message_set")
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self) -> str:
    #     return f'{self.sender.first_name}-{self.sender.last_name}'

class ChatList(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="reciever")
    timestamp = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('sender', 'receiver')  

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Message)
def update_chatlist_timestamp(sender, instance, created, **kwargs):
    if created:
        sender_user = instance.sender
        receiver_user = instance.receiver

        chat_list, created = ChatList.objects.get_or_create(sender=sender_user, receiver=receiver_user)

        chat_list.timestamp = instance.timestamp
        chat_list.save()
  
