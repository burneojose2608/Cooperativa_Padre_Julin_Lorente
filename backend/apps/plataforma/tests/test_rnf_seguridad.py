"""Pruebas de requisitos no funcionales y controles de seguridad OWASP (T-037 / RNF-08, RNF-09, RNF-17, RNF-20, RNF-24, RNF-26)."""
from datetime import timedelta
from io import BytesIO
from tempfile import TemporaryDirectory
import time

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.plataforma import models as m, negocio as n
from apps.plataforma.tests.test_sprint2 import crear_usuario
from apps.usuarios.models import Auditoria
from apps.usuarios.services.codigos_socio import ServicioSocios


class RequisitosNoFuncionalesYSeguridadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = crear_usuario(9501, "Administrador")
        cls.marketing = crear_usuario(9502, "Responsable de Marketing")
        cls.usuario = crear_usuario(9503, "Socio")
        cls.otro = crear_usuario(9504, "Socio")
        cls.socio = ServicioSocios.crear_socio_validado(cls.usuario)
        cls.socio2 = ServicioSocios.crear_socio_validado(cls.otro)
        cls.codigo = m.CodigoReferido.generar_para(cls.socio)
        for actividad in m.ReglaPuntos.ACTIVIDADES:
            m.ReglaPuntos.objects.create(
                tipo_actividad=actividad, puntos=50, limite_periodo=50, periodo="DIA",
                vigente_desde=timezone.localdate(), version=f"rnf-{actividad}",
            )

    def setUp(self):
        self.c = APIClient()
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        cfg = override_settings(MEDIA_ROOT=self.tmp.name)
        cfg.enable()
        self.addCleanup(cfg.disable)

    def test_rnf08_endpoint_salud_monitoreo(self):
        r = self.c.get("/api/salud/")
        self.assertEqual(r.status_code, 200)
        datos = r.json()
        self.assertEqual(datos["estado"], "ok")
        self.assertEqual(datos["base_datos"], "ok")
        self.assertIn("fecha", datos)

    def test_rnf09_cabeceras_seguridad_y_hsts_cuando_exigir_https(self):
        with override_settings(
            SECURE_SSL_REDIRECT=True,
            SECURE_HSTS_SECONDS=31536000,
            SECURE_HSTS_INCLUDE_SUBDOMAINS=True,
            SECURE_HSTS_PRELOAD=True,
            SECURE_CONTENT_TYPE_NOSNIFF=True,
            X_FRAME_OPTIONS="DENY",
        ):
            r_http = self.c.get("/api/salud/")
            self.assertEqual(r_http.status_code, 301)
            self.assertTrue(r_http["Location"].startswith("https://"))

            r_https = self.c.get("/api/salud/", secure=True)
            self.assertEqual(r_https.status_code, 200)
            self.assertIn("max-age=31536000", r_https["Strict-Transport-Security"])
            self.assertIn("includeSubDomains", r_https["Strict-Transport-Security"])
            self.assertEqual(r_https["X-Content-Type-Options"], "nosniff")
            self.assertEqual(r_https["X-Frame-Options"], "DENY")

    def test_rnf20_owasp_prevencion_inyeccion_sql_y_manipulacion_parametros(self):
        self.c.force_authenticate(self.marketing)
        payload_sqli = "'; DROP TABLE usuario; --"
        r = self.c.get("/api/plataforma/negocio/referidos/", {"estado": payload_sqli})
        self.assertEqual(r.status_code, 400)
        r_camp = self.c.get("/api/plataforma/negocio/referidos/", {"campana": "1 OR 1=1"})
        self.assertEqual(r_camp.status_code, 400)
        r_rep = self.c.get("/api/plataforma/negocio/reportes/", {"tipo": "referidos", "desde": "2026-01-01' OR '1'='1"})
        self.assertEqual(r_rep.status_code, 400)
        # Verificación de integridad de tablas tras intentos de SQLi.
        self.assertEqual(self.c.get("/api/salud/").status_code, 200)

        # Manipulación de parámetros / mass assignment en endpoints de negocio.
        self.c.force_authenticate(self.usuario)
        r_mass = self.c.post("/api/plataforma/negocio/comunidad/", {
            "texto": "Texto normal", "estado_moderacion": "OCULTA", "usuario": self.otro.pk,
        }, format="json")
        self.assertEqual(r_mass.status_code, 400)

    def test_rnf17_errores_comprensibles_sin_trazas_ni_rutas_internas(self):
        self.c.force_authenticate(self.usuario)
        for ruta in (
            "/api/plataforma/negocio/inexistente/",
            "/api/plataforma/negocio/capacitaciones/999999/aula/",
            "/api/plataforma/negocio/certificados/999999/pdf/",
        ):
            r = self.c.get(ruta)
            self.assertIn(r.status_code, (400, 403, 404))
            texto = r.content.decode("utf-8", errors="ignore")
            for prohibido in ("Traceback", "File \"", "SELECT ", "django.", "backend\\"):
                self.assertNotIn(prohibido, texto)

    def test_rnf06_auditoria_es_inmutable_en_base_datos(self):
        from django.db import DatabaseError, transaction
        entrada = Auditoria.objects.create(
            usuario=self.admin, entidad="prueba", registro_id="1", accion="VERIFICAR_RNF06", resultado="EXITO",
        )
        with self.assertRaises(DatabaseError), transaction.atomic():
            Auditoria.objects.filter(pk=entrada.pk).update(resultado="FALLO")
        with self.assertRaises(DatabaseError), transaction.atomic():
            Auditoria.objects.filter(pk=entrada.pk).delete()

    def test_rnf26_rechaza_archivos_ejecutables_y_doble_extension(self):
        self.c.force_authenticate(self.usuario)
        for nombre, cuerpo, mime in (
            ("script.php.png", b"<?php echo 1; ?>", "image/png"),
            ("malware.exe", b"MZ\x90\x00", "application/octet-stream"),
            ("vector.svg", b"<svg onload=alert(1)></svg>", "image/svg+xml"),
        ):
            archivo = SimpleUploadedFile(nombre, cuerpo, content_type=mime)
            r = self.c.post("/api/plataforma/negocio/comunidad/", {"texto": "Adjunto", "imagen": archivo}, format="multipart")
            self.assertEqual(r.status_code, 400, nombre)

    def test_rnf04_latencia_consultas_habituales_bajo_umbral_local(self):
        self.c.force_authenticate(self.usuario)
        n.acreditar(self.socio, "CONVERSION", 9901)
        rutas = (
            "/api/plataforma/negocio/puntos/",
            "/api/plataforma/negocio/campanas/",
            "/api/plataforma/negocio/beneficios/",
            "/api/plataforma/negocio/ranking/",
            "/api/plataforma/negocio/comunidad/",
            "/api/plataforma/notificaciones/",
        )
        tiempos = []
        for _ in range(5):
            for ruta in rutas:
                inicio = time.perf_counter()
                r = self.c.get(ruta)
                tiempos.append(time.perf_counter() - inicio)
                self.assertEqual(r.status_code, 200, ruta)
        tiempos.sort()
        p95 = tiempos[int(len(tiempos) * 0.95) - 1]
        self.assertLess(p95, 2.0, f"Percentil 95 local superó 2s: {p95:.3f}s")
