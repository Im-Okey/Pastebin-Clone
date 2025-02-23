# Generated by Django 5.1.6 on 2025-02-22 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeDislikePaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])),
            ],
            options={
                'verbose_name': 'Рейтинг пасты',
                'verbose_name_plural': 'Рейтинг пасты',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('is_checked', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('notification_type', models.IntegerField(choices=[(1, 'Comment'), (2, 'Like'), (3, 'Dislike'), (4, 'Favourite')])),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
        migrations.CreateModel(
            name='LikeDislikeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_dislikes', to='blog.comment')),
            ],
            options={
                'verbose_name': 'Рейтинг коментария',
                'verbose_name_plural': 'Рейтинг коментариев',
            },
        ),
    ]
