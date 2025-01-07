from typing import Any

from django.contrib.auth.models import Permission
from django.core.management import BaseCommand, call_command
from django.db.transaction import atomic
from albdif.models import Group


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = []

    def handle(self, *args: Any, **options: Any) -> None:

        print("Esegui le migrazioni")
        call_command("migrate")

        print("Crea il ruolo Visitatore")
        visitatori, __ = Group.objects.get_or_create(name="Visitatore")
        permissions = Permission.objects.filter(
            content_type__app_label="albdif",
            codename__in=["consulta_catalogo", ],
        )
        visitatori.permissions.add(*permissions)

        print("Crea il ruolo Titolare")
        titolari, __ = Group.objects.get_or_create(name="Titolare")
        permissions = Permission.objects.filter(
            content_type__app_label="albdif",
            codename__in=["crea_proprieta", "consulta_catalogo",],
        )
        titolari.permissions.add(*permissions)
