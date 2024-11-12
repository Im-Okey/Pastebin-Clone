# Generated by Django 5.1.1 on 2024-11-12 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_paste_time_live'),
    ]

    operations = [
        migrations.AddField(
            model_name='paste',
            name='favourite_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='paste',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
