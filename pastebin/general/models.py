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


class Messages(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_receiver', default=None)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_sender', default=None)
    post = models.ForeignKey(Paste, on_delete=models.CASCADE)
    text = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Notifications(models.Model):
    COMMENT = 1
    LIKE = 2
    DISLIKE = 3
    FAVOURITE = 4

    NOTE_TYPES = [
        (1, 'Comment'),
        (2, 'Like'),
        (3, 'Dislike'),
        (4, 'Favourite'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='note_receiver', default=None)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='note_sender', default=None)
    post = models.ForeignKey(Paste, on_delete=models.CASCADE)
    send_time = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)

    notification_type = models.IntegerField(choices=NOTE_TYPES)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def get_notification_message(self):
        if self.notification_type == 1:
            return f'{self.sender} прокомментировал ваш пост'
        elif self.notification_type == 2:
            return f'{self.sender} лайкнул ваш пост'
        elif self.notification_type == 3:
            return f'{self.sender} поставил дизлайк вашему посту'
        elif self.notification_type == 4:
            return f'{self.sender} добавил ваш пост в избранное'
        return 'Неизвестное уведомление'