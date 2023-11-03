from django.urls import path
from .views import *

urlpatterns = [
    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),
    path("addtochat/<int:user_id>/", AddToChat.as_view(),name="addtochat"),
    path("get-seller-recent-chat/<int:seller_id>/", GetSellerRecentChat.as_view()),
]