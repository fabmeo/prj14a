import pytest
from django.urls import reverse
from django.test import Client

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

