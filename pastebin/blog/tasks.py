from datetime import timedelta
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import F
from django.utils import timezone
from .models import Paste
from general.models import Messages, Notifications

from users.models import CustomUser

logger = logging.getLogger(__name__)

@shared_task
def delete_expired_pastes():
    """Позже нужно буует переделать на 1 час"""
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
    """Позже нужно бдует переделать на 1 день"""
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



@shared_task
def send_weekly_unread_report():
    """Позже нужно бдует переделать на 1 неделю"""
    task_id = send_weekly_unread_report.request.id
    logger.info(f"Задача [{task_id}] по отправке отчета о непрочитанных сообщениях запущена в {timezone.now():%Y-%m-%d %H:%M:%S}")

    users = CustomUser.objects.all()
    if users.exists():
        for user in users:
            unread_messages_count = Messages.objects.filter(user=user, is_checked=False).count()
            unread_notifications_count = Notifications.objects.filter(user=user, is_checked=False).count()

            if unread_messages_count > 0 or unread_notifications_count > 0:
                subject = 'Отчет о непрочитанных сообщениях и уведомлениях'
                message = (f'Уважаемый {user.username},\n\n'
                           f'У вас {unread_messages_count} непрочитанных сообщений и '
                           f'{unread_notifications_count} непрочитанных уведомлений.\n\n'
                           'Пожалуйста, проверьте их.')

                send_mail(
                    subject,
                    message,
                    'arseny.butko771@gmail.com',
                    [user.email],
                    fail_silently=False,
                )

                logger.info(f"Задача [{task_id}] — письмо отправлено пользователю {user.username}")
    else:
        print('Не найдено ни 1 пользователя')

    logger.info(f"Задача [{task_id}] по отправке отчета завершена")