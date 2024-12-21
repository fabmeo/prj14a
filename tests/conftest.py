from datetime import date

import pytest
from albdif.models import Visitatore, Host, Proprieta, Camera, Prenotazione, CalendarioPrenotazione


@pytest.fixture()
def create_visitatori(db):
    """Fixture Visitatori e Host"""
    return [
        Visitatore.objects.create(
            username="alimeo", first_name="Anna", last_name="Rossi", email="a@a.it", registrazione=date(2024, 11, 1)
        ),
        Visitatore.objects.create(
            username="elimeo", first_name="Elsa", last_name="Verdi", email="b@b.it", registrazione=date(2024, 11, 2)
        ),
        Host.objects.create(
            username="host1", first_name="Carla", last_name="Bianchi", email="c@c.it", registrazione=date(2024, 1, 1)
        ),
        Host.objects.create(
            username="host2", first_name="Antonio", last_name="Viole", email="d@d.it", registrazione=date(2024, 1, 2)
        ),
    ]

@pytest.fixture()
def create_proprieta(db):
    """Fixture Proprieta"""
    h1 = Host.objects.get(username='host1')
    h2 = Host.objects.get(username='host2')
    return [
        Proprieta.objects.create(
            host=h1, descrizione="host principale", principale=True
        ),
        Proprieta.objects.create(
            host=h2, descrizione="host secondario"
        ),
    ]

@pytest.fixture()
def create_camere(db):
    """Fixture Camere"""
    p1 = Proprieta.objects.get(principale=True)
    p2 = Proprieta.objects.get(principale=False)
    return [
        Camera.objects.create(
            proprieta=p1, nome="camera 1", descrizione="descrizione camera 1",
        ),
        Camera.objects.create(
            proprieta=p1, nome="camera 2", descrizione="descrizione camera 2",
        ),
        Camera.objects.create(
            proprieta=p2, nome="camera 1", descrizione="descrizione camera 1",
        ),
        Camera.objects.create(
            proprieta=p2, nome="camera 2", descrizione="descrizione camera 2",
        ),
    ]

@pytest.fixture()
def create_prenotazioni(db):
    """Fixture Prenotazioni"""
    v = Visitatore.objects.get(id=1)
    c = Camera.objects.get(id=1)
    return [
        Prenotazione.objects.create(
            visitatore=v, camera=c,
            data_prenotazione=date(2024, 12, 1),
            stato_prenotazione=Prenotazione.PRENOTATA,
            richiesta="bla bla"
        ),
    ]

@pytest.fixture()
def create_calendario_prenotazioni(db):
    """Fixture CalendarioPrenotazione"""
    p = Prenotazione.objects.get(id=1)
    return [
        CalendarioPrenotazione.objects.create(
            prenotazione=p,
            data_inizio=date(2026, 1, 1),
            data_fine=date(2026, 1, 10),
        ),
    ]
