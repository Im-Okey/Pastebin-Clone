# Generated by Django 5.1.1 on 2024-10-15 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_paste_time_live'),
        ('general', '0007_messages_is_checked_notifications_is_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.paste'),
            preserve_default=False,
        ),
    ]