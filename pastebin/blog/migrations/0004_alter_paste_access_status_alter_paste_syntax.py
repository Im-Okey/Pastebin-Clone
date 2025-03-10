# Generated by Django 5.1.6 on 2025-03-08 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_paste_syntax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paste',
            name='access_status',
            field=models.IntegerField(choices=[(0, 'Public'), (1, 'Draft')], default=0),
        ),
        migrations.AlterField(
            model_name='paste',
            name='syntax',
            field=models.CharField(choices=[('plaintext', 'Обычный текст'), ('python', 'Python'), ('javascript', 'JavaScript'), ('clike', 'C/C++/Java'), ('sql', 'SQL'), ('css', 'CSS')], default='plaintext', max_length=20),
        ),
    ]
