from io import StringIO

from django.core.management import call_command
from django.db import connection
from django.test import TestCase
from rest_framework.test import APIClient

from apps.plataforma import models as m
from apps.usuarios.models import Usuario


class DemostracionTests(TestCase):
    def test_carga_repetible_visible_y_sin_envios(self):
        base = connection.settings_dict["NAME"]
        self.assertTrue(base.startswith("test_"))
        for _ in range(2):
            call_command("poblar_demostracion", base=base, stdout=StringIO())

        socio_demo = Usuario.objects.get(username="pjl_catalogo_demo")
        self.assertFalse(socio_demo.has_usable_password())
        cliente = APIClient()
        cliente.force_authenticate(socio_demo)
        for recurso in ("campanas", "capacitaciones", "talleres", "juegos", "retos",
                        "convenios", "beneficios", "sorteos", "comunidad"):
            with self.subTest(recurso=recurso):
                respuesta = cliente.get(f"/api/plataforma/negocio/{recurso}/")
                self.assertEqual(respuesta.status_code, 200, respuesta.data)
                self.assertEqual(len(respuesta.data["resultados"]), 1)
        self.assertEqual(len(cliente.get("/api/plataforma/publicaciones/").data), 3)
        self.assertEqual(m.Certificado.objects.count(), 1)
        self.assertEqual(m.ParticipacionSorteo.objects.count(), 1)
        self.assertFalse(m.EnvioNotificacion.objects.exists())
        self.assertFalse(m.SolicitudContacto.objects.exists())
