from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from threading import Barrier, Event
from unittest.mock import patch

from django.core.management import call_command
from django.db import close_old_connections, connection
from django.test import TransactionTestCase

from apps.usuarios.models import Rol, RolPermiso, Permiso, Socio
from apps.plataforma.models import CodigoReferido, EnvioNotificacion
from apps.plataforma.notificaciones import notificar, procesar_uno
from .test_sprint2 import crear_usuario


def en_conexion(funcion):
    close_old_connections()
    try:
        return funcion()
    finally:
        connection.close()


class ConcurrenciaSprint2Tests(TransactionTestCase):
    def setUp(self):
        self.assertTrue(connection.settings_dict["NAME"].startswith("test_"))

    def tearDown(self):
        if connection.settings_dict["NAME"].startswith("test_"):
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE usuario RESTART IDENTITY CASCADE")

    def test_dos_peticiones_obtienen_el_mismo_codigo_sin_duplicados(self):
        from django.utils import timezone
        u = crear_usuario(901, "Socio")
        socio = Socio.objects.create(usuario=u, codigo_socio="SOC-900001", validado_en=timezone.now())
        barrera = Barrier(2)
        def obtener():
            barrera.wait(timeout=10)
            return CodigoReferido.generar_para(socio).valor
        with ThreadPoolExecutor(max_workers=2) as equipo:
            a, b = [equipo.submit(en_conexion, obtener) for _ in range(2)]
            self.assertEqual(a.result(timeout=20), b.result(timeout=20))
        self.assertEqual(CodigoReferido.objects.filter(socio=socio, estado="ACTIVO").count(), 1)

    def test_dos_trabajadores_no_reclaman_el_mismo_envio(self):
        u = crear_usuario(902)
        n = notificar(u, "PERFIL_ACTUALIZADO", "Prueba")
        EnvioNotificacion.objects.filter(notificacion=n, canal="INTERNA").update(estado="OMITIDA")
        iniciado = Event(); terminar = Event()
        def enviar(*args, **kwargs):
            iniciado.set()
            if not terminar.wait(timeout=10):
                raise RuntimeError("El segundo trabajador no terminó")
            return 1
        with patch("apps.plataforma.notificaciones.send_mail", side_effect=enviar) as correo:
            with ThreadPoolExecutor(max_workers=2) as equipo:
                primero = equipo.submit(en_conexion, procesar_uno)
                self.assertTrue(iniciado.wait(timeout=10))
                try:
                    segundo = equipo.submit(en_conexion, procesar_uno)
                    self.assertFalse(segundo.result(timeout=10))
                finally:
                    terminar.set()
                self.assertTrue(primero.result(timeout=10))
            self.assertEqual(correo.call_count, 1)

    def test_actualizacion_repetida_conserva_permiso_revocado(self):
        rol = Rol.objects.get(nombre="Gestor de contenidos")
        permiso = Permiso.objects.get(modulo="contenidos", accion="publicar")
        vinculo = RolPermiso.objects.filter(rol=rol, permiso=permiso)
        existia = vinculo.exists()
        vinculo.delete()
        try:
            for _ in range(2):
                call_command("actualizar_sprint2", stdout=StringIO())
            self.assertFalse(RolPermiso.objects.filter(rol=rol, permiso=permiso).exists())
        finally:
            if existia:
                RolPermiso.objects.get_or_create(rol=rol, permiso=permiso)
