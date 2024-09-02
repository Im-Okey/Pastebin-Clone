from django.db import models

from blog.models import Paste, Comment
from users.models import CustomUser


class LikeDislikePaste(models.Model):
    ACTION_CHOICES = [
        (1, 'Like'),
        (-1, 'Dislike'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    paste = models.ForeignKey(Paste, related_name='likes_dislikes', on_delete=models.CASCADE)
    action = models.IntegerField(choices=ACTION_CHOICES)

    class Meta:
        verbose_name = 'Рейтинг пасты'
        verbose_name_plural = 'Рейтинг пасты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'paste'], name='unique_user_paste_like_dislike'),
        ]


class LikeDislikeComment(models.Model):
    ACTION_CHOICES = [
        (1, 'Like'),
        (-1, 'Dislike'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='likes_dislikes', on_delete=models.CASCADE)
    action = models.IntegerField(choices=ACTION_CHOICES)

    class Meta:
        verbose_name = 'Рейтинг коментария'
        verbose_name_plural = 'Рейтинг коментариев'
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_user_comment_like_dislike'),
        ]