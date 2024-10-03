from celery import shared_task
from django.db.models import F
from django.utils import timezone
from .models import Paste


@shared_task
def delete_expired_pastes():
    now = timezone.now()
    expired_pastes = Paste.objects.filter(time_live__isnull=False, created_at__lte=now - F('time_live'))

    print(f"Посты, которые должны быть удалены: {expired_pastes.count()}")

    expired_pastes.delete()