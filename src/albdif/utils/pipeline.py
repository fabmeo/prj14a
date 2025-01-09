from typing import Any
import datetime

from albdif.models import User
from django.contrib.auth.models import User


def registra_utente(user: User | None = None, **kwargs: Any) -> dict[str, Any]:
    if user:
        if not User.objects.filter(utente=user).exists():
            v = User.objects.create(utente=user, registrazione=datetime.datetime.now())
            v.save()
    return {}
