from datetime import timedelta
import logging
from celery import shared_task
from django.db.models import F
from django.utils import timezone
from .models import Paste


logger = logging.getLogger(__name__)

@shared_task
def delete_expired_pastes():
    now = timezone.now()
    logger.info("Задача по удалению устаревших паст запущена в %s", now)

    expired_pastes = Paste.objects.filter(
        time_live__isnull=False,
        time_live__gt=timedelta(seconds=0),
        created_at__lte=now - F('time_live')
    )

    if expired_pastes.exists():
        logger.info("Найдено %d устаревших паст для удаления", expired_pastes.count())
        expired_pastes.delete()
        logger.info("Успешно удалено %d паст", expired_pastes.count())
    else:
        logger.info("Устаревших паст не найдено для удаления")

    logger.info("Задача по удалению устаревших паст завершена")