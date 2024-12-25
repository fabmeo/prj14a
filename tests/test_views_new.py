from datetime import timedelta, date
from typing import TYPE_CHECKING

from django.urls import reverse

import pytest
from django_webtest import DjangoTestApp

from albdif.utils.fixtures import UserFactory, VisitatoreFactory, HostFactory, CalendarioPrenotazioneFactory, \
    PrenotazioneFactory, CameraFactory, ProprietaFactory

if TYPE_CHECKING:
    from albdif.models import Visitatore, Host, Proprieta, Camera, Prenotazione, CalendarioPrenotazione

@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def visitatore(db):
    return VisitatoreFactory()

@pytest.fixture
def host(db):
    return HostFactory()

def test_home(app: "DjangoTestApp"):
    url = reverse("albdif:home")
    response = app.get(url, user="")
    assert response.status_code == 200

    response = app.get(url)
    assert response.status_code == 200
    assert 'albdif/home.html' in [t.name for t in response.templates]
    assert 'Homepage AD Pegaso' in response.content.decode()


def test_login_ko(app: "DjangoTestApp"):
    url = reverse("albdif:login")
    app.set_user(None)
    response = app.get(url)
    response.form["username"] = "pippo"
    response.form["password"] = "pluto"
    response = response.form.submit()
    assert response.status_code == 200
    assert "Username o password errate!" in response.content.decode()


def test_login_ok(app: "DjangoTestApp", user):
    url = reverse("albdif:login")
    app.set_user(None)
    response = app.get(url)
    #u = User.objects.all().first()
    response.form["username"] = user.username
    response.form["password"] = "password"
    response = response.form.submit()
    assert response.status_code == 302
    assert response.url == reverse('albdif:home')
    assert not "Username o password errate!" in response.content.decode()


def test_profilo_ok(app: "DjangoTestApp", user):
    url = reverse("albdif:profilo", kwargs={'pk': user.pk})
    response = app.get(url)
    assert response.status_code == 200
    assert 'Le tue prenotazioni' in response.content.decode()


def test_logout(app: "DjangoTestApp"):
    url = reverse("albdif:logout")
    response = app.post(url)
    assert response.status_code == 302
    assert response.url == reverse('albdif:home')


def test_profilo_denied(app: "DjangoTestApp", user):
    s = UserFactory()
    url = reverse("albdif:profilo", kwargs={'pk': s.pk})
    response = app.get(url)
    assert response.status_code == 302
    assert not 'Le tue prenotazioni' in response.content.decode()


def test_proprieta_partner_view(app: "DjangoTestApp"):
    url = reverse('albdif:proprieta_partner')
    response = app.get(url)
    assert response.status_code == 200
    assert 'albdif/proprieta_list.html' in [t.name for t in response.templates]
    assert 'Lista dei Partner' in response.content.decode()


def test_calendario_passato(app: "DjangoTestApp", user):
    pr1 = ProprietaFactory()
    v1 = VisitatoreFactory(utente=user)
    c1 = CameraFactory(proprieta=pr1)
    p1 = PrenotazioneFactory(
        visitatore=v1,
        camera=c1,
        data_prenotazione=date(2023, 12, 1),
        stato_prenotazione="PG"
    )
    CalendarioPrenotazioneFactory(
        prenotazione=p1,
        data_inizio=date(2024, 1, 1),
        data_fine=date(2024, 1, 2))

    url = reverse("albdif:profilo", kwargs={'pk': user.pk})
    response = app.get(url)
    assert response.status_code == 200
    assert 'Storico' in response.content.decode()


def test_prenotazione_passata(app: "DjangoTestApp", user):
    pr1 = ProprietaFactory()
    v1 = VisitatoreFactory(utente=user)
    c1 = CameraFactory(proprieta=pr1)

    url = reverse("albdif:prenota_camera", kwargs={'id1': v1.pk, 'id2': c1.pk})
    response = app.get(url)
    assert response.status_code == 200
    assert 'Stai prenotando la camera' in response.content.decode()

    response.form["richiesta"] = "bla bla"
    response.form["data_inizio"] = date(2024,1,1)
    response.form["data_fine"] = date(2026,1,2)
    response = response.form.submit()
    assert 'La data inizio deve essere futura' in response.content.decode()

    response.form["richiesta"] = "bla bla"
    response.form["data_inizio"] = date(2026,1,1)
    response.form["data_fine"] = date(2024,1,2)
    response = response.form.submit()
    assert 'La data fine non può essere antecedente alla data inizio' in response.content.decode()

def test_prenotazione_negata(app: "DjangoTestApp", user):
    u1 = UserFactory()
    pr1 = ProprietaFactory()
    v1 = VisitatoreFactory(utente=u1)
    c1 = CameraFactory(proprieta=pr1)
    p1 = PrenotazioneFactory(
        visitatore=v1,
        camera=c1,
        data_prenotazione=date(2024, 12, 25),
        stato_prenotazione="PR"
    )
    CalendarioPrenotazioneFactory(
        prenotazione=p1,
        data_inizio=date(2025, 2, 1),
        data_fine=date(2025, 2, 2))

    v = VisitatoreFactory(utente=user)
    url = reverse("albdif:prenota_camera", kwargs={'id1': v.pk, 'id2': c1.pk})
    response = app.get(url)
    assert response.status_code == 200
    assert 'Stai prenotando la camera' in response.content.decode()

    response.form["richiesta"] = "bla bla"
    response.form["data_inizio"] = date(2025,2,1)
    response.form["data_fine"] = date(2025,2,1)
    response = response.form.submit()
    assert "Spiacenti: la camera è stata già prenotata" in response.content.decode()

def test_prenotazione_sovrapposta(app: "DjangoTestApp", user):
    pr1 = ProprietaFactory()
    v1 = VisitatoreFactory(utente=user)
    c1 = CameraFactory(proprieta=pr1)
    p1 = PrenotazioneFactory(
        visitatore=v1,
        camera=c1,
        data_prenotazione=date(2024, 12, 25),
        stato_prenotazione="PR"
    )
    CalendarioPrenotazioneFactory(
        prenotazione=p1,
        data_inizio=date(2025, 2, 1),
        data_fine=date(2025, 2, 2))

    url = reverse("albdif:prenota_camera", kwargs={'id1': v1.pk, 'id2': c1.pk})
    response = app.get(url)
    assert response.status_code == 200
    assert 'Stai prenotando la camera' in response.content.decode()

    response.form["richiesta"] = "bla bla"
    response.form["data_inizio"] = date(2025,2,1)
    response.form["data_fine"] = date(2025,2,1)
    response = response.form.submit()
    assert "Spiacenti: le date si sovrappongono ad un" in response.content.decode()
