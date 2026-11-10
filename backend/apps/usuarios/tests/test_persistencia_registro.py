from datetime import date
from io import StringIO

from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.usuarios.models.padron import PadronPrueba
from apps.usuarios.repositories import UsuarioRepository


class PersistenciaRegistroTests(TestCase):
    def crear(self, **cambios):
        datos = dict(cedula="0100000009", nombre="Sintético", apellido="Prueba",
                     correo="uno@example.test", username="uno01", telefono="0990000000",
                     fecha_nacimiento=date(2000, 1, 1), clave="Clave1234")
        return UsuarioRepository.crear(**{**datos, **cambios})

    def test_carga_reproducible_y_estados_independientes(self):
        for _ in range(2):
            call_command("cargar_padron_sintetico", stdout=StringIO())
        self.assertEqual(PadronPrueba.objects.count(), 3)
        self.assertEqual(PadronPrueba.objects.filter(activo=True).count(), 2)

    def test_unicidad_directa_de_cedula_correo_y_username(self):
        self.crear()
        for cambios in (
            dict(correo="dos@example.test", username="dos02"),
            dict(cedula="0100000017", correo=" UNO@EXAMPLE.TEST ", username="dos02"),
            dict(cedula="0100000017", correo="dos@example.test", username=" UNO01 "),
        ):
            with self.subTest(campos=tuple(cambios)), self.assertRaises(IntegrityError):
                with transaction.atomic():
                    self.crear(**cambios)

    def test_sql_acepta_diez_digitos_sin_verificador(self):
        usuario = self.crear(cedula="0100000008")
        self.assertEqual(usuario.cedula, "0100000008")

    def test_sql_rechaza_caracteres_no_numericos(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.crear(cedula="010000000x")
