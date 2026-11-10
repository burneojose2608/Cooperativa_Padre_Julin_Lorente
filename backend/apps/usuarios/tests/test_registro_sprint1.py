from datetime import date
from unittest.mock import patch

from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, OperationalError
from django.test import TestCase
from rest_framework.test import APIClient

from apps.usuarios.models import Auditoria, Consentimiento, PadronPrueba, Socio, Usuario, UsuarioRol
from apps.usuarios.services import iniciar_sesion, registrar_socio
from apps.usuarios.repositories.padron_repository import EstadoPadron
from apps.usuarios.services.excepciones import (ConsentimientoRequerido, DatoDuplicado,
                                               ServicioNoDisponible, SocioNoElegible)

DATOS = dict(cedula="0100000009", nombre="Socio", apellido="Sintético",
             correo="uno@example.test", username="socio01", telefono="0990000000",
             fecha_nacimiento=date(2000, 1, 1), clave="Clave1234", acepta_terminos=True)


class RegistroSprint1Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        PadronPrueba.objects.create(cedula=DATOS["cedula"], activo=True)
        PadronPrueba.objects.create(cedula="0100000017", activo=False)

    def setUp(self):
        cache.clear()
        self.cliente = APIClient()

    def post(self, **cambios):
        datos = {**DATOS, "fecha_nacimiento": "2000-01-01", **cambios}
        return self.cliente.post("/api/auth/registro/", datos, format="json")

    def sin_cuenta(self):
        for modelo in (Usuario, Socio, UsuarioRol, Consentimiento):
            self.assertEqual(modelo.objects.count(), 0, modelo.__name__)
        self.assertFalse(Auditoria.objects.filter(resultado="EXITO").exists())

    def test_activo_crea_fecha_consentimiento_y_hash_argon2id(self):
        usuario = registrar_socio(**DATOS)
        self.assertEqual(usuario.cedula, "0100000009")
        self.assertIsNotNone(usuario.socio.validado_en)
        self.assertTrue(usuario.password.startswith("argon2$argon2id$"))
        consentimiento = Consentimiento.objects.get(usuario=usuario)
        self.assertEqual(consentimiento.version, "1.0")
        self.assertIsNotNone(consentimiento.fecha_aceptacion)

    def test_inactivo_se_rechaza_sin_crear_cuenta(self):
        inactivo = self.post(cedula="0100000017")
        self.assertEqual(inactivo.status_code, 403)
        self.sin_cuenta()

    def test_ausente_del_padron_crea_cuenta_general_y_puede_iniciar_sesion(self):
        registro = self.post(cedula="0100000025")
        self.assertEqual(registro.status_code, 201)
        self.assertIsNone(registro.json()["codigo_socio"])
        self.assertEqual(registro.json()["roles"], [])
        usuario = Usuario.objects.get(cedula="0100000025")
        self.assertTrue(usuario.check_password(DATOS["clave"]))
        self.assertFalse(Socio.objects.exists())
        self.assertFalse(UsuarioRol.objects.exists())
        self.assertEqual(Consentimiento.objects.filter(usuario=usuario).count(), 1)
        self.assertEqual(Auditoria.objects.filter(accion="REGISTRO", resultado="EXITO").count(), 1)
        login = self.cliente.post("/api/auth/login/", {
            "identificador": DATOS["username"], "clave": DATOS["clave"],
        }, format="json")
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.json()["usuario"]["roles"], [])
        self.assertIsNone(login.json()["usuario"]["area"])
        self.cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {login.json()['access']}")
        perfil = self.cliente.get("/api/auth/yo/")
        self.assertEqual(perfil.status_code, 200)
        self.assertEqual(perfil.json()["username"], DATOS["username"])
        for area in ("socio", "admin", "marketing", "rse", "contenidos"):
            with self.subTest(area=area):
                self.assertEqual(self.cliente.get(f"/api/auth/areas/{area}/").status_code, 403)

    def test_duplicados_tambien_se_rechazan_para_cuentas_generales(self):
        self.assertEqual(self.post(cedula="0100000025").status_code, 201)
        for cambios, campo in (
            ({"cedula": "0100000025", "correo": "otro@example.test", "username": "otro01"}, "cedula"),
            ({"cedula": "0100000033", "correo": " UNO@EXAMPLE.TEST ", "username": "otro01"}, "correo"),
            ({"cedula": "0100000033", "correo": "otro@example.test", "username": " SOCIO01 "}, "username"),
        ):
            respuesta = self.post(**cambios)
            self.assertEqual(respuesta.status_code, 409)
            self.assertEqual(respuesta.json()["error"]["campo"], campo)
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertFalse(Socio.objects.exists())

    def test_diez_digitos_sin_verificador_crean_cuentas_generales(self):
        for i, cedula in enumerate(("1234567890", "9999999999", "0000000000")):
            with self.subTest(cedula=cedula):
                respuesta = self.post(cedula=cedula, username=f"general{i}", correo=f"general{i}@example.test")
                self.assertEqual(respuesta.status_code, 201)
                self.assertIsNone(respuesta.json()["codigo_socio"])
                self.assertEqual(respuesta.json()["roles"], [])
        self.assertEqual(Usuario.objects.count(), 3)
        self.assertFalse(Socio.objects.exists())

    def test_fallo_intermedio_de_cuenta_general_revierte_todo(self):
        with patch("apps.usuarios.services.registro_service.ConsentimientoRepository.registrar",
                   side_effect=RuntimeError("detalle interno")):
            respuesta = self.post(cedula="0100000025")
        self.assertEqual(respuesta.status_code, 500)
        self.sin_cuenta()

    def test_cuenta_general_no_puede_autodeclararse_socio(self):
        self.assertEqual(self.post(cedula="0100000025", roles=["Socio"]).status_code, 400)
        self.sin_cuenta()

    def test_hash_historico_pbkdf2_permite_login_y_se_actualiza(self):
        usuario = registrar_socio(**DATOS)
        Usuario.objects.filter(pk=usuario.pk).update(
            password=make_password(DATOS["clave"], hasher="pbkdf2_sha256"))
        resultado = iniciar_sesion(identificador=DATOS["username"], clave=DATOS["clave"])
        self.assertIn("access", resultado)
        usuario.refresh_from_db()
        self.assertTrue(usuario.password.startswith("argon2$argon2id$"))

    def test_fallo_padron_cierra_registro_y_no_filtra_detalles(self):
        with patch("apps.usuarios.repositories.padron_repository.PadronRepository.consultar_estado",
                   side_effect=OperationalError("SQL /ruta/interna secreto")):
            respuesta = self.post()
        self.assertEqual(respuesta.status_code, 503)
        self.assertNotIn("secreto", respuesta.content.decode())
        self.sin_cuenta()

    def test_contrato_inyectable(self):
        class PadronInactivo:
            def consultar_estado(self, cedula):
                return EstadoPadron.INACTIVO
        with self.assertRaises(SocioNoElegible):
            registrar_socio(**DATOS, padron=PadronInactivo())
        self.sin_cuenta()

    def test_estado_desconocido_del_adaptador_no_autoriza_ninguna_cuenta(self):
        class PadronDesconocido:
            def consultar_estado(self, cedula):
                return None
        with self.assertRaises(ServicioNoDisponible):
            registrar_socio(**DATOS, padron=PadronDesconocido())
        self.sin_cuenta()

    def test_no_acepta_campos_controlados_por_servidor(self):
        for campo, valor in (("activo", True), ("estado", "ACTIVA"), ("roles", ["Administrador"]),
                             ("validado_en", "2026-11-08"), ("resultado_validacion", True)):
            with self.subTest(campo=campo):
                self.assertEqual(self.post(**{campo: valor}).status_code, 400)
        self.sin_cuenta()

    def test_consentimiento_obligatorio_y_booleano_estricto(self):
        for valor in (False, "true", 1, None):
            self.assertEqual(self.post(acepta_terminos=valor).status_code, 400)
        datos = {**DATOS, "fecha_nacimiento": "2000-01-01"}
        del datos["acepta_terminos"]
        self.assertEqual(self.cliente.post("/api/auth/registro/", datos, format="json").status_code, 400)
        with self.assertRaises(ConsentimientoRequerido):
            registrar_socio(**{**DATOS, "acepta_terminos": False})
        self.sin_cuenta()

    def test_cedula_numerica_se_rechaza(self):
        self.assertEqual(self.post(cedula=100000009).status_code, 400)

    def test_clave_comun_se_rechaza_en_el_backend_sin_cuenta_parcial(self):
        respuesta = self.post(clave="Password123")
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(respuesta.json()["error"]["campo"], "clave")
        self.sin_cuenta()

    def test_cuerpo_debe_ser_objeto_json(self):
        for cuerpo in ([{"activo": True}], "texto", 123):
            respuesta = self.cliente.post("/api/auth/registro/", cuerpo, format="json")
            self.assertEqual(respuesta.status_code, 400)

    def test_entrada_con_sintaxis_sql_se_guarda_como_texto_sin_ejecutarse(self):
        nombre = "Prueba'); DROP TABLE usuario; --"
        respuesta = self.post(nombre=nombre)
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Usuario.objects.get(cedula=DATOS["cedula"]).nombre, nombre)

    def test_normaliza_antes_de_almacenar_y_rechaza_duplicados(self):
        u = registrar_socio(**{**DATOS, "cedula": " 0100000009 ",
                              "correo": " UNO@EXAMPLE.TEST ", "username": " SOCIO01 "})
        self.assertEqual((u.correo, u.username), ("uno@example.test", "socio01"))
        for cambios, campo in (({}, "cedula"),
                               ({"cedula": "0100000017", "correo": " UNO@EXAMPLE.TEST "}, "correo"),
                               ({"cedula": "0100000017", "correo": "dos@example.test", "username": " SOCIO01 "}, "username")):
            with self.subTest(campo=campo), self.assertRaises(DatoDuplicado) as error:
                registrar_socio(**{**DATOS, **cambios})
            self.assertEqual(error.exception.campo, campo)
        self.assertEqual(Usuario.objects.count(), 1)

    def test_fallo_intermedio_revierte_todas_las_filas(self):
        with patch("apps.usuarios.services.registro_service.ConsentimientoRepository.registrar",
                   side_effect=RuntimeError("detalle interno")):
            respuesta = self.post()
        self.assertEqual(respuesta.status_code, 500)
        self.assertNotIn("detalle interno", respuesta.content.decode())
        self.sin_cuenta()

    def test_integridad_desconocida_no_se_convierte_en_duplicado(self):
        with patch("apps.usuarios.services.registro_service.RolRepository.asignar",
                   side_effect=IntegrityError("otra restricción")):
            respuesta = self.post()
        self.assertEqual(respuesta.status_code, 500)
        self.assertEqual(respuesta.json()["error"]["codigo"], "error_interno")
        self.sin_cuenta()

    def test_limite_solicitudes_conservado(self):
        for _ in range(30):
            self.assertEqual(self.post(acepta_terminos=False).status_code, 400)
        self.assertEqual(self.post().status_code, 429)
