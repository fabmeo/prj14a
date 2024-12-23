from datetime import date, timedelta
from random import randint
from typing import Any

from django.conf import settings
from django.db.models import Model
from django.utils.text import slugify
from django.utils.translation import gettext as _

import factory.fuzzy
from factory.django import DjangoModelFactory

from albdif.models import Visitatore, Host, Proprieta, Camera, Prenotazione, CalendarioPrenotazione


# class UserFactory(DjangoModelFactory):
#     username = factory.Sequence(lambda n: f"name-{n}@example.com")
#     email = factory.Sequence(lambda n: f"name-{n}@example.com")
#     password = "password"  # noqa
#
#     class Meta:
#         model = settings.AUTH_USER_MODEL
#
#     @classmethod
#     def _create(cls, model_class: "Model", *args: Any, **kwargs: Any) -> "User":
#         """Crea oggetto e lo salva sul db"""
#         if cls._meta.django_get_or_create:
#             return cls._get_or_create(model_class, *args, **kwargs)
#
#         manager = cls._get_manager(model_class)
#         return manager.create_user(*args, **kwargs)


class VisitatoreFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"name-{n}@example.com")
    email = factory.Sequence(lambda n: f"name-{n}@example.com")
    password = "password"

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class: "Model", *args: Any, **kwargs: Any) -> "Visitatore":
        """Crea oggetto e lo salva sul db"""
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class HostFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"name-{n}@example.com")
    email = factory.Sequence(lambda n: f"name-{n}@example.com")
    password = "password"
    data_registrazione = factory.fuzzy.FuzzyDate(date(2025, 1, 1), date(2025, 12, 31))

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class: "Model", *args: Any, **kwargs: Any) -> "Host":
        """Crea oggetto e lo salva sul db"""
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class ProprietaFactory(DjangoModelFactory):
    host = factory.SubFactory(HostFactory)
    descrizione = "todo"
    principale = False # solo uno a True, gli altri a False

    class Meta:
        model = Proprieta


class CameraFactory(DjangoModelFactory):
    proprieta = factory.SubFactory(ProprietaFactory)
    nome = "todo"
    descrizione = "todo"
    services = dict

    class Meta:
        model = Camera


STATI = ["PR", "SC", "CA", "PG"]

class PrenotazioneFactory(DjangoModelFactory):
    visitatore = factory.SubFactory(VisitatoreFactory)
    camera = factory.SubFactory(CameraFactory)
    data_prenotazione = factory.fuzzy.FuzzyDate(date(2024, 1, 1), date(2024, 12, 31))
    stato_prenotazione = factory.Iterator(STATI)
    richiesta = "todo"

    class Meta:
        model = Prenotazione


class CalendarioPrenotazioneFactory(DjangoModelFactory):
    prenotazione = factory.SubFactory(PrenotazioneFactory)
    data_inizio = factory.fuzzy.FuzzyDate(date(2025, 1, 1), date(2025, 12, 31))
    data_fine = factory.fuzzy.FuzzyDate(date(2025, 1, 1), date(2025, 12, 31))

    class Meta:
        model = CalendarioPrenotazione
