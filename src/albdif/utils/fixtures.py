import random
import os
from datetime import date, timedelta
from typing import Any

from django.conf import settings
from django.db.models import Model
from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile

import factory.fuzzy
from factory.django import DjangoModelFactory

from albdif.config import env
from albdif.models import Visitatore, Proprieta, Camera, Prenotazione, CalendarioPrenotazione, Foto, Stagione, \
    Servizio, ServizioCamera, PrezzoCamera, RuoloUtente, RichiestaAdesione

prefix = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et "
          "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ")

suffix = ("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu "
          "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt "
          "mollit anim id est laborum.")


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"test-{n}")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: f"test-{n}@adpegasus.it")
    password = "password"  # noqa
    is_superuser = False
    is_staff = False

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class: "Model", *args: Any, **kwargs: Any) -> "User":
        """Crea oggetto e lo salva sul db"""
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class VisitatoreFactory(DjangoModelFactory):
    utente = factory.SubFactory(UserFactory)
    registrazione = factory.fuzzy.FuzzyDate(date(2024, 1, 1), date(2025, 12, 31))

    class Meta:
        model = Visitatore


class StagioneFactory(DjangoModelFactory):
    stagione = factory.fuzzy.FuzzyChoice(choices=['Bassa', 'Media', 'Alta'])
    data_inizio = factory.fuzzy.FuzzyDate(date(2025, 1, 1), date(2025, 12, 31))
    data_fine = factory.LazyAttribute(lambda obj: obj.data_inizio + timedelta(days=2))
    prezzo_default = factory.fuzzy.FuzzyDecimal(50.00, 500.00)

    class Meta:
        model = Stagione


class ProprietaPrincFactory(DjangoModelFactory):
    nome = "AD Pegasus"
    descrizione = "Questo è l'albergo diffuso principale ..."
    principale = True  # solo uno a True, gli altri a False

    class Meta:
        model = Proprieta


class ProprietaFactory(DjangoModelFactory):
    descrizione = factory.fuzzy.FuzzyText(prefix=prefix, length=12, suffix=suffix)
    principale = False  # solo uno a True, gli altri a False
    nome = factory.Faker('name')

    class Meta:
        model = Proprieta


class GroupFactory(DjangoModelFactory):
    name = factory.fuzzy.FuzzyText(length=10)
    permissions = factory.fuzzy.FuzzyText(length=10)

    class Meta:
        model = Group


class RuoloUtenteFactory(DjangoModelFactory):
    utente = factory.SubFactory(UserFactory)
    ruolo = factory.SubFactory(GroupFactory)
    ente = factory.SubFactory(ProprietaFactory)

    class Meta:
        model = RuoloUtente


class ServizioFactory(DjangoModelFactory):

    descrizione_servizio = factory.fuzzy.FuzzyChoice(choices=['toilette', 'wifi', 'phon', 'minibar', 'aria condizionata'])

    class Meta:
        model = Servizio


class CameraFactory(DjangoModelFactory):
    proprieta = factory.SubFactory(ProprietaFactory)
    nome = factory.Faker('name')
    descrizione = factory.fuzzy.FuzzyText(prefix=prefix, length=12, suffix=suffix)
    numero_posti_letto = factory.fuzzy.FuzzyInteger(1,6)

    class Meta:
        model = Camera


def random_decimal():
    return factory.fuzzy.FuzzyDecimal(1.0, 3.00, 2)


class ServizioCameraFactory(DjangoModelFactory):

    camera = factory.SubFactory(CameraFactory)
    servizio = factory.SubFactory(ServizioFactory)
    incluso = factory.fuzzy.FuzzyChoice(choices=[True, False])
    costo = factory.LazyAttribute(lambda obj: random_decimal().fuzz() if not obj.incluso else 0.0)

    class Meta:
        model = ServizioCamera


STATI = ["PR", "PG", "CA"]

class PrenotazioneFactory(DjangoModelFactory):
    visitatore = factory.SubFactory(VisitatoreFactory)
    camera = factory.SubFactory(CameraFactory)
    data_prenotazione = factory.fuzzy.FuzzyDate(start_date=date.today() - timedelta(days=30),
                                                end_date=date.today())
    stato_prenotazione = factory.Iterator(STATI)
    richiesta = factory.fuzzy.FuzzyText()
    costo_soggiorno = factory.fuzzy.FuzzyDecimal(10.0,100.00,2)
    data_pagamento = factory.fuzzy.FuzzyDate(start_date=date.today() - timedelta(days=30),
                                             end_date=date.today())
    numero_persone = factory.fuzzy.FuzzyInteger(1,6)
    data_stato = factory.LazyAttribute(lambda obj: obj.data_prenotazione + timedelta(minutes=10))

    class Meta:
        model = Prenotazione


class CalendarioPrenotazioneFactory(DjangoModelFactory):
    prenotazione = factory.SubFactory(PrenotazioneFactory)
    data_inizio = factory.fuzzy.FuzzyDate(start_date=date.today() - timedelta(days=30),
                                             end_date=date.today() + timedelta(days=365))
    data_fine = factory.fuzzy.FuzzyDate(start_date=date.today() - timedelta(days=30),
                                             end_date=date.today() + timedelta(days=365))

    class Meta:
        model = CalendarioPrenotazione


class FotoFactory(DjangoModelFactory):

    descrizione = factory.Faker('name')
    file = factory.LazyAttribute(lambda _: FotoFactory._get_random_file())

    class Meta:
        model = Foto

    @staticmethod
    def _get_random_file():
        """Ritorna un'immagine da una lista di immagini non coperte da copyright e presenti su static/img
        """
        directory = os.path.join(env("STATIC_ROOT"), 'img')
        try:
            valid_files = [
                f for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))
            ]
            if not valid_files:
                raise RuntimeError(f"La directory '{directory}' non contiene immagini valide.")

            # Seleziona un file casuale
            random_file_name = random.choice(valid_files)
            file_path = os.path.join(directory, random_file_name)

            # Leggi il contenuto del file
            with open(file_path, 'rb') as f:
                file_content = f.read()

            # Ritorna un oggetto ContentFile
            return ContentFile(file_content, name=f'foto_camera/{random_file_name}')
        except FileNotFoundError:
            raise RuntimeError(f"La directory '{directory}' non esiste.")
        except Exception as e:
            raise RuntimeError(f"Errore durante il caricamento dei file dalla directory '{directory}': {e}")

class PrezzoCameraFactory(DjangoModelFactory):

    camera = factory.SubFactory(CameraFactory)
    stagione = factory.SubFactory(StagioneFactory)
    prezzo = factory.fuzzy.FuzzyDecimal(10.00, 200.00, 2)

    class Meta:
        model = PrezzoCamera


class RichiestaAdesioneFactory(DjangoModelFactory):

    utente = factory.SubFactory(UserFactory)
    richiesta_adesione = factory.LazyAttribute(
        lambda _: ContentFile(b"%PDF-1.4\n%Fake PDF content", name="richiesta_adesione.pdf"))
    data_richiesta = factory.fuzzy.FuzzyDate(start_date=date.today() - timedelta(days=30),)
    approvazione_adesione = factory.LazyAttribute(
        lambda _: ContentFile(b"%PDF-1.4\n%Fake PDF content", name="approvazione_richiesta.pdf"))
    data_adesione = factory.fuzzy.FuzzyDate(start_date=date.today())

    class Meta:
        model = RichiestaAdesione