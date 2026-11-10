from concurrent.futures import ThreadPoolExecutor
from datetime import date
from threading import Barrier
from unittest.mock import patch

from django.core.cache import cache
from django.db import OperationalError, close_old_connections, connection
from django.test import TestCase, TransactionTestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.usuarios.models import Auditoria, Consentimiento, PadronPrueba, Socio, Usuario, UsuarioRol
from apps.usuarios.repositories import ConsentimientoRepository, RolRepository, SocioRepository, UsuarioRepository
from apps.usuarios.services.conversion_socio_service import convertir_cuenta_a_socio
from apps.usuarios.services.excepciones import ConversionNoAutorizada

LISTA = "/api/auth/administracion/cuentas-generales/"
CLAVE = "ClaveDemo1234"


def crear_cuenta(numero, rol=None, **cambios):
    datos = dict(cedula=f"{numero:010d}", nombre="Persona", apellido="Sintética",
                 username=f"prueba{numero}", correo=f"prueba{numero}@example.test",
                 telefono="0990000000", fecha_nacimiento=date(2000, 1, 1), clave=CLAVE)
    usuario = UsuarioRepository.crear(**{**datos, **cambios})
    if rol:
        RolRepository.asignar(usuario, RolRepository.obtener_por_nombre(rol))
    return usuario


