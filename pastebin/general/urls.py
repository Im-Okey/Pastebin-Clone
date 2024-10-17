from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.messages, name='messages'),

    path('notifications/mark-all-read/', views.mark_all_read_notifications, name='mark-all-notes-read'),
    path('messages/mark-all-read/', views.mark_all_read_messages, name='mark-all-messages-read'),

    path('message/read/<int:message_id>/', views.mark_message_as_read, name='mark-message-read'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_as_read,
         name='mark-notification-read'),

]
