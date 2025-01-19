from datetime import date, timedelta

from django.core.management.base import BaseCommand
from albdif.models import Group, RuoloUtente, RichiestaAdesione
from django.contrib.auth.models import Permission

from albdif.models import Proprieta, Camera, Prenotazione, Servizio, Visitatore, User
from albdif.utils.fixtures import ProprietaFactory, CameraFactory, PrenotazioneFactory, \
    CalendarioPrenotazioneFactory, StagioneFactory, FotoFactory, ProprietaPrincFactory, UserFactory, VisitatoreFactory, \
    ServizioFactory, ServizioCameraFactory, RuoloUtenteFactory, RichiestaAdesioneFactory


class Command(BaseCommand):
    help = 'Crea dati di test'

    def handle(self, *args, **kwargs):

        # Creazione dell'utente admin
        UserFactory.create(username="admin",
                           first_name="Fabius",
                           last_name="Pegasus",
                           is_superuser=True,
                           is_staff=True)

        servs = ['toilette', 'wifi', 'phon', 'minibar', 'aria condizionata']
        for s in servs:
            ServizioFactory.create(descrizione_servizio=s)

        # Creazione ruoli
        visitatore, __ = Group.objects.get_or_create(name="Visitatore")
        permissions = Permission.objects.filter(
            content_type__app_label="albdif",
            codename__in=["consulta_catalogo", ],
        )
        visitatore.permissions.add(*permissions)

        print("Crea il ruolo Titolare")
        titolare, __ = Group.objects.get_or_create(name="Titolare")
        permissions = Permission.objects.filter(
            content_type__app_label="albdif",
            codename__in=["crea_proprieta", "consulta_catalogo",],
        )
        titolare.permissions.add(*permissions)

        # Creazione visitatori
        utenti = UserFactory.build_batch(2)
        for u in utenti:
            u.save()
            # Creazione ruolo
            RuoloUtenteFactory.create(utente=u, ruolo=visitatore, ente=None)
        print(f"utenti: {len(utenti)}")

        for t in User.objects.filter(is_superuser=False):
            VisitatoreFactory.create(utente=t)

        # Proprietà principale
        ProprietaPrincFactory.create()

        # Creazione altre proprieta
        for _ in range(3):
            p = ProprietaFactory.create()
            # Creazione il visitatore
            v = VisitatoreFactory.create()
            # Creazione ruolo Titolare "ru" per il visitatore "v" sulla proprietà "p"
            ru = RuoloUtenteFactory.create(utente=v.utente, ruolo=titolare, ente=p)
            FotoFactory.create(proprieta=p)
            RichiestaAdesioneFactory(utente=ru.utente)
        print(f"proprietà: {Proprieta.objects.all().count()}")

        # Creazione camere
        for proprieta in Proprieta.objects.all():
            for _ in range(4):
                c = CameraFactory.create(proprieta=proprieta)
                for s in Servizio.objects.all():
                    ServizioCameraFactory.create(camera=c, servizio=s)
                FotoFactory.create(camera=c)
                FotoFactory.create(camera=c)
        print(f"camere: {Camera.objects.all().count()}")

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

        gruppo = Group.objects.get(name="Visitatore")
        for r in RuoloUtente.objects.filter(ruolo=gruppo):
            # Creazione prenotazioni
            for c in Camera.objects.all():
                v = Visitatore.objects.get(utente=r.utente)
                PrenotazioneFactory.create(camera=c, visitatore=v)

        # Creazione calendario prenotazioni
        gg = 1
        for p in Prenotazione.objects.all():
            CalendarioPrenotazioneFactory.create(prenotazione=p,
                                                 data_inizio=date.today() + timedelta(days=gg),
                                                 data_fine=date.today() + timedelta(days=gg+3))
            gg = gg + 20

        # Creazione dell'utente guest
        g = UserFactory.create(username="guest")
        v = VisitatoreFactory.create(utente=g)

        c1 = Camera.objects.get(id=1)
        c2 = Camera.objects.get(id=2)
        c3 = Camera.objects.get(id=3)
        # pagata passata
        p1 = PrenotazioneFactory.create(camera=c1, visitatore=v,
                                        stato_prenotazione='PG',
                                        data_prenotazione=date(2024, 1, 1))
        CalendarioPrenotazioneFactory.create(prenotazione=p1,
                                             data_inizio=date(2024, 2, 1),
                                             data_fine=date(2024, 2, 5))

        # pagata futura
        p2 = PrenotazioneFactory.create(camera=c2, visitatore=v,
                                        stato_prenotazione='PG',
                                        data_prenotazione=date(2024, 1, 1))
        CalendarioPrenotazioneFactory.create(prenotazione=p2,
                                             data_inizio=date(2024, 1, 1),
                                             data_fine=date(2024, 1, 5))

        # prenotata futura
        p3 = PrenotazioneFactory.create(camera=c3, visitatore=v,
                                        stato_prenotazione='PR',
                                        data_prenotazione=date.today() - timedelta(days=10))
        CalendarioPrenotazioneFactory.create(prenotazione=p3,
                                             data_inizio=date.today() + timedelta(days=30),
                                             data_fine=date.today() + timedelta(days=35))

        self.stdout.write(self.style.SUCCESS('Dati di test creati con successo'))