from django.core.cache import cache
from django.db import OperationalError, ProgrammingError
from django.test import SimpleTestCase
from rest_framework.test import APIClient

from config.manejo_errores import manejador_de_errores


class ErroresSegurosTests(SimpleTestCase):
    def test_fallos_no_exponen_detalles_en_respuesta_ni_en_log(self):
        secreto = "SELECT clave_hash FROM usuario; /ruta/interna clave=NoDebeAparecer"
        for clase, estado in ((RuntimeError, 500), (ProgrammingError, 500), (OperationalError, 503)):
            with self.subTest(tipo=clase.__name__), self.assertLogs("config.manejo_errores", level="ERROR") as logs:
                respuesta = manejador_de_errores(clase(secreto), {})
            self.assertEqual(respuesta.status_code, estado)
            self.assertNotIn(secreto, str(respuesta.data))
            self.assertNotIn("NoDebeAparecer", " ".join(logs.output))
            self.assertIn(clase.__name__, " ".join(logs.output))


class FormatoRegistroTests(SimpleTestCase):
    def setUp(self):
        cache.clear()
        self.cliente = APIClient()

    def test_json_mal_formado_se_rechaza_antes_del_servicio(self):
        respuesta = self.cliente.post("/api/auth/registro/", '{"cedula":', content_type="application/json")
        self.assertEqual(respuesta.status_code, 400)

    def test_todos_los_campos_son_obligatorios_en_el_servidor(self):
        respuesta = self.cliente.post("/api/auth/registro/", {}, format="json")
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(set(respuesta.json()), {"cedula", "nombre", "apellido", "correo", "username",
                                                "telefono", "fecha_nacimiento", "clave", "acepta_terminos"})
