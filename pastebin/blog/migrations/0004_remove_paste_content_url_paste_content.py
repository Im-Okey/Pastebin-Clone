# Generated by Django 5.1.1 on 2024-09-24 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_paste_content_paste_access_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paste',
            name='content_url',
        ),
        migrations.AddField(
            model_name='paste',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
