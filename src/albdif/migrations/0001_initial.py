# Generated by Django 4.2.17 on 2025-01-08 21:47

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('nome', models.CharField(default='... inserire un nickname', max_length=100)),
                ('descrizione', models.CharField(max_length=2000)),
                ('principale', models.BooleanField(default=False, help_text="Indica se è l'AD principale")),
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
            name='Group',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('registrazione', models.DateTimeField()),
                ('codice_fiscale', models.CharField(blank=True, max_length=16, null=True)),
                ('partita_iva', models.CharField(blank=True, max_length=11, null=True)),
                ('telefono', models.CharField(blank=True, help_text='Deve contenere solo numeri e uno slash ( / )', max_length=255, null=True, validators=[django.core.validators.RegexValidator('^\\d[1-9]{1,3}/\\d{7,10}$')], verbose_name='Telefono')),
                ('richiesta_associazione', models.FileField(blank=True, null=True, upload_to='richiesta_host')),
                ('contratto', models.FileField(blank=True, null=True, upload_to='contratti_host')),
                ('groups', models.ManyToManyField(related_name='albdif_user_set', to='albdif.group')),
                ('user_permissions', models.ManyToManyField(related_name='albdif_user_set_permissions', to='auth.permission')),
            ],
            options={
                'permissions': (('Visitatore', 'Gestione visitatore'), ('Titolare', 'Titolare di proprietà'), ('Contabile', 'Gestore contabilità proprietà'), ('Accoglienza', 'Accoglienza visitatori di una proprietà')),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
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
                ('ente', models.ForeignKey(blank=True, limit_choices_to={'parent__isnull': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='albdif.proprieta')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('visitatore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albdif.utente')),
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
