import re
from datetime import date, timedelta

from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.usuarios.models import Auditoria, TokenRecuperacion, Usuario
from apps.usuarios.repositories import UsuarioRepository
from apps.usuarios.services import excepciones as exc
from apps.usuarios.services import iniciar_sesion
from apps.usuarios.services.recuperacion_service import (EnlaceInvalido, restablecer_clave,
                                                         solicitar_recuperacion)
from apps.usuarios.validators.cedula import es_cedula_valida

_CEDULAS = [c for c in (f"11{n:08d}" for n in range(1, 400)) if es_cedula_valida(c)]


def crear(n=0, **extra):
    return UsuarioRepository.crear(
        clave="Vieja12345", cedula=_CEDULAS[n], nombre="Ana", apellido="Prueba",
        correo=f"u{n}@mail.com", username=f"usuario{n}", telefono="0991234567",
        fecha_nacimiento=date(1995, 1, 1), **extra)


def token_del_correo(i=-1):
    return re.search(r"token=([\w-]+)", mail.outbox[i].body).group(1)


@override_settings(MOSTRAR_ENLACE_EN_CONSOLA=False)
class RecuperacionTests(TestCase):
    def setUp(self):
        cache.clear()
        self.u = crear(0)

    def test_restablecer_clave_revoca_access_y_refresh_de_sesiones_previas(self):
        datos = iniciar_sesion(identificador="usuario0", clave="Vieja12345")
        solicitar_recuperacion(identificador="usuario0")
        restablecer_clave(token=token_del_correo(), clave="Nueva12345")
        cliente = APIClient()
        cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {datos['access']}")
        self.assertEqual(cliente.get("/api/auth/yo/").status_code, 401)
        self.assertEqual(cliente.post("/api/auth/refresh/", {"refresh": datos["refresh"]}, format="json").status_code, 401)

    def test_envia_correo_con_enlace_y_guarda_solo_la_huella(self):
        solicitar_recuperacion(identificador="usuario0")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["u0@mail.com"])
        token = token_del_correo()
        guardado = TokenRecuperacion.objects.get()
        self.assertNotEqual(guardado.token_hash, token)  # el token real no está en la base
        self.assertEqual(len(guardado.token_hash), 64)

    def test_funciona_con_correo_o_cedula(self):
        for i, ident in enumerate(("u0@mail.com", self.u.cedula)):
            TokenRecuperacion.objects.all().update(creado_en=timezone.now() - timedelta(hours=1))
            solicitar_recuperacion(identificador=ident)
            self.assertEqual(len(mail.outbox), i + 1)

    def test_cuenta_inexistente_o_desactivada_no_envia_nada(self):
        solicitar_recuperacion(identificador="noexiste")
        Usuario.objects.filter(pk=self.u.pk).update(estado="DESACTIVADA")
        solicitar_recuperacion(identificador="usuario0")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(TokenRecuperacion.objects.count(), 0)

    @override_settings(MOSTRAR_ENLACE_EN_CONSOLA=True)
    def test_modo_pruebas_muestra_el_enlace_limpio_en_la_terminal(self):
        from contextlib import redirect_stdout
        from io import StringIO
        salida = StringIO()
        with redirect_stdout(salida):
            solicitar_recuperacion(identificador="usuario0")
        self.assertIn(f"Enlace: http://localhost:5173/restablecer?token={token_del_correo()}", salida.getvalue())

    def test_no_se_pueden_pedir_enlaces_en_rafaga(self):
        solicitar_recuperacion(identificador="usuario0")
        solicitar_recuperacion(identificador="usuario0")
        self.assertEqual(len(mail.outbox), 1)

    def test_un_enlace_nuevo_invalida_el_anterior(self):
        solicitar_recuperacion(identificador="usuario0")
        viejo = token_del_correo()
        TokenRecuperacion.objects.update(creado_en=timezone.now() - timedelta(hours=1))
        solicitar_recuperacion(identificador="usuario0")
        with self.assertRaises(EnlaceInvalido):
            restablecer_clave(token=viejo, clave="Nueva12345")
        restablecer_clave(token=token_del_correo(), clave="Nueva12345")

    def test_restablecer_cambia_la_clave_y_el_enlace_sirve_una_sola_vez(self):
        solicitar_recuperacion(identificador="usuario0")
        t = token_del_correo()
        restablecer_clave(token=t, clave="Nueva12345")
        self.assertIn("access", iniciar_sesion(identificador="usuario0", clave="Nueva12345"))
        with self.assertRaises(exc.CredencialesInvalidas):
            iniciar_sesion(identificador="usuario0", clave="Vieja12345")
        with self.assertRaises(EnlaceInvalido):
            restablecer_clave(token=t, clave="Otra123456")

    def test_enlace_vencido_o_falso(self):
        solicitar_recuperacion(identificador="usuario0")
        t = token_del_correo()
        TokenRecuperacion.objects.update(vence_en=timezone.now() - timedelta(seconds=1),
                                         creado_en=timezone.now() - timedelta(hours=1))
        for malo in (t, "token-inventado"):
            with self.assertRaises(EnlaceInvalido):
                restablecer_clave(token=malo, clave="Nueva12345")

    def test_clave_debil_no_gasta_el_enlace(self):
        solicitar_recuperacion(identificador="usuario0")
        t = token_del_correo()
        with self.assertRaises(exc.ClaveDebil):
            restablecer_clave(token=t, clave="corta")
        restablecer_clave(token=t, clave="Nueva12345")  # sigue sirviendo

    def test_restablecer_desbloquea_la_cuenta(self):
        for _ in range(5):
            with self.assertRaises(exc.CredencialesInvalidas):
                iniciar_sesion(identificador="usuario0", clave="mala")
        with self.assertRaises(exc.CredencialesInvalidas):
            iniciar_sesion(identificador="usuario0", clave="Vieja12345")
        solicitar_recuperacion(identificador="usuario0")
        restablecer_clave(token=token_del_correo(), clave="Nueva12345")
        self.assertIn("access", iniciar_sesion(identificador="usuario0", clave="Nueva12345"))

    def test_queda_en_auditoria(self):
        solicitar_recuperacion(identificador="usuario0")
        restablecer_clave(token=token_del_correo(), clave="Nueva12345")
        acciones = set(Auditoria.objects.values_list("accion", flat=True))
        self.assertTrue({"RECUPERAR_SOLICITUD", "RECUPERAR_RESTABLECER"} <= acciones)


