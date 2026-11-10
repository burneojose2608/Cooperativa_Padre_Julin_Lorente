from datetime import date
from unittest.mock import patch

from django.core.cache import cache
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient

from apps.usuarios.models import Auditoria, Consentimiento, PadronPrueba, Socio, Usuario, UsuarioRol
from apps.usuarios.repositories import RolRepository, SocioRepository, UsuarioRepository
from apps.usuarios.services.codigos_socio import crear_socio_validado, generar_codigo_socio
from apps.usuarios.services.conversion_socio_service import convertir_cuenta_a_socio
from apps.usuarios.services.excepciones import ServicioNoDisponible
from .test_registro_sprint1 import DATOS


class CodigosSocioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        datos = {**DATOS}
        datos.pop("acepta_terminos")
        cls.existente = UsuarioRepository.crear(**{**datos, "cedula": "0000000111",
                                                   "username": "existente", "correo": "existente@example.test"})
        SocioRepository.crear(cls.existente, "SOC-000001")
        cls.admin = UsuarioRepository.crear(
            cedula="0000000222", nombre="Admin", apellido="Prueba", correo="admin@example.test",
            username="adminprueba", telefono="0990000000", fecha_nacimiento=date(1995, 1, 1), clave="Clave1234")
        RolRepository.asignar(cls.admin, RolRepository.obtener_por_nombre("Administrador"))
        PadronPrueba.objects.create(cedula=DATOS["cedula"], activo=True)

    def setUp(self):
        cache.clear()

    def registrar(self):
        return APIClient().post("/api/auth/registro/", {**DATOS, "fecha_nacimiento": "2000-01-01"}, format="json")

    def sin_alta_parcial(self):
        self.assertFalse(Usuario.objects.filter(cedula=DATOS["cedula"]).exists())
        self.assertFalse(Auditoria.objects.filter(accion="REGISTRO", resultado="EXITO").exists())
        self.assertFalse(Consentimiento.objects.exists())
        self.assertEqual(Socio.objects.count(), 1)

    def test_colision_real_de_codigo_reintenta_sin_romper_transaccion_del_registro(self):
        # Solo se fuerza el número aleatorio. PostgreSQL ejecuta y rechaza
        # realmente la primera inserción por su restricción única.
        with patch("apps.usuarios.services.codigos_socio.generar_codigo_socio",
                   side_effect=["SOC-000001", "SOC-000002"]):
            respuesta = self.registrar()
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json()["codigo_socio"], "SOC-000002")
        usuario = Usuario.objects.get(cedula=DATOS["cedula"])
        self.assertEqual(RolRepository.nombres_de(usuario), ["Socio"])
        self.assertTrue(Consentimiento.objects.filter(usuario=usuario).exists())

    def test_colisiones_repetidas_dan_error_temporal_y_rollback_completo(self):
        with patch("apps.usuarios.services.codigos_socio.generar_codigo_socio", return_value="SOC-000001"):
            respuesta = self.registrar()
        self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(respuesta.json()["error"]["codigo"], "servicio_no_disponible")
        self.sin_alta_parcial()

    def test_otro_error_real_de_integridad_no_se_reintenta_como_codigo_duplicado(self):
        with patch("apps.usuarios.services.codigos_socio.generar_codigo_socio", return_value="SOC-000003"):
            with self.assertRaises(IntegrityError):
                crear_socio_validado(self.existente)  # clave primaria, no código de socio
        self.assertEqual(Socio.objects.filter(usuario=self.existente).count(), 1)
        self.assertFalse(Socio.objects.filter(codigo_socio="SOC-000003").exists())

    def test_generacion_con_colisiones_esta_acotada(self):
        with patch("apps.usuarios.services.codigos_socio.secrets.randbelow", return_value=1) as aleatorio:
            with self.assertRaises(ServicioNoDisponible):
                generar_codigo_socio()
        self.assertLessEqual(aleatorio.call_count, 10)

    def test_conversion_administrativa_reutiliza_el_reintento_seguro(self):
        datos = {**DATOS}
        datos.pop("acepta_terminos")
        general = UsuarioRepository.crear(**datos)
        with patch("apps.usuarios.services.codigos_socio.generar_codigo_socio",
                   side_effect=["SOC-000001", "SOC-000004"]):
            socio, convertido = convertir_cuenta_a_socio(
                administrador=self.admin, id_usuario=general.pk, confirmar_socio_activo=True)
        self.assertTrue(convertido)
        self.assertEqual(socio.codigo_socio, "SOC-000004")
        self.assertEqual(UsuarioRol.objects.filter(usuario=general).count(), 1)
        self.assertEqual(Auditoria.objects.filter(accion="CONVERTIR_SOCIO").count(), 1)
