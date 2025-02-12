from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    # notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-all-read/', views.mark_all_read_notifications, name='mark-all-notes-read'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_as_read,
         name='mark-notification-read'),

    # messages
    path('messages/', views.messages, name='messages'),
    path('messages/mark-all-read/', views.mark_all_read_messages, name='mark-all-messages-read'),
    path('message/read/<int:message_id>/', views.mark_message_as_read, name='mark-message-read'),


    # likes & dislikes
    path('like/<int:paste_id>/', views.like_paste, name='like_paste'),
    path('dislike/<int:paste_id>/', views.dislike_paste, name='dislike_paste'),

]
