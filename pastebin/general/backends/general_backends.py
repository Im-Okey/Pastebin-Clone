from general.models import Notifications, Messages


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
    else:
        raise ValueError("Invalid flag provided")


def create_message(request, post, comment):
    """Создает сообщение"""
    Messages.objects.create(
        user=post.author,
        sender=request.user,
        post=post,
        text=comment.content,
    )