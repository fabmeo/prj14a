from typing import Any
import datetime

from albdif.models import Visitatore, RuoloUtente
from django.contrib.auth.models import User, Group
from django.db import transaction


@transaction.atomic
def registra_utente(user: User | None = None, **kwargs: Any) -> dict[str, Any]:
    if user:
        if not Visitatore.objects.filter(utente=user).exists():
            try:
                # crea il visitatore legandolo all'utente appena registrato
                v = Visitatore.objects.create(utente=user, registrazione=datetime.datetime.now())
                # salva l'istanza
                v.save()
                # preleva il gruppo/ruolo dell'utente
                gruppo=Group.objects.filter(name="Visitatore")
                # crea il ruolo dell'utente sul sito (i visitatori hanno l'ente a null
                ru = RuoloUtente.objects.create(utente=user, ruolo=gruppo, ente=None)
                ru.save()
            except Exception as e:
                raise "Errore: non è stato possibile creare l'utente, rivolgersi all'assistenza"
    return {}
