import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from albdif.models import Visitatore, Host, Proprieta, Camera, Prenotazione, CalendarioPrenotazione
from tests.conftest import create_visitatori

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestLogin:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_ok(self):
        response = self.client.post(reverse('albdif:login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        assert response.status_code == 302
        assert response.url == reverse('albdif:home')

    def test_login_ko(self):
        response = self.client.post(reverse('albdif:login'), {
            'username': 'testuser',
            'password': 'password_ko'
        })
        assert response.status_code == 200
        assert "Username o password errate!" in response.content.decode()

    def test_login_utente_inattivo(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('albdif:login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        assert response.status_code == 200
        #assert "L'account non è attivo!" in response.content.decode()
        assert "Username o password errate!" in response.content.decode()


@pytest.mark.django_db
class TestProfilo:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_profilo_ok(self):
        response = self.client.post(reverse('albdif:login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        assert response.status_code == 302
        assert response.url == reverse('albdif:home')

    def test_profilo_ko(self, create_visitatori):
        response = self.client.post(reverse('albdif:login'), {
            'username': 'alimeo',
            'password': 'A12345678.'
        })
        assert response.status_code == 200

        response = self.client.post(reverse('albdif:profilo', kwargs={'pk': 2}))
        assert response.status_code == 403


@pytest.mark.django_db
class TestHome:

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
class TestUtenti:
    def test_presenza_utenti(self, create_visitatori):
        v = Visitatore.objects.get(utente__username='alimeo')
        assert str(v) == "Rossi Anna"
        h = Host.objects.get(utente__username='host1')
        assert str(h) == "Bianchi Carla"


@pytest.mark.django_db
class TestProprieta:
    def test_presenza_proprieta(self, create_visitatori, create_proprieta):
        p = Proprieta.objects.get(descrizione="host principale")
        assert p.principale
        assert str(p) == "host principale"
        p = Proprieta.objects.get(descrizione="host secondario")
        assert not p.principale
        assert str(p) == "host secondario"


@pytest.mark.django_db
class TestCamere:
    def test_presenza_camere(self, create_visitatori, create_proprieta, create_camere):
        c = Camera.objects.filter(proprieta__principale=True).count()
        assert c > 0
        c1 = Camera.objects.get(proprieta__principale=True, id=1)
        assert str(c1) == "camera 1 di host principale"
        c = Camera.objects.filter(proprieta__principale=False).count()
        assert c > 0
        c1 = Camera.objects.get(proprieta__principale=False, id=4)
        assert str(c1) == "camera 2 di host secondario"


@pytest.mark.django_db
class TestPrenotazione:
    def test_presenza_prenotazione(self, create_visitatori, create_proprieta, create_camere, create_prenotazioni, create_calendario_prenotazioni):
        p = Prenotazione.objects.get(id=1)
        assert p.stato_prenotazione == Prenotazione.PRENOTATA
        assert str(p) == "Rossi Anna PR camera 1 di host principale"

    def test_presenza_calendario(self, create_visitatori, create_proprieta, create_camere, create_prenotazioni, create_calendario_prenotazioni):
        c = CalendarioPrenotazione.objects.filter(id=1).count()
        assert c > 0
        c = CalendarioPrenotazione.objects.get(id=1)
        assert str(c) == "Rossi Anna PR camera 1 di host principale 2026-01-01 2026-01-10"
