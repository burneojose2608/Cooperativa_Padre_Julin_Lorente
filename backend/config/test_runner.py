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
        for conexion in connections.all():
            nombre = (conexion.settings_dict.get("TEST", {}).get("NAME")
                      or "test_" + conexion.settings_dict["NAME"])
            if not nombre.startswith("test_"):
                raise RuntimeError("Las pruebas requieren una base aislada con prefijo test_.")
        config = super().setup_databases(**kwargs)
        for conexion in connections.all():
            with conexion.cursor() as cursor:
                for script in sorted(SQL_DIR.glob("*.sql")):
                    cursor.execute(script.read_text(encoding="utf-8"))
        return config
