# Generated by Django 4.2.17 on 2025-01-11 09:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('albdif', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prezzocamera',
            options={'verbose_name': 'Prezzo della camera', 'verbose_name_plural': 'Prezzo delle camere'},
        ),
        migrations.AlterUniqueTogether(
            name='ruoloutente',
            unique_together={('utente', 'ente')},
        ),
    ]
