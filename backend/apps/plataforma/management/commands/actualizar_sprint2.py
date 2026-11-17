from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Aplica únicamente la actualización aditiva 07 del Sprint 2."

    def handle(self, *args, **options):
        if connection.in_atomic_block:
            from django.core.management.base import CommandError
            raise CommandError("Ejecuta esta actualización fuera de una transacción de aplicación.")
        sql = (Path(settings.BASE_DIR) / "sql" / "07_sprint_2.sql").read_text(encoding="utf-8")
        with connection.cursor() as cursor:
            cursor.execute(sql)
        from apps.usuarios.models import Socio
        from apps.plataforma.models import CodigoReferido
        for socio in Socio.objects.filter(validado_en__isnull=False, usuario__estado="ACTIVA").iterator():
            CodigoReferido.generar_para(socio)
        self.stdout.write(self.style.SUCCESS("Esquema del Sprint 2 actualizado sin reiniciar los datos."))