@override_settings(CONVERSION_SOCIOS_TEMPORAL_HABILITADA=True)
class ConversionSocioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = crear_cuenta(100, "Administrador")
        cls.marketing = crear_cuenta(101, "Responsable de Marketing")
        cls.general = crear_cuenta(102)
        ConsentimientoRepository.registrar(cls.general, "1.0")
        cls.socio = crear_cuenta(103, "Socio")
        SocioRepository.crear(cls.socio, "SOC-EXISTENTE", validado_en=timezone.now())

    def setUp(self):
        cache.clear()
        self.c = APIClient()
        self.c.force_authenticate(self.admin)

    def convertir(self, usuario=None, datos=None):
        id_usuario = (usuario or self.general).pk
        return self.c.post(f"/api/auth/administracion/cuentas/{id_usuario}/convertir-socio/",
                           datos if datos is not None else {"confirmar_socio_activo": True}, format="json")

    def sin_conversion(self):
        self.assertFalse(Socio.objects.filter(usuario=self.general).exists())
        self.assertFalse(UsuarioRol.objects.filter(usuario=self.general).exists())
        self.assertFalse(Auditoria.objects.filter(accion="CONVERTIR_SOCIO").exists())

    def test_sin_autenticacion_no_puede_listar_ni_convertir(self):
        self.c = APIClient()
        self.assertEqual(self.c.get(LISTA).status_code, 401)
        self.assertEqual(self.convertir().status_code, 401)

    def test_general_marketing_y_socio_no_pueden_aprobar(self):
        for usuario in (self.general, self.marketing, self.socio):
            with self.subTest(rol=usuario.username):
                self.c.force_authenticate(usuario)
                self.assertEqual(self.c.get(LISTA).status_code, 403)
                self.assertEqual(self.convertir().status_code, 403)
        self.sin_conversion()

    def test_servicio_tambien_verifica_administrador(self):
        with self.assertRaises(ConversionNoAutorizada):
            convertir_cuenta_a_socio(administrador=self.general, id_usuario=self.general.pk,
                                     confirmar_socio_activo=True)
        self.sin_conversion()

    def test_administrador_suspendido_o_con_rol_revocado_no_puede_convertir(self):
        Usuario.objects.filter(pk=self.admin.pk).update(estado="SUSPENDIDA")
        with self.assertRaises(ConversionNoAutorizada):
            convertir_cuenta_a_socio(administrador=self.admin, id_usuario=self.general.pk,
                                     confirmar_socio_activo=True)
        Usuario.objects.filter(pk=self.admin.pk).update(estado="ACTIVA")
        UsuarioRol.objects.filter(usuario=self.admin).delete()
        self.assertEqual(self.convertir().status_code, 403)
        self.sin_conversion()

    def test_lista_real_filtrada_sin_datos_sensibles_ni_cuentas_internas(self):
        respuesta = self.c.get(LISTA, {"q": self.general.username})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["count"], 1)
        cuenta = respuesta.json()["results"][0]
        self.assertEqual(cuenta["id"], self.general.pk)
        self.assertEqual(cuenta["estado_padron"], "no_encontrado")
        self.assertEqual(set(cuenta), {"id", "nombre", "apellido", "username", "cedula", "estado", "estado_padron"})
        self.assertEqual(self.c.get(LISTA).json()["count"], 1)

    def test_confirmacion_obligatoria_estricta_y_sin_roles_del_cliente(self):
        for datos in ({}, {"confirmar_socio_activo": False}, {"confirmar_socio_activo": "true"},
                      {"confirmar_socio_activo": 1}, {"confirmar_socio_activo": True, "roles": ["Socio"]}):
            with self.subTest(datos=datos):
                self.assertEqual(self.convertir(datos=datos).status_code, 400)
        self.sin_conversion()
        self.assertFalse(PadronPrueba.objects.exists())

    def test_aprobacion_crea_socio_padron_rol_y_auditoria_sin_alterar_cuenta(self):
        antes = (self.general.username, self.general.correo, self.general.password)
        consentimiento = Consentimiento.objects.get(usuario=self.general)
        respuesta = self.convertir()
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.json()["convertido"])
        self.general.refresh_from_db()
        self.assertEqual((self.general.username, self.general.correo, self.general.password), antes)
        self.assertTrue(self.general.check_password(CLAVE))
        socio = Socio.objects.get(usuario=self.general)
        self.assertIsNotNone(socio.validado_en)
        self.assertEqual(RolRepository.nombres_de(self.general), ["Socio"])
        self.assertTrue(PadronPrueba.objects.get(pk=self.general.cedula).activo)
        self.assertEqual(Consentimiento.objects.get(usuario=self.general).pk, consentimiento.pk)
        auditoria = Auditoria.objects.get(accion="CONVERTIR_SOCIO")
        self.assertEqual((auditoria.usuario_id, auditoria.registro_id, auditoria.entidad),
                         (self.admin.pk, str(self.general.pk), "socio"))

    def test_repeticion_no_duplica_roles_socio_ni_auditoria(self):
        primero = self.convertir().json()
        segundo = self.convertir().json()
        self.assertTrue(primero["convertido"])
        self.assertFalse(segundo["convertido"])
        self.assertEqual(primero["codigo_socio"], segundo["codigo_socio"])
        self.assertEqual(Socio.objects.filter(usuario=self.general).count(), 1)
        self.assertEqual(UsuarioRol.objects.filter(usuario=self.general).count(), 1)
        self.assertEqual(Auditoria.objects.filter(accion="CONVERTIR_SOCIO").count(), 1)

    def test_padron_activo_se_reutiliza_y_el_inactivo_no_se_reactiva(self):
        padron = PadronPrueba.objects.create(cedula=self.general.cedula, activo=False)
        self.assertEqual(self.convertir().status_code, 403)
        padron.refresh_from_db()
        self.assertFalse(padron.activo)
        self.sin_conversion()
        PadronPrueba.objects.filter(pk=padron.pk).update(activo=True)
        self.assertEqual(self.convertir().status_code, 200)
        self.assertEqual(PadronPrueba.objects.count(), 1)

    def test_cuenta_suspendida_o_con_otro_rol_se_rechaza(self):
        self.assertEqual(self.convertir(self.marketing).status_code, 409)
        Usuario.objects.filter(pk=self.general.pk).update(estado="SUSPENDIDA")
        self.assertEqual(self.convertir().status_code, 409)
        self.sin_conversion()

    def test_cuenta_inexistente_responde_404(self):
        respuesta = self.c.post("/api/auth/administracion/cuentas/999999/convertir-socio/",
                                {"confirmar_socio_activo": True}, format="json")
        self.assertEqual(respuesta.status_code, 404)

    @override_settings(CONVERSION_SOCIOS_TEMPORAL_HABILITADA=False)
    def test_proceso_temporal_puede_deshabilitarse(self):
        self.assertEqual(self.c.get(LISTA).status_code, 503)
        self.assertEqual(self.convertir().status_code, 503)
        self.sin_conversion()

    def test_fallos_intermedios_revierten_incluso_la_validacion_del_padron(self):
        for metodo in ("RolRepository.asignar", "AuditoriaRepository.registrar"):
            with self.subTest(metodo=metodo), patch(
                    "apps.usuarios.services.conversion_socio_service." + metodo,
                    side_effect=RuntimeError("detalle interno secreto")):
                respuesta = self.convertir()
                self.assertEqual(respuesta.status_code, 500)
                self.assertNotIn("secreto", respuesta.content.decode())
            self.sin_conversion()
            self.assertFalse(PadronPrueba.objects.exists())

    def test_fallo_de_padron_no_permite_convertir(self):
        with patch("apps.usuarios.services.conversion_socio_service.PadronRepository.confirmar_activo_manualmente",
                   side_effect=OperationalError("SQL secreto")):
            respuesta = self.convertir()
        self.assertEqual(respuesta.status_code, 503)
        self.assertNotIn("secreto", respuesta.content.decode())
        self.sin_conversion()

    def test_misma_sesion_del_usuario_consulta_su_nuevo_rol(self):
        cliente_usuario = APIClient()
        login = cliente_usuario.post("/api/auth/login/", {"identificador": self.general.username, "clave": CLAVE}, format="json").json()
        cliente_usuario.credentials(HTTP_AUTHORIZATION=f"Bearer {login['access']}")
        self.assertEqual(cliente_usuario.get("/api/auth/areas/socio/").status_code, 403)
        self.assertEqual(self.convertir().status_code, 200)
        self.assertEqual(cliente_usuario.get("/api/auth/yo/").json()["area"], "socio")
        self.assertEqual(cliente_usuario.get("/api/auth/areas/socio/").status_code, 200)
        self.assertEqual(cliente_usuario.get("/api/auth/areas/admin/").status_code, 403)


