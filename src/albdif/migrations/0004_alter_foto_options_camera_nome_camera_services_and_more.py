# Generated by Django 5.1.3 on 2024-11-30 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albdif', '0003_proprieta_principale'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foto',
            options={'verbose_name': 'Foto', 'verbose_name_plural': 'Foto'},
        ),
        migrations.AddField(
            model_name='camera',
            name='nome',
            field=models.CharField(default='... inserire un nickname', max_length=100),
        ),
        migrations.AddField(
            model_name='camera',
            name='services',
            field=models.JSONField(default={'aria_condizionata': True, 'minibar': False, 'toilette': True, 'tv': True, 'wifi': True}, help_text='Servizi offerti nella camera, ad esempio: toilette, wifi, phon, etc.'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='descrizione',
            field=models.CharField(max_length=1000),
        ),
    ]