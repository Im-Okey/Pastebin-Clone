from ..models import Notifications, Messages


def get_general_context(request, Paste):
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    unread_notifications_count = Notifications.objects.filter(user=request.user, is_checked=False).count()
    unread_messages_count = Messages.objects.filter(user=request.user, is_checked=False).count()

    return popular_posts, unread_messages_count, unread_notifications_count
