from .models import Messages, Notifications
from blog.models import Paste


def unread_counts(request):
    if request.user.is_authenticated:
        unread_messages_count = Messages.objects.filter(user=request.user, is_checked=False).count()
        unread_notifications_count = Notifications.objects.filter(user=request.user, is_checked=False).count()
    else:
        unread_messages_count = 0
        unread_notifications_count = 0

    return {
        'unread_messages_count': unread_messages_count,
        'unread_notifications_count': unread_notifications_count,
    }