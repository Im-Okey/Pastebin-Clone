# Generated by Django 5.1.1 on 2024-10-01 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_paste_time_live_alter_paste_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paste',
            name='time_live',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
