"""Al correr los tests, crea una base temporal `test_<nombre>` y le carga
tus scripts SQL (carpeta sql/). Así las pruebas usan las mismas tablas reales
y tu base cooperativa_db nunca se toca."""
from pathlib import Path

from django.conf import settings
from django.db import connections
from django.test.runner import DiscoverRunner

SQL_DIR = Path(settings.BASE_DIR) / "sql"


class RunnerConScriptsSQL(DiscoverRunner):
    def setup_databases(self, **kwargs):
        aliases = set(kwargs.get("aliases", connections))
        if not aliases:
            return super().setup_databases(**kwargs)
        for conexion in connections.all():
            if conexion.alias not in aliases:
                continue
            nombre = (conexion.settings_dict.get("TEST", {}).get("NAME")
                      or "test_" + conexion.settings_dict["NAME"])
            if not nombre.startswith("test_"):
                raise RuntimeError("Las pruebas requieren una base aislada con prefijo test_.")
        config = super().setup_databases(**kwargs)
        for conexion in connections.all():
            if conexion.alias not in aliases:
                continue
            # Comprobar el nombre real después de que Django cambie a la base de pruebas.
            # SimpleTestCase no crea bases: nunca cargar scripts en la conexión de trabajo.
            if not conexion.settings_dict["NAME"].startswith("test_"):
                raise RuntimeError("Se impidió cargar scripts SQL fuera de una base test_.")
            with conexion.cursor() as cursor:
                for script in sorted(SQL_DIR.glob("*.sql")):
                    cursor.execute(script.read_text(encoding="utf-8"))
        return config
