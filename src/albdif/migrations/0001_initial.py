# Generated by Django 5.1.3 on 2024-12-21 17:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='... inserire un nickname', max_length=100)),
                ('descrizione', models.CharField(max_length=1000)),
                ('services', models.JSONField(default={'aria condizionata': True, 'minibar': False, 'toilette': True, 'tv': True, 'wifi': True}, help_text='Servizi offerti nella camera, ad esempio: toilette, wifi, phon, etc.')),
            ],
            options={
                'verbose_name': 'Camera',
                'verbose_name_plural': 'Camere',
            },
        ),
        migrations.CreateModel(
            name='Stagione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stagione', models.CharField(max_length=50)),
                ('data_inizio', models.DateField()),
                ('data_fine', models.DateField()),
            ],
            options={
                'verbose_name': 'Stagione',
                'verbose_name_plural': 'Stagioni',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registrazione', models.DateTimeField(verbose_name='data registrazione')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'Host',
            },
        ),
        migrations.CreateModel(
            name='Prenotazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_prenotazione', models.DateTimeField()),
                ('stato_prenotazione', models.CharField(choices=[('PR', 'Registrata'), ('SC', 'Scaduta'), ('CA', 'Cancellata'), ('PG', 'Confermata')], default='PR', max_length=2)),
                ('richiesta', models.CharField(blank=True, help_text='richiesta aggiuntiva del cliente', max_length=1000, null=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.camera')),
            ],
            options={
                'verbose_name': 'Prenotazione',
                'verbose_name_plural': 'Prenotazioni',
            },
        ),
        migrations.CreateModel(
            name='CalendarioPrenotazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inizio', models.DateField()),
                ('data_fine', models.DateField()),
                ('prenotazione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.prenotazione')),
            ],
            options={
                'verbose_name': 'Calendario della prenotazione',
                'verbose_name_plural': 'Calendario della prenotazione',
            },
        ),
        migrations.CreateModel(
            name='Proprieta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=200)),
                ('principale', models.BooleanField(default=False, help_text="Indica se è l'AD principale")),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.host')),
            ],
            options={
                'verbose_name': 'Proprietà',
                'verbose_name_plural': 'Proprietà',
            },
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, upload_to='foto_camera')),
                ('camera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='albdif.camera')),
                ('proprieta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='albdif.proprieta')),
            ],
            options={
                'verbose_name': 'Foto',
                'verbose_name_plural': 'Foto',
            },
        ),
        migrations.AddField(
            model_name='camera',
            name='proprieta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.proprieta'),
        ),
        migrations.CreateModel(
            name='PrezzoCamera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prezzo', models.DecimalField(decimal_places=2, max_digits=7)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.camera')),
                ('stagione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.stagione')),
            ],
            options={
                'verbose_name': 'Prezzo della camera',
                'verbose_name_plural': 'Prezzo della camere',
            },
        ),
        migrations.CreateModel(
            name='Visitatore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registrazione', models.DateTimeField(verbose_name='data registrazione')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Visitatore',
                'verbose_name_plural': 'Visitatori',
            },
        ),
        migrations.AddField(
            model_name='prenotazione',
            name='visitatore',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.visitatore'),
        ),
    ]
