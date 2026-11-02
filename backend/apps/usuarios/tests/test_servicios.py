from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken

from apps.usuarios.models import Auditoria, Consentimiento, Socio, Usuario
from apps.usuarios.repositories import RolRepository
from apps.usuarios.services import excepciones as exc
from apps.usuarios.services import iniciar_sesion, registrar_socio

DATOS = dict(cedula="1710034065", nombre="Ana", apellido="Pérez", correo="ana@mail.com",
             username="ana01", telefono="0991234567", fecha_nacimiento=date(2000, 5, 1),
             clave="Clave1234")


class RegistroTests(TestCase):
    def test_registro_correcto_crea_usuario_socio_rol_y_consentimiento(self):
        u = registrar_socio(**DATOS)
        self.assertTrue(u.check_password("Clave1234"))
        self.assertNotEqual(u.password, "Clave1234")  # cifrada
        self.assertTrue(Socio.objects.filter(usuario=u, codigo_socio__startswith="SOC-").exists())
        self.assertEqual(RolRepository.nombres_de(u), ["Socio"])
        self.assertEqual(Consentimiento.objects.filter(usuario=u).count(), 1)
        self.assertTrue(Auditoria.objects.filter(accion="REGISTRO", resultado="EXITO").exists())

    def test_cedula_invalida(self):
        with self.assertRaises(exc.CedulaInvalida):
            registrar_socio(**{**DATOS, "cedula": "1710034066"})
        self.assertFalse(Usuario.objects.exists())

    def test_cedula_duplicada(self):
        registrar_socio(**DATOS)
        with self.assertRaises(exc.DatoDuplicado) as e:
            registrar_socio(**{**DATOS, "correo": "otro@mail.com", "username": "otro"})
        self.assertEqual(e.exception.campo, "cedula")

    def test_correo_duplicado_sin_importar_mayusculas(self):
        registrar_socio(**DATOS)
        with self.assertRaises(exc.DatoDuplicado) as e:
            registrar_socio(**{**DATOS, "cedula": "1100000007", "correo": "ANA@MAIL.COM", "username": "otro"})
        self.assertEqual(e.exception.campo, "correo")

    def test_username_duplicado(self):
        registrar_socio(**DATOS)
        with self.assertRaises(exc.DatoDuplicado) as e:
            registrar_socio(**{**DATOS, "cedula": "1100000007", "correo": "b@mail.com", "username": "ANA01"})
        self.assertEqual(e.exception.campo, "username")

    def test_clave_debil(self):
        for clave in ("corta1", "sololetrasaaa", "12345678"):
            with self.assertRaises(exc.ClaveDebil):
                registrar_socio(**{**DATOS, "clave": clave})


class LoginTests(TestCase):
    def setUp(self):
        self.usuario = registrar_socio(**DATOS)

    def test_login_por_username_cedula_y_correo(self):
        for ident in ("ana01", "1710034065", "ANA@mail.com"):
            r = iniciar_sesion(identificador=ident, clave="Clave1234")
            self.assertEqual(r["usuario"]["roles"], ["Socio"])

    def test_token_incluye_roles(self):
        r = iniciar_sesion(identificador="ana01", clave="Clave1234")
        self.assertEqual(AccessToken(r["access"])["roles"], ["Socio"])

    def test_clave_incorrecta_y_usuario_inexistente_dan_el_mismo_error(self):
        with self.assertRaises(exc.CredencialesInvalidas) as a:
            iniciar_sesion(identificador="ana01", clave="mala")
        with self.assertRaises(exc.CredencialesInvalidas) as b:
            iniciar_sesion(identificador="noexiste", clave="mala")
        self.assertEqual(a.exception.mensaje, b.exception.mensaje)

    def test_bloqueo_tras_5_intentos_fallidos(self):
        for _ in range(5):
            with self.assertRaises(exc.CredencialesInvalidas):
                iniciar_sesion(identificador="ana01", clave="mala")
        with self.assertRaises(exc.CuentaBloqueada):  # ni con la clave correcta
            iniciar_sesion(identificador="ana01", clave="Clave1234")

    def test_bloqueo_expira(self):
        Usuario.objects.filter(pk=self.usuario.pk).update(bloqueado_hasta=timezone.now() - timedelta(minutes=1))
        self.assertIn("access", iniciar_sesion(identificador="ana01", clave="Clave1234"))

    def test_login_exitoso_reinicia_contador(self):
        for _ in range(3):
            with self.assertRaises(exc.CredencialesInvalidas):
                iniciar_sesion(identificador="ana01", clave="mala")
        iniciar_sesion(identificador="ana01", clave="Clave1234")
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.intentos_fallidos, 0)

    def test_cuenta_suspendida(self):
        Usuario.objects.filter(pk=self.usuario.pk).update(estado="SUSPENDIDA")
        with self.assertRaises(exc.CuentaInactiva):
            iniciar_sesion(identificador="ana01", clave="Clave1234")

    def test_login_queda_en_auditoria(self):
        iniciar_sesion(identificador="ana01", clave="Clave1234")
        with self.assertRaises(exc.CredencialesInvalidas):
            iniciar_sesion(identificador="ana01", clave="mala")
        resultados = set(Auditoria.objects.filter(accion="LOGIN").values_list("resultado", flat=True))
        self.assertEqual(resultados, {"EXITO", "FALLO"})
