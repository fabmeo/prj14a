from datetime import timedelta
from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone

import pytest
from django_webtest import DjangoTestApp

if TYPE_CHECKING:
    from albdif.models import Visitatore, Host, Proprieta, Camera, Prenotazione, CalendarioPrenotazione


def test_home(app: "DjangoTestApp"):
    url = reverse("albdif:home")
    res = app.get(url, user="")
    assert res.status_code == 200

    res = app.get(url)
    assert res.status_code == 200