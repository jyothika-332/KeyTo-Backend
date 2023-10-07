
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from userapp.views import *
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('userapp.urls')),  
    path('verify/', VerifyOTP.as_view()),
    path('send-otp/', SendOTP.as_view()),
    path('property/', include('properties.urls')),
    path('banner/', include('bannerapp.urls')),  
    path('payment/', include('paymentapp.urls')),  
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
