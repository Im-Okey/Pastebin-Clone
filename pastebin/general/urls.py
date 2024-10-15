from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.messages, name='messages'),
]
