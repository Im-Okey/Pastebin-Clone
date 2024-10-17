from datetime import timedelta
import logging
from celery import shared_task
from django.db.models import F
from django.utils import timezone
from .models import Paste
from general.models import Messages, Notifications

logger = logging.getLogger(__name__)

@shared_task
def delete_expired_pastes():
    """Позже нужно бдует переделать на 1 день"""
    now = timezone.now()
    task_id = delete_expired_pastes.request.id
    logger.info(f"Задача [{task_id}] по удалению устаревших паст запущена в {now:%Y-%m-%d %H:%M:%S}")

    expired_pastes = Paste.objects.filter(
        time_live__isnull=False,
        time_live__gt=timedelta(seconds=0),
        created_at__lte=now - F('time_live')
    )

    if expired_pastes.exists():
        logger.info(f"Задача [{task_id}] — найдено {expired_pastes.count()} устаревших паст для удаления")
        count, _ = expired_pastes.delete()
        logger.info(f"Задача [{task_id}] — успешно удалено {count} паст")
    else:
        logger.info(f"Задача [{task_id}] — устаревших паст не найдено для удаления")

    logger.info(f"Задача [{task_id}] по удалению устаревших паст завершена")


@shared_task
def delete_old_unread_messages_and_notifications():
    """Позже нужно бдует переделать на 1 неделю"""
    now = timezone.now()
    task_id = delete_old_unread_messages_and_notifications.request.id
    logger.info(f"Задача [{task_id}] по удалению старых прочитанных сообщений и уведомлений запущена в {now:%Y-%m-%d %H:%M:%S}")

    old_messages = Messages.objects.filter(
        is_checked=True,
        send_time__lte=now - timedelta(minutes=1)
    )

    old_notifications = Notifications.objects.filter(
        is_checked=True,
        send_time__lte=now - timedelta(minutes=1)
    )


    if old_messages.exists():
        logger.info(f"Задача [{task_id}] — найдено {old_messages.count()} сообщений для удаления")
        deleted_messages_count, _ = old_messages.delete()
        logger.info(f"Задача [{task_id}] — успешно удалено {deleted_messages_count} сообщений")
    else:
        logger.info(f"Задача [{task_id}] — старых сообщений для удаления не найдено")

    if old_notifications.exists():
        logger.info(f"Задача [{task_id}] — найдено {old_notifications.count()} уведомлений для удаления")
        deleted_notifications_count, _ = old_notifications.delete()
        logger.info(f"Задача [{task_id}] — успешно удалено {deleted_notifications_count} уведомлений")
    else:
        logger.info(f"Задача [{task_id}] — старых уведомлений для удаления не найдено")

    logger.info(f"Задача [{task_id}] по удалению старых прочитанных сообщений и уведомлений завершена")