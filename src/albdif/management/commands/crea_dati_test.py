from datetime import date

from django.core.management.base import BaseCommand
from albdif.models import Proprieta, Camera, Prenotazione, ServizioCamera, Servizio

from albdif.utils.fixtures import ProprietaFactory, CameraFactory, PrenotazioneFactory, \
    CalendarioPrenotazioneFactory, StagioneFactory, FotoFactory, ProprietaPrincFactory, UserFactory, VisitatoreFactory, \
    ServizioFactory, ServizioCameraFactory
from albdif.views import camera_detail


class Command(BaseCommand):
    help = 'Crea dati di test'

    def handle(self, *args, **kwargs):

        # Servizi
        #servs = ServizioFactory.build_batch(5)
        #for s in servs:
        #    s.save()
        servs = ['toilette', 'wifi', 'phon', 'minibar', 'aria condizionata']
        for s in servs:
            ServizioFactory.create(descrizione_servizio=s)

        # Proprietà principale
        ProprietaPrincFactory.create()

        # Creazione proprieta
        for _ in range(3):
            p = ProprietaFactory.create()
            FotoFactory.create(proprieta=p)

        # Creazione camere
        for proprieta in Proprieta.objects.all():
            for _ in range(4):
                c = CameraFactory.create(proprieta=proprieta)
                for s in Servizio.objects.all():
                    ServizioCameraFactory.create(camera=c, servizio=s)
                FotoFactory.create(camera=c)
                FotoFactory.create(camera=c)

        # Creazione stagioni
        stagioni = [
            ('Bassa', date(2025, 1, 1), date(2025, 2, 28), 50.00),
            ('Media', date(2025, 3, 1), date(2025, 5, 31), 75.00),
            ('Bassa', date(2025, 6, 1), date(2025, 9, 30), 100.00),
            ('Media', date(2025, 10, 1), date(2025, 12, 31), 75.00),
            ('Bassa', date(2026, 1, 1), date(9999, 12, 31), 85.00)
        ]
        
        for stagione, data_inizio, data_fine, prezzo_default in stagioni:
            StagioneFactory.create(
                stagione=stagione,
                data_inizio=data_inizio,
                data_fine=data_fine,
                prezzo_default=prezzo_default
            )

        # Creazione prenotazioni
        for c in Camera.objects.all():
            PrenotazioneFactory.create(camera=c)

        # Creazione calendario prenotazioni
        for p in Prenotazione.objects.all():
            CalendarioPrenotazioneFactory.create(prenotazione=p)

        # Creazione dell'utente guest
        g = UserFactory.create(username="guest")
        VisitatoreFactory.create(utente=g)

        self.stdout.write(self.style.SUCCESS('Dati di test creati con successo'))