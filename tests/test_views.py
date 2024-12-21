import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from albdif.models import Visitatore, Host, Proprieta, Camera, Prenotazione, CalendarioPrenotazione
from tests.conftest import create_visitatori

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestMyView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('albdif:home'))
        assert response.status_code == 200
        assert 'albdif/home.html' in [t.name for t in response.templates]
        assert 'Homepage AD Pegaso' in response.content.decode()

    def test_proprieta_partner_view(self):
        response = self.client.get(reverse('albdif:proprieta_partner'))
        assert response.status_code == 200
        assert 'albdif/proprieta_list.html' in [t.name for t in response.templates]
        assert 'Lista dei Partner' in response.content.decode()


@pytest.mark.django_db
class TestUsers:
    #pytestmark = pytest.mark.django_db
    def test_presenza_utenti(self, create_visitatori):
        v = Visitatore.objects.get(username='alimeo')
        assert not v.is_superuser
        h = Host.objects.get(username='host1')
        assert not h.is_superuser

@pytest.mark.django_db
class TestProprieta:
    #pytestmark = pytest.mark.django_db
    def test_presenza_proprieta(self, create_visitatori, create_proprieta):
        p = Proprieta.objects.get(descrizione="host principale")
        assert p.principale
        p = Proprieta.objects.get(descrizione="host secondario")
        assert not p.principale

@pytest.mark.django_db
class TestProprieta:
    #pytestmark = pytest.mark.django_db
    def test_presenza_camere(self, create_visitatori, create_proprieta, create_camere):
        c = Camera.objects.filter(proprieta__principale=True).count()
        assert c > 0
        c = Camera.objects.filter(proprieta__principale=False).count()
        assert c > 0

@pytest.mark.django_db
class TestPrenotazione:
    #pytestmark = pytest.mark.django_db
    def test_presenza_prenotazione(self, create_visitatori, create_proprieta, create_camere, create_prenotazioni, create_calendario_prenotazioni):
        p = Prenotazione.objects.get(id=1)
        assert p.stato_prenotazione == Prenotazione.PRENOTATA
        c = CalendarioPrenotazione.objects.filter(id=1).count()
        assert c > 0
