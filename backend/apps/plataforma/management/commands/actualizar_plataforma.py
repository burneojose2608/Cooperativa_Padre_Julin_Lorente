from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = 'Aplica la evolución aditiva 08 sin reiniciar datos ni permisos existentes.'

    def handle(self, *args, **options):
        if connection.in_atomic_block:
            raise CommandError('Ejecute la actualización fuera de una transacción de aplicación.')
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM version_esquema WHERE version='sprint-2')")
            if not cursor.fetchone()[0]:
                raise CommandError('Primero debe aplicar actualizar_sprint2.')
            cursor.execute((Path(settings.BASE_DIR) / 'sql/08_alcance_completo.sql').read_text(encoding='utf-8'))
        self.stdout.write(self.style.SUCCESS('Plataforma actualizada. Datos existentes conservados.'))
