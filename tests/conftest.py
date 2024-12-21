from datetime import date

import pytest
from django.contrib.auth.models import User

from albdif.models import Visitatore, Host, Proprieta, Camera, Prenotazione, CalendarioPrenotazione


@pytest.fixture()
def create_utenti(db):
    """Fixture Utenti"""
    return [
        User.objects.create(
            username="alimeo", first_name="Anna", last_name="Rossi", email="a@a.it",
            password="A12345678."
        ),
        User.objects.create(
            username="elimeo", first_name="Elisa", last_name="Verdi", email="b@a.it",
            password="A12345678."
        ),
        User.objects.create(
            username="host1", first_name="Carla", last_name="Bianchi", email="c@a.it",
            password="A12345678."
        ),
        User.objects.create(
            username="host2", first_name="Antonio", last_name="Viole", email="d@a.it",
            password="A12345678."
        ),
    ]
@pytest.fixture()
def create_visitatori(create_utenti):
    """Fixture Visitatori e Host"""
    u1 = User.objects.get(username="alimeo")
    u2 = User.objects.get(username="elimeo")
    u3 = User.objects.get(username="host1")
    u4 = User.objects.get(username="host2")
    return [
        Visitatore.objects.create(
            utente=u1, registrazione=date(2024, 11, 1),
        ),
        Visitatore.objects.create(
            utente=u2, registrazione=date(2024, 11, 2)
        ),
        Host.objects.create(
            utente=u3, registrazione=date(2024, 1, 1)
        ),
        Host.objects.create(
            utente=u4, registrazione=date(2024, 1, 2)
        ),
    ]

@pytest.fixture()
def create_proprieta(db):
    """Fixture Proprieta"""
    h1 = Host.objects.get(utente__username='host1')
    h2 = Host.objects.get(utente__username='host2')
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