@override_settings(MOSTRAR_ENLACE_EN_CONSOLA=False)
class RecuperacionApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.c = APIClient()
        crear(0)

    def post(self, ruta, datos):
        return self.c.post(f"/api/auth/{ruta}/", datos, format="json")

    def test_misma_respuesta_exista_o_no_la_cuenta(self):
        a = self.post("recuperar", {"identificador": "usuario0"})
        b = self.post("recuperar", {"identificador": "no.existe"})
        self.assertEqual((a.status_code, b.status_code), (200, 200))
        self.assertEqual(a.json(), b.json())
        self.assertEqual(len(mail.outbox), 1)

    def test_flujo_completo_por_la_api(self):
        self.post("recuperar", {"identificador": "u0@mail.com"})
        r = self.post("restablecer", {"token": token_del_correo(), "clave": "Nueva12345"})
        self.assertEqual(r.status_code, 200)
        login = self.post("login", {"identificador": "usuario0", "clave": "Nueva12345"})
        self.assertEqual(login.status_code, 200)

    def test_errores_de_la_api(self):
        r = self.post("restablecer", {"token": "falso", "clave": "Nueva12345"})
        self.assertEqual((r.status_code, r.json()["error"]["codigo"]), (400, "enlace_invalido"))
        self.assertEqual(self.post("recuperar", {}).status_code, 400)
        self.post("recuperar", {"identificador": "usuario0"})
        r = self.post("restablecer", {"token": token_del_correo(), "clave": "corta"})
        self.assertEqual((r.status_code, r.json()["error"]["codigo"]), (400, "clave_debil"))

    def test_limite_de_solicitudes_por_hora(self):
        codigos = [self.post("recuperar", {"identificador": "x"}).status_code for _ in range(12)]
        self.assertEqual(codigos[:10], [200] * 10)
        self.assertEqual(codigos[10], 429)
