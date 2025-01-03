from datetime import date
from decimal import Decimal

from django_webtest import DjangoTestApp

from albdif.models import Proprieta, Stagione, Camera, PrezzoCamera
from albdif.utils.fixtures import CameraFactory, StagioneFactory, PrezzoCameraFactory


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
    PrezzoCameraFactory(camera=c1, stagione=s1, prezzo=45.63)
    assert c1.prezzo_bassa_stagione == Decimal("45.63")