@override_settings(CONVERSION_SOCIOS_TEMPORAL_HABILITADA=True)
class ConversionConcurrenteTests(TransactionTestCase):
    def setUp(self):
        self.assertTrue(connection.settings_dict["NAME"].startswith("test_"))
        self.admins = [crear_cuenta(201, "Administrador"), crear_cuenta(202, "Administrador")]
        self.general = crear_cuenta(203)

    def tearDown(self):
        if connection.settings_dict["NAME"].startswith("test_"):
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE usuario RESTART IDENTITY CASCADE")
            PadronPrueba.objects.all().delete()

    def test_dos_administradores_solo_convierten_una_vez(self):
        barrera = Barrier(2)
        id_usuario = self.general.pk

        def convertir(id_admin):
            close_old_connections()
            try:
                admin = Usuario.objects.get(pk=id_admin)
                cliente = APIClient()
                cliente.force_authenticate(admin)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT pg_backend_pid()")
                    pid = cursor.fetchone()[0]
                barrera.wait(timeout=15)
                respuesta = cliente.post(f"/api/auth/administracion/cuentas/{id_usuario}/convertir-socio/",
                                         {"confirmar_socio_activo": True}, format="json")
                return pid, respuesta.status_code, respuesta.json()
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=2) as executor:
            futuros = [executor.submit(convertir, admin.pk) for admin in self.admins]
            resultados = [f.result(timeout=30) for f in futuros]
        self.assertEqual(len({r[0] for r in resultados}), 2)
        self.assertEqual([r[1] for r in resultados], [200, 200])
        self.assertEqual(sorted(r[2]["convertido"] for r in resultados), [False, True])
        self.assertEqual(Socio.objects.filter(usuario_id=id_usuario).count(), 1)
        self.assertEqual(UsuarioRol.objects.filter(usuario_id=id_usuario).count(), 1)
        self.assertEqual(Auditoria.objects.filter(accion="CONVERTIR_SOCIO").count(), 1)
