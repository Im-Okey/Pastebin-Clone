# Generated by Django 5.1.6 on 2025-02-24 20:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_initial'),
        ('general', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='likedislikecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='likedislikepaste',
            name='paste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_dislikes', to='blog.paste'),
        ),
        migrations.AddField(
            model_name='likedislikepaste',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messages',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.paste'),
        ),
        migrations.AddField(
            model_name='messages',
            name='sender',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messages',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notifications',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.paste'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='sender',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='note_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notifications',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='note_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='likedislikecomment',
            constraint=models.UniqueConstraint(fields=('user', 'comment'), name='unique_user_comment_like_dislike'),
        ),
        migrations.AddConstraint(
            model_name='likedislikepaste',
            constraint=models.UniqueConstraint(fields=('user', 'paste'), name='unique_user_paste_like_dislike'),
        ),
    ]
