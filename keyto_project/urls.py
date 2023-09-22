
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from userapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('userapp.urls')),  
    path('verify/', VerifyOTP.as_view()),
    path('property/', include('properties.urls')),  
]
