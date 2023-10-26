from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path ('',PropertyView.as_view()),
   path ('dashboard_datas/',DashboardDatasViews.as_view()),
   path ('agent_dashboard/',DashboardDatasViewsSeller.as_view()),
]