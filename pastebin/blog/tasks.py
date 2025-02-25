from datetime import timedelta
import logging
from celery import shared_task
import requests
from django.core.mail import send_mail
from django.db.models import F
from django.utils import timezone

from blog.models import Comment, Paste
from config import settings
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
    logger.info(
        f"Задача [{task_id}] по удалению старых прочитанных сообщений и уведомлений запущена в {now:%Y-%m-%d %H:%M:%S}")

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
    logger.info(
        f"Задача [{task_id}] по отправке отчета о непрочитанных сообщениях запущена в {timezone.now():%Y-%m-%d %H:%M:%S}")

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
                try:
                    send_mail(
                        subject,
                        message,
                        'arseny.butko771@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(e)

                logger.info(f"Задача [{task_id}] — письмо отправлено пользователю {user.username}")
    else:
        print('Не найдено ни 1 пользователя')

    logger.info(f"Задача [{task_id}] по отправке отчета завершена")


PERSPECTIVE_API_KEY = settings.PERSPECTIVE_API_KEY
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


@shared_task
def check_toxicity(comment_content):
    """Отправляет текст в Perspective API и проверяет токсичность комментария"""
    # Формируем запрос
    payload = {
        "comment": {"text": comment_content},
        "languages": ["ru", "en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {}
        }
    }
    params = {"key": PERSPECTIVE_API_KEY}

    response = requests.post(PERSPECTIVE_URL, json=payload, params=params)

    if response.status_code == 200:
        scores = response.json()["attributeScores"]
        toxicity = scores["TOXICITY"]["summaryScore"]["value"]
        severe_toxicity = scores["SEVERE_TOXICITY"]["summaryScore"]["value"]

        result = {
            "blocked": toxicity > 0.8 or severe_toxicity > 0.6
        }
        return result

    else:
        return {"error": "Ошибка API"}
