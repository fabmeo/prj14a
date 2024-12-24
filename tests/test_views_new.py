from datetime import timedelta
from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone

import pytest
from django_webtest import DjangoTestApp

from albdif.utils.fixtures import UserFactory, VisitatoreFactory, HostFactory
from albdif.models import User

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
