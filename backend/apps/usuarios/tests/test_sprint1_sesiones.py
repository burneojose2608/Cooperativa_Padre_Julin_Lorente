from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from unittest.mock import patch

from django.core.cache import cache
from django.db import close_old_connections, connection
from django.test import TestCase, TransactionTestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.usuarios.models import Auditoria, PadronPrueba, Sesion, Usuario, UsuarioRol
from apps.usuarios.repositories import RolRepository
from .test_conversion_socio import CLAVE, crear_cuenta


class SesionesSprint1Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = crear_cuenta(700, "Socio")
        cls.otro = crear_cuenta(701)

    def setUp(self):
        cache.clear()
        self.c = APIClient()

    def login(self, usuario=None):
        usuario = usuario or self.usuario
        respuesta = self.c.post("/api/auth/login/", {"identificador": usuario.username, "clave": CLAVE}, format="json")
        self.assertEqual(respuesta.status_code, 200)
        return respuesta.json()

    def usar(self, access):
        self.c.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def refresh(self, datos):
        return self.c.post("/api/auth/refresh/", {"refresh": datos["refresh"]}, format="json")

    def test_access_y_refresh_pertenecen_a_una_sesion_persistida(self):
        datos = self.login()
        access, refresh = AccessToken(datos["access"]), RefreshToken(datos["refresh"])
        self.assertEqual(access["sid"], refresh["sid"])
        sesion = Sesion.objects.get(pk=access["sid"])
        self.assertEqual(sesion.usuario_id, self.usuario.pk)
        self.assertIsNone(sesion.revocada_en)
        self.assertGreater(sesion.vence_en, timezone.now())
        self.assertIsNotNone(sesion.ultimo_uso)

    def test_login_normaliza_consulta_de_cuentas_historicas_con_espacios(self):
        crear_cuenta(702, username=" usuarioespacios ", correo=" correo@example.test ")
        for identificador in (" USUARIOESPACIOS ", " CORREO@EXAMPLE.TEST "):
            respuesta = self.c.post("/api/auth/login/", {"identificador": identificador, "clave": CLAVE}, format="json")
            self.assertEqual(respuesta.status_code, 200)

    def test_usuario_numerico_tiene_prioridad_sobre_cedula_de_otra_cuenta(self):
        numerico = crear_cuenta(702, username=self.usuario.cedula)
        datos = self.login(numerico)
        self.assertEqual(datos["usuario"]["id"], numerico.pk)

    def test_logout_revoca_access_y_refresh_y_rechaza_reutilizacion(self):
        datos = self.login()
        self.usar(datos["access"])
        self.assertEqual(self.c.post("/api/auth/logout/", {}, format="json").status_code, 204)
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)
        self.assertEqual(self.refresh(datos).status_code, 401)
        self.assertEqual(self.c.post("/api/auth/logout/", {}, format="json").status_code, 401)
        self.assertEqual(Auditoria.objects.filter(accion="LOGOUT").count(), 1)

    def test_logout_de_una_sesion_no_revoca_otra_sesion_independiente(self):
        primera, segunda = self.login(), self.login()
        self.usar(primera["access"])
        self.c.post("/api/auth/logout/", {}, format="json")
        self.usar(segunda["access"])
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 200)
        self.assertEqual(self.refresh(segunda).status_code, 200)

    def test_cambiar_sid_a_sesion_de_otro_usuario_no_da_acceso(self):
        primera, segunda = self.login(), self.login(self.otro)
        token = AccessToken(primera["access"])
        token["sid"] = RefreshToken(segunda["refresh"])["sid"]
        self.usar(str(token))
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)

    def test_tokens_historicos_sin_sesion_no_pueden_reutilizarse(self):
        refresh = RefreshToken.for_user(self.usuario)
        self.usar(str(refresh.access_token))
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)
        self.assertEqual(self.refresh({"refresh": str(refresh)}).status_code, 401)

    def test_refresh_invalido_o_sin_usuario_responde_401(self):
        for valor in ("no-es-un-token", str(RefreshToken())):
            self.assertEqual(self.refresh({"refresh": valor}).status_code, 401)
        token = RefreshToken.for_user(self.usuario)
        token["user_id"] = "no-numerico"
        self.assertEqual(self.refresh({"refresh": str(token)}).status_code, 401)

    def test_inactividad_quince_minutos_revoca_en_servidor_y_no_revive(self):
        datos = self.login()
        id_sesion = RefreshToken(datos["refresh"])["sid"]
        ultimo = timezone.now() - timedelta(minutes=15)
        Sesion.objects.filter(pk=id_sesion).update(ultimo_uso=ultimo)
        self.usar(datos["access"])
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)
        self.assertEqual(self.c.post("/api/auth/actividad/", {}, format="json").status_code, 401)
        self.assertEqual(self.refresh(datos).status_code, 401)
        sesion = Sesion.objects.get(pk=id_sesion)
        self.assertIsNotNone(sesion.revocada_en)
        self.assertEqual(sesion.ultimo_uso, ultimo)
        self.assertEqual(Auditoria.objects.filter(accion="SESION_EXPIRADA").count(), 1)

    def test_actividad_antes_del_limite_actualiza_ultimo_uso(self):
        datos = self.login()
        id_sesion = RefreshToken(datos["refresh"])["sid"]
        Sesion.objects.filter(pk=id_sesion).update(ultimo_uso=timezone.now() - timedelta(minutes=14))
        self.usar(datos["access"])
        self.assertEqual(self.c.post("/api/auth/actividad/", {}, format="json").status_code, 204)
        self.assertGreater(Sesion.objects.get(pk=id_sesion).ultimo_uso, timezone.now() - timedelta(seconds=5))

    def test_vencimiento_absoluto_no_se_extiende_por_refresh(self):
        datos = self.login()
        Sesion.objects.filter(pk=RefreshToken(datos["refresh"])["sid"]).update(vence_en=timezone.now() - timedelta(seconds=1))
        self.assertEqual(self.refresh(datos).status_code, 401)

    def test_usuario_suspendido_no_usa_access_ni_refresh_existentes(self):
        datos = self.login()
        Usuario.objects.filter(pk=self.usuario.pk).update(estado="SUSPENDIDA")
        self.usar(datos["access"])
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)
        self.assertEqual(self.refresh(datos).status_code, 401)

    def test_fallo_de_auditoria_en_logout_no_finge_cierre_confirmado(self):
        datos = self.login()
        self.usar(datos["access"])
        with patch("apps.usuarios.services.sesiones_service.AuditoriaRepository.registrar", side_effect=RuntimeError("interno")):
            self.assertEqual(self.c.post("/api/auth/logout/", {}, format="json").status_code, 500)
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 200)
        self.assertIsNone(Sesion.objects.get(pk=RefreshToken(datos["refresh"])["sid"]).revocada_en)

    def test_cinco_fallos_bloquean_quince_minutos_sin_revelar_causa(self):
        fallos = []
        for _ in range(5):
            fallos.append(self.c.post("/api/auth/login/", {"identificador": self.usuario.username, "clave": "incorrecta"}, format="json"))
        usuario = Usuario.objects.get(pk=self.usuario.pk)
        self.assertGreater(usuario.bloqueado_hasta, timezone.now() + timedelta(minutes=14))
        bloqueado = self.c.post("/api/auth/login/", {"identificador": self.usuario.username, "clave": CLAVE}, format="json")
        self.assertEqual(bloqueado.status_code, 401)
        self.assertEqual(bloqueado.json(), fallos[0].json())
        self.assertEqual(Auditoria.objects.filter(accion="LOGIN", resultado="FALLO").count(), 6)
        self.assertFalse(Sesion.objects.exists())

    def test_fallos_de_credenciales_tienen_mismo_contrato_y_auditoria_con_ip(self):
        respuestas = []
        for identificador, clave, estado, bloqueo in (
            ("inexistente", CLAVE, "ACTIVA", None),
            (self.usuario.username, "incorrecta", "ACTIVA", None),
            (self.usuario.username, CLAVE, "DESACTIVADA", None),
            (self.usuario.username, CLAVE, "ACTIVA", timezone.now() + timedelta(minutes=15)),
        ):
            Usuario.objects.filter(pk=self.usuario.pk).update(estado=estado, bloqueado_hasta=bloqueo)
            respuesta = self.c.post("/api/auth/login/", {"identificador": identificador, "clave": clave},
                                    format="json", REMOTE_ADDR="203.0.113.9")
            self.assertEqual(respuesta.status_code, 401)
            respuestas.append(respuesta.json())
        self.assertTrue(all(r == respuestas[0] for r in respuestas))
        self.assertEqual(Auditoria.objects.filter(accion="LOGIN", resultado="FALLO", ip="203.0.113.9").count(), 4)

    def test_formato_invalido_y_json_mal_formado_tambien_quedan_auditados(self):
        self.assertEqual(self.c.post("/api/auth/login/", {}, format="json").status_code, 400)
        self.assertEqual(self.c.post("/api/auth/login/", '{"clave":', content_type="application/json").status_code, 400)
        self.assertEqual(Auditoria.objects.filter(accion="LOGIN", resultado="FALLO").count(), 2)

    def test_limite_de_login_y_rechazo_auditado(self):
        for _ in range(30):
            self.assertEqual(self.c.post("/api/auth/login/", {}, format="json").status_code, 400)
        respuesta = self.c.post("/api/auth/login/", {}, format="json")
        self.assertEqual(respuesta.status_code, 429)
        self.assertEqual(Auditoria.objects.filter(accion="LOGIN", resultado="FALLO").count(), 31)

    def test_login_correcto_registra_ip_y_recurso_sin_credenciales(self):
        respuesta = self.c.post("/api/auth/login/", {"identificador": self.usuario.username, "clave": CLAVE},
                                format="json", REMOTE_ADDR="203.0.113.10")
        self.assertEqual(respuesta.status_code, 200)
        auditoria = Auditoria.objects.get(accion="LOGIN", resultado="EXITO")
        self.assertEqual((auditoria.ip, auditoria.registro_id), ("203.0.113.10", str(self.usuario.pk)))

    def test_union_de_roles_y_revocacion_de_rol_sin_confiar_en_jwt(self):
        roles = ("Administrador", "Responsable de Marketing", "Responsable de Responsabilidad Social", "Gestor de contenidos")
        for nombre in roles:
            RolRepository.asignar(self.usuario, RolRepository.obtener_por_nombre(nombre))
        datos = self.login()
        self.assertEqual(datos["usuario"]["areas"], ["admin", "marketing", "rse", "contenidos", "socio"])
        self.usar(datos["access"])
        for area in datos["usuario"]["areas"]:
            self.assertEqual(self.c.get(f"/api/auth/areas/{area}/").status_code, 200)
        UsuarioRol.objects.filter(usuario=self.usuario, rol__nombre="Responsable de Marketing").delete()
        self.assertEqual(self.c.get("/api/auth/areas/marketing/").status_code, 403)
        renovado = self.refresh(datos)
        self.assertEqual(renovado.status_code, 200)
        self.assertNotIn("Responsable de Marketing", AccessToken(renovado.json()["access"])["roles"])

    @override_settings(SECURE_SSL_REDIRECT=True, SECURE_PROXY_SSL_HEADER=None)
    def test_configuracion_https_rechaza_http_y_no_confia_en_cabecera_falsificada(self):
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 301)
        self.assertEqual(self.c.get("/api/auth/yo/", HTTP_X_FORWARDED_PROTO="https").status_code, 301)
        self.assertEqual(self.c.get("/api/auth/yo/", secure=True).status_code, 401)


