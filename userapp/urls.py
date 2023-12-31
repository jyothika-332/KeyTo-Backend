from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
   path ('',UserView.as_view()),
   path ('become-a-seller/<int:id>/',BecomeSeller.as_view()),
   path ('changepassword/',ChangePassword.as_view()),
   path ('send-resetlink/',SendResetLink.as_view()),
   path ('reset-password/',ResetPassword.as_view()),
   path ('updateseller/<int:pk>/',UpdateSeller.as_view()),
   path ('addtopremium/',AddtoPremium.as_view()),
   path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('get_refresh_token/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
   
]
