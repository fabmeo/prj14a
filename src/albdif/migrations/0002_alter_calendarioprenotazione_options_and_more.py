# Generated by Django 5.1.3 on 2024-11-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albdif', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendarioprenotazione',
            options={'verbose_name': 'Calendario della prenotazione', 'verbose_name_plural': 'Calendario della prenotazione'},
        ),
        migrations.AlterModelOptions(
            name='camera',
            options={'verbose_name': 'Camera', 'verbose_name_plural': 'Camere'},
        ),
        migrations.AlterModelOptions(
            name='foto',
            options={'verbose_name': 'Foto camera', 'verbose_name_plural': 'Foto camere'},
        ),
        migrations.AlterModelOptions(
            name='host',
            options={'verbose_name': 'Host', 'verbose_name_plural': 'Host'},
        ),
        migrations.AlterModelOptions(
            name='prenotazione',
            options={'verbose_name': 'Prenotazione', 'verbose_name_plural': 'Prenotazioni'},
        ),
        migrations.AlterModelOptions(
            name='prezzocamera',
            options={'verbose_name': 'Prezzo della camera', 'verbose_name_plural': 'Prezzo della camere'},
        ),
        migrations.AlterModelOptions(
            name='proprieta',
            options={'verbose_name': 'Proprietà', 'verbose_name_plural': 'Proprietà'},
        ),
        migrations.AlterModelOptions(
            name='stagione',
            options={'verbose_name': 'Stagione', 'verbose_name_plural': 'Stagioni'},
        ),
        migrations.AlterModelOptions(
            name='visitatore',
            options={'verbose_name': 'Visitatore', 'verbose_name_plural': 'Visitatori'},
        ),
        migrations.AlterField(
            model_name='foto',
            name='file',
            field=models.FileField(blank=True, upload_to='foto_camera'),
        ),
    ]