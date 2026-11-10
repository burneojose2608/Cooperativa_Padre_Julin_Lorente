from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from apps.usuarios.models.padron import PadronPrueba


# Identificadores generados matemáticamente: no representan socios reales.
PADRON_SINTETICO = (("0100000009", True), ("0100000017", True), ("0100000025", False))


class Command(BaseCommand):
    help = "Carga reproducible de padrón sintético en bases test_* o sprint1_*."

    def handle(self, *args, **options):
        if not connection.settings_dict["NAME"].startswith(("test_", "sprint1_")):
            raise CommandError("La carga solo se permite en una base aislada test_* o sprint1_*.")
        with transaction.atomic():
            for cedula, activo in PADRON_SINTETICO:
                fila, _ = PadronPrueba.objects.get_or_create(cedula=cedula, defaults={"activo": activo})
                if fila.activo != activo:
                    raise CommandError("El padrón existente difiere de la carga; no se sobrescribe.")
        self.stdout.write(self.style.SUCCESS("Padrón sintético preparado: 2 activos y 1 inactivo."))
