from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

from django.core.cache import cache
from django.db import close_old_connections, connection
from django.test import TransactionTestCase
from rest_framework.test import APIClient

from apps.usuarios.models import Auditoria, Consentimiento, PadronPrueba, Socio, Usuario, UsuarioRol
from apps.usuarios.repositories import UsuarioRepository


class ConcurrenciaRegistroTests(TransactionTestCase):
    """Dos peticiones HTTP, conexiones y transacciones PostgreSQL independientes."""

    def setUp(self):
        cache.clear()
        self.assertEqual(connection.vendor, "postgresql")
        self.assertTrue(connection.settings_dict["NAME"].startswith("test_"))
        PadronPrueba.objects.bulk_create([
            PadronPrueba(cedula="0100000009", activo=True),
            PadronPrueba(cedula="0100000017", activo=True),
        ])

    def tearDown(self):
        # managed=False no participa en flush. Solo limpiar la base aislada;
        # TRUNCATE respeta la auditoría de solo inserción y conserva los roles.
        if connection.settings_dict["NAME"].startswith("test_"):
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE usuario RESTART IDENTITY CASCADE")
            PadronPrueba.objects.all().delete()

    def ejecutar_carrera(self, campo, *, cuenta_general=False):
        if cuenta_general:
            PadronPrueba.objects.all().delete()
        primero = dict(cedula="0100000009", nombre="Socio", apellido="Sintético",
                       correo="uno@example.test", username="socio01", telefono="0990000000",
                       fecha_nacimiento="2000-01-01", clave="Clave1234", acepta_terminos=True)
        segundo = {**primero, "cedula": "0100000017", "correo": "dos@example.test", "username": "socio02"}
        segundo[campo] = primero[campo]
        barrera = Barrier(2)
        consulta_real = UsuarioRepository.existe_username

        def sincronizar(username):
            existe = consulta_real(username)
            # Ambas peticiones completan las comprobaciones previas antes de
            # escribir; solo se añade sincronización, no se simula PostgreSQL.
            barrera.wait(timeout=15)
            return existe

        def enviar(datos):
            close_old_connections()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT pg_backend_pid()")
                    pid = cursor.fetchone()[0]
                respuesta = APIClient().post("/api/auth/registro/", datos, format="json")
                return pid, respuesta.status_code, respuesta.json()
            finally:
                connection.close()

        with patch.object(UsuarioRepository, "existe_username", side_effect=sincronizar):
            with ThreadPoolExecutor(max_workers=2) as executor:
                futuros = [executor.submit(enviar, datos) for datos in (primero, segundo)]
                resultados = [f.result(timeout=30) for f in futuros]
        self.assertEqual(len({r[0] for r in resultados}), 2)
        self.assertEqual(sorted(r[1] for r in resultados), [201, 409])
        rechazo = next(r[2] for r in resultados if r[1] == 409)
        self.assertEqual(rechazo["error"]["codigo"], "dato_duplicado")
        self.assertEqual(rechazo["error"]["campo"], campo)
        for modelo in (Usuario, Consentimiento):
            self.assertEqual(modelo.objects.count(), 1, modelo.__name__)
        for modelo in (Socio, UsuarioRol):
            self.assertEqual(modelo.objects.count(), 0 if cuenta_general else 1, modelo.__name__)
        self.assertEqual(Auditoria.objects.filter(resultado="EXITO").count(), 1)
        self.assertEqual(Auditoria.objects.filter(resultado="FALLO").count(), 1)

    def test_carrera_por_cedula(self):
        self.ejecutar_carrera("cedula")

    def test_carrera_por_correo(self):
        self.ejecutar_carrera("correo")

    def test_carrera_por_username(self):
        self.ejecutar_carrera("username")

    def test_carrera_por_cedula_de_cuenta_general(self):
        self.ejecutar_carrera("cedula", cuenta_general=True)
