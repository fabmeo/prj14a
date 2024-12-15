import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from albdif.models import Visitatore, Host
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