class LoginConcurrenteTests(TransactionTestCase):
    def setUp(self):
        self.assertTrue(connection.settings_dict["NAME"].startswith("test_"))
        self.usuario = crear_cuenta(799)
        cache.clear()

    def tearDown(self):
        if connection.settings_dict["NAME"].startswith("test_"):
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE usuario RESTART IDENTITY CASCADE")
            PadronPrueba.objects.all().delete()

    def test_cinco_fallos_simultaneos_no_pierden_contadores(self):
        barrera = Barrier(5)
        username = self.usuario.username
        def intentar():
            close_old_connections()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT pg_backend_pid()")
                    pid = cursor.fetchone()[0]
                barrera.wait(timeout=15)
                respuesta = APIClient().post("/api/auth/login/", {"identificador": username, "clave": "incorrecta"}, format="json")
                return pid, respuesta.status_code
            finally:
                connection.close()
        with ThreadPoolExecutor(max_workers=5) as executor:
            resultados = list(executor.map(lambda _: intentar(), range(5)))
        self.assertEqual(len({r[0] for r in resultados}), 5)
        self.assertTrue(all(r[1] == 401 for r in resultados))
        self.usuario.refresh_from_db()
        self.assertIsNotNone(self.usuario.bloqueado_hasta)
        self.assertEqual(Auditoria.objects.filter(accion="LOGIN", resultado="FALLO").count(), 5)
