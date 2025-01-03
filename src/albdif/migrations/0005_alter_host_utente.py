# Generated by Django 4.2.17 on 2024-12-30 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('albdif', '0004_alter_visitatore_utente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='utente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
