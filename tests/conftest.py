from datetime import date

import pytest
from albdif.models import Visitatore, Host


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