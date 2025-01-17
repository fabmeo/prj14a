# Generated by Django 4.2.17 on 2025-01-09 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='... inserire un nickname', max_length=100)),
                ('descrizione', models.CharField(max_length=1000)),
                ('numero_posti_letto', models.IntegerField(blank=True, default=2, null=True)),
            ],
            options={
                'verbose_name': 'Camera',
                'verbose_name_plural': 'Camere',
            },
        ),
        migrations.CreateModel(
            name='Proprieta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=2000)),
                ('principale', models.BooleanField(default=False, help_text="Indica se è l'AD principale")),
                ('nome', models.CharField(default='... inserire un nickname', max_length=100)),
            ],
            options={
                'verbose_name': 'Proprietà',
                'verbose_name_plural': 'Proprietà',
            },
        ),
        migrations.CreateModel(
            name='Servizio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione_servizio', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Servizio',
                'verbose_name_plural': 'Servizi',
            },
        ),
        migrations.CreateModel(
            name='Stagione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stagione', models.CharField(choices=[('Bassa', 'Bassa stagione'), ('Media', 'Media stagione'), ('Alta', 'Alta stagione')], max_length=50)),
                ('data_inizio', models.DateField()),
                ('data_fine', models.DateField()),
                ('prezzo_default', models.DecimalField(decimal_places=2, default=50, max_digits=7)),
            ],
            options={
                'verbose_name': 'Stagione',
                'verbose_name_plural': 'Stagioni',
            },
        ),
        migrations.CreateModel(
            name='Visitatore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registrazione', models.DateTimeField()),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('codice_fiscale', models.CharField(blank=True, max_length=16, null=True)),
                ('utente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Visitatore',
                'verbose_name_plural': 'Visitatori',
            },
        ),
        migrations.CreateModel(
            name='ServizioCamera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incluso', models.BooleanField(default=False)),
                ('costo', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.camera')),
                ('servizio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.servizio')),
            ],
            options={
                'verbose_name': 'Servizio camera',
                'verbose_name_plural': 'Servizi camera',
            },
        ),
        migrations.CreateModel(
            name='RuoloUtente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='albdif.proprieta')),
                ('ruolo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ruolo utente',
                'verbose_name_plural': 'Ruoli utente',
            },
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
            name='Prenotazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_prenotazione', models.DateTimeField()),
                ('stato_prenotazione', models.CharField(choices=[('PR', 'Registrata'), ('PG', 'Confermata'), ('CA', 'Cancellata'), ('RR', 'Richiesta Rimborso'), ('RE', 'Rimborsata'), ('NE', 'Negata'), ('SC', 'Scaduta')], default='PR', max_length=2)),
                ('richiesta', models.CharField(blank=True, help_text='richiesta aggiuntiva del cliente', max_length=1000, null=True)),
                ('costo_soggiorno', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('data_pagamento', models.DateTimeField(blank=True, null=True)),
                ('numero_persone', models.IntegerField(blank=True, default=1, null=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.camera')),
                ('visitatore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.visitatore')),
            ],
            options={
                'verbose_name': 'Prenotazione',
                'verbose_name_plural': 'Prenotazioni',
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
            name='CalendarioPrenotazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inizio', models.DateField(help_text='Data inizio soggiorno')),
                ('data_fine', models.DateField(help_text='Data fine soggiorno')),
                ('prenotazione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.prenotazione')),
            ],
            options={
                'verbose_name': 'Calendario della prenotazione',
                'verbose_name_plural': 'Calendario della prenotazione',
            },
        ),
    ]
