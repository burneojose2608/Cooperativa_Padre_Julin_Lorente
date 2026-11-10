from pathlib import Path
from datetime import date

from django.conf import settings
from django.db import DatabaseError, connection, transaction
from django.test import TransactionTestCase

from apps.usuarios.models import Usuario
from apps.usuarios.repositories import UsuarioRepository


class EsquemaRegistroTests(TransactionTestCase):
    def crear(self, **cambios):
        datos = dict(cedula="0100000009", nombre="Socio", apellido="Prueba",
                     correo="uno@example.test", username="socio01", telefono="0990000000",
                     fecha_nacimiento=date(2000, 1, 1), clave="Clave1234")
        return UsuarioRepository.crear(**{**datos, **cambios})

    def ejecutar(self, ruta):
        self.assertTrue(connection.settings_dict["NAME"].startswith("test_"))
        with connection.cursor() as cursor:
            cursor.execute((Path(settings.BASE_DIR) / "sql" / ruta).read_text(encoding="utf-8"))

    def existe_padron(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('public.padron_prueba') IS NOT NULL")
            return cursor.fetchone()[0]

    def test_reversion_y_reaplicacion_en_postgresql(self):
        self.ejecutar("reversiones/05_registro_padron_unicidad.sql")
        try:
            self.assertFalse(self.existe_padron())
        finally:
            self.ejecutar("05_registro_padron_unicidad.sql")
        self.assertTrue(self.existe_padron())

    def test_conflictos_abortan_sin_alterar_cuentas_ni_esquema(self):
        self.ejecutar("reversiones/05_registro_padron_unicidad.sql")
        try:
            self.crear()
            self.crear(cedula="0100000017", correo=" UNO@EXAMPLE.TEST ", username="otro02")
            cantidad = Usuario.objects.count()
            with self.assertRaises(DatabaseError):
                self.ejecutar("05_registro_padron_unicidad.sql")
            connection.rollback()
            self.assertFalse(self.existe_padron())
            self.assertEqual(Usuario.objects.count(), cantidad)
        finally:
            connection.rollback()
            Usuario.objects.all().delete()
            self.ejecutar("05_registro_padron_unicidad.sql")

    def test_sql06_actualiza_instalacion_anterior_y_reversion_no_borra_cuentas(self):
        self.ejecutar("reversiones/06_cedula_formato_acordado.sql")
        try:
            with self.assertRaises(DatabaseError), transaction.atomic():
                self.crear(cedula="0100000008")
            self.ejecutar("06_cedula_formato_acordado.sql")
            self.crear(cedula="0100000008")
            with self.assertRaises(DatabaseError):
                self.ejecutar("reversiones/06_cedula_formato_acordado.sql")
            connection.rollback()
            self.assertTrue(Usuario.objects.filter(cedula="0100000008").exists())
        finally:
            connection.rollback()
            Usuario.objects.all().delete()
            self.ejecutar("06_cedula_formato_acordado.sql")
