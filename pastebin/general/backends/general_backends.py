from general.models import Notifications, Messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def create_notification_by_flag(request, post, flag):
    """Создает уведобление в зависимости от флага"""
    Notifications.objects.create(
        user=post.author,
        sender=request.user,
        post=post,
        notification_type=flag
    )


def create_notification(request, post, flag):
    """Формирует флаг для создания нужного уведомления"""
    get_flag_dictionary = {
        'comment': 1,
        'like': 2,
        'dislike': 3,
        'favourite': 4
    }

    if flag in get_flag_dictionary:
        numeric_flag = get_flag_dictionary[flag]
        create_notification_by_flag(request, post, numeric_flag)
        create_new_notification(post)
    else:
        raise ValueError("Invalid flag provided")


def create_message(request, post, comment):
    """Создает сообщение"""
    message = Messages.objects.create(
        user=post.author,
        sender=request.user,
        post=post,
        text=comment.content,
    )
    create_new_message(sender=request.user, recipient=post.author, message=message)


def create_new_message(sender, recipient, message):
    """Создает новое сообщение для работы с WebSockets"""
    unread_count = Messages.objects.filter(user=recipient, is_checked=False).count()
    avatar_url = sender.avatar.url if sender.avatar else "URL по умолчанию"

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}",
        {
            "type": "send_unread_message_count",
            "unread_messages_count": unread_count,
        }
    )
    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}",
        {
            "type": "send_new_message",
            "message": {
                "sender": sender.username,
                "text": message.text,
                "send_time": message.send_time.strftime('%Y-%m-%d %H:%M:%S'),
                "avatar_url": avatar_url,
            }
        }
    )


def create_new_notification(post):
    """Создает новое уведомление для работы с WebSockets"""
    unread_notifications_count = Notifications.objects.filter(user=post.author, is_checked=False).count()
    print(unread_notifications_count)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{post.author.id}",
        {
            "type": "send_unread_notification_count",
            "unread_notifications_count": unread_notifications_count
        }
    )
