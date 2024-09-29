import uuid
from django.utils import timezone

from django.db import models
from django.urls import reverse
from users.models import CustomUser as User
from datetime import timedelta, datetime


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Paste(models.Model):
    ACCESS_STATUS_CHOICES = [
        (0, 'Private'),
        (1, 'Public'),
        (2, 'Draft'),
    ]

    TIME_LIVE_CHOICES = [
        (None, 'Никогда'),
        (timedelta(hours=1), 'Через 1 час'),
        (timedelta(days=1), 'Через 1 день'),
        (timedelta(weeks=1), 'Через 1 неделю'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    access_status = models.IntegerField(choices=ACCESS_STATUS_CHOICES, default=1)
    time_live = models.DurationField(null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    is_delete_after_read = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает уникальную ссулку на пасту."""
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    def get_deletion_date(self):
        """Возвращает дату удаления пасты или 'Никогда'."""
        if self.time_live:
            deletion_date = timezone.now() + self.time_live
            return deletion_date.strftime('%d.%m.%Y')
        return "Никогда"

    def get_formatted_created_at(self):
        """Возвращает дату создания пасты."""
        return self.created_at.strftime('%d.%m.%Y')

    def get_time_live_display(self):
        """Возвращает строковое представление времени жизни пасты."""
        if self.time_live is None:
            return "Никогда"
        elif self.time_live <= timedelta(hours=1):
            return "Через 1 час"
        elif self.time_live <= timedelta(days=1):
            return "Через 1 день"
        elif self.time_live <= timedelta(weeks=1):
            return "Через 1 неделю"
        else:
            return "Неизвестно"

    class Meta:
        verbose_name = 'Паста'
        verbose_name_plural = 'Паста'


class Comment(models.Model):
    paste = models.ForeignKey(Paste, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
