
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path ('',UserView.as_view()),
   # path ('login/',LoginView.as_view()),

   path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
   
]
