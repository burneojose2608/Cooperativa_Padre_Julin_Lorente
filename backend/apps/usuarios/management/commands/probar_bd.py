"""Comprueba que Django está conectado a cooperativa_db y que ve las tablas."""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Prueba la conexión con PostgreSQL y cuenta las tablas de la base."

    def handle(self, *args, **options):
        with connection.cursor() as cur:
            cur.execute("SELECT current_database(), current_user, version()")
            base, usuario, version = cur.fetchone()
            cur.execute(
                "SELECT count(*) FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
            )
            tablas = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM rol")
            roles = cur.fetchone()[0]
        self.stdout.write(self.style.SUCCESS("Conexión correcta"))
        self.stdout.write(f"  Base de datos : {base}")
        self.stdout.write(f"  Usuario       : {usuario}")
        self.stdout.write(f"  PostgreSQL    : {version.split(',')[0]}")
        self.stdout.write(f"  Tablas        : {tablas}")
        self.stdout.write(f"  Roles         : {roles}")
