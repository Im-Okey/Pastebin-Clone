from django.shortcuts import render

from .models import Notifications, Messages
from blog.models import Paste

from .backends.general_backends import get_general_context


def notifications(request):
    notes = Notifications.objects.all().filter(user=request.user)
    popular_posts, unread_messages_count, unread_notifications_count = get_general_context(request, Paste)

    return render(request, 'notifications.html', {
        'popular_posts': popular_posts,
        'notes': notes,
        'unread_notifications_count': unread_notifications_count,
        'unread_messages_count': unread_messages_count
    })


def messages(request):
    mess = Messages.objects.all().filter(user=request.user)
    popular_posts, unread_messages_count, unread_notifications_count = get_general_context(request, Paste)
    return render(request, 'messages.html', {
        'popular_posts': popular_posts,
        'messages': mess,
        'unread_notifications_count': unread_notifications_count,
        'unread_messages_count': unread_messages_count
    })
