from django.core.management.base import BaseCommand
from albdif.models import Proprieta

from albdif.utils.fixtures import VisitatoreFactory, HostFactory, ProprietaFactory, CameraFactory, PrenotazioneFactory, \
    CalendarioPrenotazioneFactory, StagioneFactory, FotoFactory


class Command(BaseCommand):
    help = 'Crea dati di test'

    def handle(self, *args, **kwargs):
        # Creazione visitatori
        for _ in range(9):
            VisitatoreFactory.create()

        # Creazione host
        for _ in range(2):
            HostFactory.create()

        # Creazione proprieta
        for _ in range(3):
            p = ProprietaFactory.create()
            FotoFactory.create(proprieta=p)

        # una delle 3 è la principale
        p = Proprieta.objects.all().first()
        p.principale = True
        p.save()

        # Creazione camere
        for proprieta in Proprieta.objects.all():
            for _ in range(3):
                c = CameraFactory.create(proprieta=proprieta)
                FotoFactory.create(camera=c)
                FotoFactory.create(camera=c)


        # Creazione stagioni
        for _ in range(3):
            StagioneFactory.create()

        # Creazione prenotazioni
        for _ in range(10):
            PrenotazioneFactory.create()

        # Creazione calendario prenotazioni
        for _ in range(10):
            CalendarioPrenotazioneFactory.create()

        self.stdout.write(self.style.SUCCESS('Dati di test creati con successo'))