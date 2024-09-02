from django.db import models

from blog.models import Tag
from users.models import CustomUser


class TagSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка на тег'
        verbose_name_plural = 'Подписки на теги'
        constraints = [
            models.UniqueConstraint(fields=['user', 'tag'], name='unique_user_tag_subscription'),
        ]


class UserFollow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка на пользователя'
        verbose_name_plural = 'Подписки на пользователей'
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follower_followed'),
        ]