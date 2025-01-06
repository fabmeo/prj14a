from datetime import date, timedelta
from decimal import Decimal

from django_webtest import DjangoTestApp

from albdif.models import Proprieta, Prenotazione
from albdif.utils.fixtures import CameraFactory, StagioneFactory, PrezzoCameraFactory, PrenotazioneFactory, \
    VisitatoreFactory, CalendarioPrenotazioneFactory, ServizioFactory, ServizioCameraFactory


def test_proprieta(user, host):
    Proprieta.objects.create(
        host=host,
        descrizione="bla bla",
        principale=True,
    )
    try:
        Proprieta.objects.create(
            host=host,
            descrizione="bla bla",
            principale=True
        )
    except Exception as e:
        assert "Esiste già una proprietà principale." in str(e)


def test_stagione(app: "DjangoTestApp"):
    try:
        StagioneFactory.create(
            stagione="Bassa",
            data_inizio=date(2025, 1, 1),
            data_fine=date(2024, 12, 31)
        )
    except Exception as e:
        assert "La data fine deve essere maggiore della data inizio" in str(e)

    s1 = StagioneFactory.create(
        stagione="Bassa",
        data_inizio=date(2025, 1, 1),
        data_fine=date(2025, 12, 31)
    )
    try:
        s1 = StagioneFactory.create(
            stagione="Alta",
            data_inizio=date(2025, 7, 1),
            data_fine=date(2025, 8, 31),
            prezzo_default=120
        )
    except Exception as e:
        assert "Le date si sovrappongono ad un'altra stagione" in str(e)


def test_camera(app: "DjangoTestApp"):
    s1 = StagioneFactory.create(
        stagione="Bassa",
        data_inizio=date(2025, 1, 1),
        data_fine=date(2025, 12, 31)
    )
    c1 = CameraFactory.create()
    assert c1.prezzo_bassa_stagione
    assert c1.prezzo_bassa_stagione > 0
    PrezzoCameraFactory.create(camera=c1, stagione=s1, prezzo=45.63)
    assert c1.prezzo_bassa_stagione == Decimal("45.63")

def test_prenotazione(app: "DjangoTestApp"):
    c1 = CameraFactory.create()
    v1 = VisitatoreFactory.create()
    p1 = PrenotazioneFactory.create(camera=c1, visitatore=v1, stato_prenotazione=Prenotazione.CONFERMATA)
    try:
        p1.stato_prenotazione = Prenotazione.REGISTRATA
        p1.save()
    except Exception as e:
        assert "Passaggio di stato non consentito da" in str(e)

def test_prenotazione_contemporanea(app: "DjangoTestApp"):

    c1 = CameraFactory.create()
    v1 = VisitatoreFactory.create()
    v2 = VisitatoreFactory.create()
    p1 = PrenotazioneFactory.create(camera=c1, visitatore=v1, stato_prenotazione=Prenotazione.REGISTRATA)
    CalendarioPrenotazioneFactory.create(prenotazione=p1,
                                         data_inizio=date.today() + timedelta(days=5),
                                         data_fine=date.today() + timedelta(days=7))
    try:
        p2 = PrenotazioneFactory.create(camera=c1, visitatore=v2, stato_prenotazione=Prenotazione.REGISTRATA)
        CalendarioPrenotazioneFactory.create(prenotazione=p2,
                                             data_inizio=date.today() + timedelta(days=5),
                                             data_fine=date.today() + timedelta(days=7))
    except Exception as e:
        assert "Trovata altra prenotazione nello stesso periodo" in str(e)


def test_servizio_camera(app: "DjangoTestApp"):
    c1 = CameraFactory.create()
    s1 = ServizioFactory.create()
    try:
        ServizioCameraFactory.create(servizio=s1, camera=c1, incluso=False, costo=0)
    except Exception as e:
        assert "Se il servizio è opzionale va indicato il costo" in str(e)

