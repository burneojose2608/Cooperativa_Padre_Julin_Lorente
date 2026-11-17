from contextlib import redirect_stdout
from datetime import date, timedelta
from io import BytesIO, StringIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.db import connection
from django.test import TestCase, override_settings
from django.utils import timezone
from PIL import Image
from rest_framework.test import APIClient

from apps.usuarios.models import Usuario, Rol, UsuarioRol, RolPermiso, Permiso, Auditoria, HistorialEstado, Socio
from apps.usuarios.repositories import UsuarioRepository
from apps.usuarios.services import ControlAcceso
from apps.usuarios.services.codigos_socio import ServicioSocios
from apps.usuarios.services.recuperacion_service import ServicioRecuperacion
from apps.plataforma.models import (CodigoReferido, ReglaPuntos, ContenidoInstitucional, MaterialEducativo,
    Capacitacion, ModuloCapacitacion, Notificacion, EnvioNotificacion, PreferenciaNotificacion)
from apps.plataforma.notificaciones import notificar, procesar_uno


def crear_usuario(n, rol=None):
    u = UsuarioRepository.crear(cedula=f"{n:010}", nombre="Prueba", apellido="Sprint",
        username=f"sprint{n}", correo=f"sprint{n}@ejemplo.com", telefono="0991234567",
        fecha_nacimiento=date(1995, 1, 1), clave="Inicial12345")
    if rol:
        UsuarioRol.objects.create(usuario=u, rol=Rol.objects.get(nombre=rol))
    return u


def imagen(nombre="foto.png"):
    salida = BytesIO()
    Image.new("RGB", (16, 16), "blue").save(salida, "PNG")
    return SimpleUploadedFile(nombre, salida.getvalue(), content_type="image/png")


class Sprint2Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = crear_usuario(701, "Administrador")
        cls.gestor = crear_usuario(702, "Gestor de contenidos")
        cls.rse = crear_usuario(703, "Responsable de Responsabilidad Social")
        cls.general = crear_usuario(704)
        cls.otro = crear_usuario(705)
        cls.socio_u = crear_usuario(706, "Socio")
        cls.socio = ServicioSocios.crear_socio_validado(cls.socio_u)

    def setUp(self):
        cache.clear()
        self.c = APIClient()
        self.c.force_authenticate(self.general)
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        configuracion = override_settings(MEDIA_ROOT=self.tmp.name)
        configuracion.enable()
        self.addCleanup(configuracion.disable)

    def como(self, usuario):
        self.c.force_authenticate(usuario)

    def contenido(self, **datos):
        return ContenidoInstitucional.objects.create(autor=self.gestor, titulo="Noticia",
            cuerpo="Texto <script>alert('x')</script>", categoria="Institucional", tipo="NOTICIA",
            desde=timezone.localdate(), **datos)

    def test_hu002_003_solo_titular_edita_contacto_y_rechaza_identidad(self):
        self.assertEqual(self.c.get("/api/auth/yo/").json()["cedula"], self.general.cedula)
        self.assertEqual(self.c.get(f"/api/auth/yo/{self.otro.pk}/").status_code, 403)
        self.assertEqual(self.c.patch(f"/api/auth/yo/{self.otro.pk}/", {"telefono": "0991111111"}, format="json").status_code, 403)
        r = self.c.patch("/api/auth/yo/", {"correo": "nuevo@ejemplo.com", "telefono": "0999999999"}, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(r.json()["correo"], "nuevo@ejemplo.com")
        for campo in ("cedula", "nombre", "id_usuario", "roles", "username", "estado"):
            r = self.c.patch("/api/auth/yo/", {campo: "cambio"}, format="json")
            self.assertEqual(r.status_code, 400, (campo, r.data))
        self.otro.refresh_from_db()
        self.assertEqual(self.otro.correo, "sprint705@ejemplo.com")

    def test_perfil_requiere_autenticacion_y_correo_unico(self):
        self.assertEqual(self.c.patch("/api/auth/yo/", {"correo": self.otro.correo.upper()}, format="json").status_code, 400)
        self.c = APIClient()
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)

    def test_hu003_foto_privada_y_tipo_real(self):
        r = self.c.patch("/api/auth/yo/", {"foto": imagen()}, format="multipart")
        self.assertEqual(r.status_code, 200, r.data)
        foto = self.c.get("/api/auth/yo/foto/")
        self.assertEqual(foto.status_code, 200)
        foto._resource_closers[0]()  # Cierra el archivo sin request_finished dentro del TestCase.
        mala = SimpleUploadedFile("foto.png", b"<script>x</script>", content_type="image/png")
        self.assertEqual(self.c.patch("/api/auth/yo/", {"foto": mala}, format="multipart").status_code, 400)
        self.como(self.otro)
        self.assertEqual(self.c.get("/api/auth/yo/foto/").status_code, 404)
        self.como(self.general)
        self.assertEqual(self.c.delete("/api/auth/yo/foto/").status_code, 204)

    def test_hu003_rechaza_mas_de_10mb(self):
        grande = SimpleUploadedFile("foto.png", b"0" * (10 * 1024 * 1024 + 1), content_type="image/png")
        self.assertEqual(self.c.patch("/api/auth/yo/", {"foto": grande}, format="multipart").status_code, 400)

    def test_hu004_exige_actual_politica_y_revoca_sesiones(self):
        tokens = ControlAcceso.iniciar_sesion(identificador=self.general.username, clave="Inicial12345")
        for datos in ({"actual": "falsa", "nueva": "Nueva12345"}, {"actual": "Inicial12345", "nueva": "password"}):
            self.assertEqual(self.c.post("/api/auth/yo/clave/", datos, format="json").status_code, 400)
        r = self.c.post("/api/auth/yo/clave/", {"actual": "Inicial12345", "nueva": "Nueva12345"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.general.refresh_from_db()
        self.assertTrue(self.general.check_password("Nueva12345"))
        self.assertNotEqual(self.general.password, "Nueva12345")
        self.c = APIClient()
        self.c.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)
        self.assertTrue(Auditoria.objects.filter(accion="CAMBIAR_CLAVE").exists())

    def test_hu005_admin_crea_busca_filtra_edita_sin_exponer_hash(self):
        self.como(self.admin)
        datos = dict(cedula="0000000801", nombre="Cuenta", apellido="Interna", correo="interna@ejemplo.com",
                     username="interna801", telefono="0991234567", fecha_nacimiento="1995-01-01", clave="Inicial12345", rol="Gestor de contenidos")
        r = self.c.post("/api/auth/administracion/usuarios/", datos, format="json")
        self.assertEqual(r.status_code, 201, r.data)
        id_usuario = r.data["id"]
        self.assertNotIn("password", r.data)
        r = self.c.get("/api/auth/administracion/usuarios/?q=interna801&estado=ACTIVA&rol=Gestor%20de%20contenidos")
        self.assertEqual(r.data["total"], 1)
        self.assertEqual(self.c.patch(f"/api/auth/administracion/usuarios/{id_usuario}/", {"telefono": "0987654321"}, format="json").status_code, 200)
        self.assertEqual(self.c.post("/api/auth/administracion/usuarios/", datos, format="json").status_code, 409)

    def test_hu007_suspender_revoca_login_y_guarda_responsable_motivo(self):
        tokens = ControlAcceso.iniciar_sesion(identificador=self.general.username, clave="Inicial12345")
        self.como(self.admin)
        ruta = f"/api/auth/administracion/usuarios/{self.general.pk}/estado/"
        self.assertEqual(self.c.post(ruta, {"estado": "SUSPENDIDA", "motivo": ""}, format="json").status_code, 400)
        r = self.c.post(ruta, {"estado": "SUSPENDIDA", "motivo": "Verificación administrativa"}, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        h = HistorialEstado.objects.get(registro_id=self.general.pk)
        self.assertEqual((h.usuario_id, h.estado_nuevo), (self.admin.pk, "SUSPENDIDA"))
        self.c = APIClient()
        self.c.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)
        self.c.credentials()
        self.assertEqual(self.c.post("/api/auth/login/", {"identificador": self.general.username, "clave": "Inicial12345"}, format="json").status_code, 401)
        self.como(self.admin)
        self.assertEqual(self.c.post(ruta, {"estado": "ACTIVA", "motivo": "Validación completada"}, format="json").status_code, 200)

    def test_ultimo_admin_no_puede_quedar_inactivo_o_sin_rol(self):
        # La semilla solo registra roles, no cuentas administrativas.
        self.como(self.admin)
        base = f"/api/auth/administracion/usuarios/{self.admin.pk}/"
        self.assertEqual(self.c.post(base + "estado/", {"estado": "DESACTIVADA", "motivo": "Prueba"}, format="json").status_code, 400)
        self.assertEqual(self.c.put(base + "roles/", {"roles": []}, format="json").status_code, 400)

    def test_hu013_asignacion_revocacion_aplican_siguiente_peticion(self):
        self.como(self.admin)
        rol = Rol.objects.get(nombre="Gestor de contenidos")
        ruta = f"/api/auth/administracion/usuarios/{self.general.pk}/roles/"
        self.assertEqual(self.c.put(ruta, {"roles": [rol.pk]}, format="json").status_code, 200)
        self.como(self.general)
        self.assertEqual(self.c.get("/api/plataforma/contenidos/").status_code, 200)
        self.como(self.admin)
        self.assertEqual(self.c.put(ruta, {"roles": []}, format="json").status_code, 200)
        self.como(self.general)
        self.assertEqual(self.c.get("/api/plataforma/contenidos/").status_code, 403)

    def test_hu013_permisos_se_revocan_sin_reiniciar_sesion_y_sql_no_los_reasigna(self):
        self.como(self.admin)
        rol = Rol.objects.get(nombre="Gestor de contenidos")
        r = self.c.put(f"/api/auth/administracion/roles/{rol.pk}/permisos/", {"permisos": []}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertFalse(RolPermiso.objects.filter(rol=rol).exists())
        self.como(self.gestor)
        self.assertEqual(self.c.get("/api/plataforma/contenidos/").status_code, 403)
        self.assertTrue(Auditoria.objects.filter(accion="MODIFICAR_PERMISOS", usuario=self.admin).exists())

    def test_socio_no_se_asigna_sin_validacion(self):
        self.como(self.admin)
        rol = Rol.objects.get(nombre="Socio")
        self.assertEqual(self.c.put(f"/api/auth/administracion/usuarios/{self.general.pk}/roles/", {"roles": [rol.pk]}, format="json").status_code, 400)

    def test_hu014_servidor_deniega_roles_e_idor(self):
        for usuario in (self.general, self.socio_u, self.gestor, self.rse):
            self.como(usuario)
            for ruta in ("usuarios/", "roles/", "auditoria/", f"usuarios/{self.otro.pk}/"):
                self.assertEqual(self.c.get("/api/auth/administracion/" + ruta).status_code, 403)
        self.como(self.general)
        self.assertEqual(self.c.get("/api/plataforma/referidos/codigo/").status_code, 403)
        self.assertEqual(self.c.get("/api/plataforma/materiales/").status_code, 403)
        self.assertEqual(self.c.get("/api/plataforma/reglas-puntos/").status_code, 403)
        self.como(self.socio_u)
        self.assertEqual(self.c.get(f"/api/auth/yo/{self.otro.pk}/").status_code, 403)
        self.assertEqual(self.c.patch(f"/api/auth/yo/{self.otro.pk}/", {"correo": "ajeno@ejemplo.com"}, format="json").status_code, 403)

    def test_hu011_solo_consola_nunca_smtp_ni_token_http(self):
        salida = StringIO()
        with patch("django.core.mail.send_mail") as smtp, redirect_stdout(salida):
            self.c = APIClient()
            r = self.c.post("/api/auth/recuperar/", {"identificador": self.general.username}, format="json")
        smtp.assert_not_called()
        import re
        token = re.search(r"token=([\w-]+)", salida.getvalue()).group(1)
        self.assertNotIn(token, str(r.data))
        self.assertIn("Código de recuperación", salida.getvalue())
        self.assertEqual(self.c.post("/api/auth/restablecer/", {"token": token, "clave": "Nueva12345"}, format="json").status_code, 200)
        self.assertEqual(self.c.post("/api/auth/restablecer/", {"token": token, "clave": "Otra12345"}, format="json").status_code, 400)

    def test_hu016_019_codigo_unico_persistente_enlace_funcional_sin_exponer_socio(self):
        self.como(self.socio_u)
        r = self.c.get("/api/plataforma/referidos/codigo/")
        self.assertEqual(r.status_code, 200, r.data)
        codigo = r.data["codigo"]
        self.assertEqual(len(codigo), 16)
        self.assertEqual(self.c.get("/api/plataforma/referidos/codigo/").data["codigo"], codigo)
        self.assertNotIn(self.socio.codigo_socio, codigo)
        self.c = APIClient()
        invitacion = self.c.get(f"/api/plataforma/invitaciones/{codigo}/")
        self.assertEqual(invitacion.status_code, 200)
        self.assertNotIn(self.socio_u.cedula, str(invitacion.data))
        Usuario.objects.filter(pk=self.socio_u.pk).update(estado="SUSPENDIDA")
        self.assertEqual(self.c.get(f"/api/plataforma/invitaciones/{codigo}/").status_code, 404)

    def test_hu031_crea_versiones_sin_reescribir_reglas_previas(self):
        self.como(self.admin)
        datos = {"tipo_actividad": "JUEGO", "puntos": 10, "limite_periodo": 2, "periodo": "DIA",
                 "vigente_desde": str(timezone.localdate()), "vigente_hasta": None}
        a = self.c.post("/api/plataforma/reglas-puntos/", datos, format="json")
        self.assertEqual(a.status_code, 201, a.data)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO movimiento_puntos(id_socio,id_regla,tipo,cantidad,origen_tipo,origen_id) "
                           "VALUES (%s,%s,'ACREDITACION',10,'JUEGO',90001)", [self.socio.pk, a.data["id"]])
        datos["puntos"] = 20
        b = self.c.post("/api/plataforma/reglas-puntos/", datos, format="json")
        self.assertEqual(b.status_code, 201)
        self.assertEqual(ReglaPuntos.objects.get(pk=a.data["id"]).puntos, 10)
        with connection.cursor() as cursor:
            cursor.execute("SELECT cantidad,id_regla FROM movimiento_puntos WHERE origen_tipo='JUEGO' AND origen_id=90001")
            self.assertEqual(cursor.fetchone(), (10, a.data["id"]))
        self.assertEqual(ReglaPuntos.vigente_para("JUEGO", timezone.localdate()).pk, b.data["id"])
        self.assertEqual(self.c.put(f"/api/plataforma/reglas-puntos/{a.data['id']}/", datos, format="json").status_code, 404)
        datos["vigente_desde"] = str(timezone.localdate() - timedelta(days=1))
        self.assertEqual(self.c.post("/api/plataforma/reglas-puntos/", datos, format="json").status_code, 400)

    def test_hu060_061_064_publica_programa_y_retiro_controlan_visibilidad(self):
        self.como(self.gestor)
        datos = {"titulo": "Noticia", "cuerpo": "<script>texto</script>", "categoria": "Social", "tipo": "NOTICIA",
                 "desde": str(timezone.localdate() + timedelta(days=2)), "hasta": None}
        r = self.c.post("/api/plataforma/contenidos/", datos, format="json")
        self.assertEqual(r.status_code, 201, r.data)
        id_c = r.data["id"]
        self.assertEqual(self.c.post(f"/api/plataforma/contenidos/{id_c}/publicar/", {}, format="json").status_code, 200)
        self.assertEqual(self.c.get("/api/plataforma/publicaciones/").data, [])
        ContenidoInstitucional.objects.filter(pk=id_c).update(desde=timezone.localdate())
        self.assertEqual(len(self.c.get("/api/plataforma/publicaciones/").data), 1)
        self.assertEqual(self.c.post(f"/api/plataforma/contenidos/{id_c}/retirar/", {"motivo": "Corrección"}, format="json").status_code, 200)
        self.assertEqual(self.c.get("/api/plataforma/publicaciones/").data, [])
        c = self.contenido(estado="PUBLICADO", hasta=timezone.localdate() - timedelta(days=1))
        self.assertFalse(c.es_visible(timezone.localdate()))

    def test_editar_publicado_lo_devuelve_a_borrador_y_validacion_fechas(self):
        self.como(self.gestor)
        c = self.contenido(estado="PUBLICADO")
        datos = {"titulo": "Edición", "cuerpo": "Nuevo", "categoria": "Social", "tipo": "NOTICIA",
                 "desde": str(timezone.localdate()), "hasta": None}
        r = self.c.put(f"/api/plataforma/contenidos/{c.pk}/", datos, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["estado"], "BORRADOR")
        datos["hasta"] = str(timezone.localdate() - timedelta(days=1))
        self.assertEqual(self.c.put(f"/api/plataforma/contenidos/{c.pk}/", datos, format="json").status_code, 400)
        self.como(self.rse)
        self.assertEqual(self.c.post(f"/api/plataforma/contenidos/{c.pk}/publicar/", {}).status_code, 403)

    def test_hu062_material_privado_multipart_reutilizable_y_edicion_eliminacion(self):
        curso = Capacitacion.objects.create(titulo="Curso", modalidad="VIRTUAL", estado="BORRADOR")
        m1 = ModuloCapacitacion.objects.create(capacitacion=curso, orden=1, titulo="Primero")
        m2 = ModuloCapacitacion.objects.create(capacitacion=curso, orden=2, titulo="Segundo")
        self.como(self.rse)
        r = self.c.post("/api/plataforma/materiales/", {"titulo": "Guía", "categoria": "Educación", "archivo": imagen(), "modulos": f"[{m1.pk},{m2.pk}]"}, format="multipart")
        self.assertEqual(r.status_code, 201, r.data)
        material = MaterialEducativo.objects.get(pk=r.data["id"])
        self.assertEqual(material.modulos.count(), 2)
        self.assertTrue(material.es_admisible())
        self.assertNotIn("foto.png", material.recurso)
        archivo = self.c.get(f"/api/plataforma/materiales/{material.pk}/archivo/")
        self.assertEqual(archivo.status_code, 200)
        archivo._resource_closers[0]()
        self.como(self.general)
        self.assertEqual(self.c.get(f"/api/plataforma/materiales/{material.pk}/archivo/").status_code, 404)
        self.como(self.gestor)
        r = self.c.put(f"/api/plataforma/materiales/{material.pk}/", {"titulo": "Nueva guía", "categoria": "Social", "modulos": []}, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(r.data["modulos"], [])
        self.assertEqual(self.c.delete(f"/api/plataforma/materiales/{material.pk}/").status_code, 204)

    def test_hu062_rechaza_extension_mime_y_contenido_falsificados(self):
        self.como(self.rse)
        for archivo in (SimpleUploadedFile("x.pdf", b"no pdf", content_type="application/pdf"),
                        SimpleUploadedFile("x.svg", b"<svg/>", content_type="image/svg+xml"), imagen("x.jpg")):
            r = self.c.post("/api/plataforma/materiales/", {"titulo": "Malo", "categoria": "Social", "archivo": archivo}, format="multipart")
            self.assertEqual(r.status_code, 400, r.data)
        self.assertFalse(MaterialEducativo.objects.exists())
        from pypdf import PdfWriter
        pdf = BytesIO()
        escritor = PdfWriter(); escritor.add_blank_page(width=300, height=300); escritor.write(pdf)
        self.como(self.gestor)
        archivo = SimpleUploadedFile("guia.pdf", pdf.getvalue(), content_type="application/pdf")
        r = self.c.post("/api/plataforma/materiales/", {"titulo": "PDF educativo", "categoria": "Educación", "archivo": archivo, "contenido": "", "modulos": "[]"}, format="multipart")
        self.assertEqual(r.status_code, 201, r.data)
        self.assertIsNone(r.data["contenido"])

    def test_multimedia_necesita_material_y_descarga_solo_durante_vigencia(self):
        self.como(self.gestor)
        c = self.contenido()
        c.tipo = "MULTIMEDIA"; c.save(update_fields=["tipo"])
        ruta = f"/api/plataforma/contenidos/{c.pk}/publicar/"
        self.assertEqual(self.c.post(ruta, {}).status_code, 400)
        r = self.c.post("/api/plataforma/materiales/", {"titulo": "Imagen", "categoria": "Social", "archivo": imagen(), "contenido": c.pk}, format="multipart")
        self.assertEqual(r.status_code, 201, r.data)
        self.assertEqual(self.c.post(ruta, {}).status_code, 200)
        self.como(self.general)
        archivo = self.c.get(f"/api/plataforma/materiales/{r.data['id']}/archivo/")
        self.assertEqual(archivo.status_code, 200)
        archivo._resource_closers[0]()
        ContenidoInstitucional.objects.filter(pk=c.pk).update(estado="RETIRADO")
        self.assertEqual(self.c.get(f"/api/plataforma/materiales/{r.data['id']}/archivo/").status_code, 404)

    def test_hu068_no_envia_correo_en_peticion_y_respeta_preferencias(self):
        PreferenciaNotificacion.objects.create(usuario=self.general, evento="PERFIL_ACTUALIZADO", canal="CORREO", habilitada=False)
        with patch("apps.plataforma.notificaciones.send_mail") as smtp:
            n = notificar(self.general, "PERFIL_ACTUALIZADO", "Cambio", clave_evento="perfil:1")
            notificar(self.general, "PERFIL_ACTUALIZADO", "Cambio", clave_evento="perfil:1")
            smtp.assert_not_called()
        self.assertEqual(EnvioNotificacion.objects.filter(notificacion=n).count(), 1)
        self.assertEqual(Notificacion.objects.filter(clave_evento="perfil:1").count(), 1)
        self.assertEqual(self.c.get("/api/plataforma/notificaciones/").data["no_leidas"], 0)

    def test_hu068_hasta_tres_reintentos_error_persistente_y_preferencias_tardias(self):
        n = notificar(self.general, "PERFIL_ACTUALIZADO", "Cambio")
        envio = EnvioNotificacion.objects.get(notificacion=n, canal="CORREO")
        # Aísla esta cola de las notificaciones del socio creado en setUpTestData.
        EnvioNotificacion.objects.exclude(pk=envio.pk).update(estado="OMITIDA")
        with patch("apps.plataforma.notificaciones.send_mail", side_effect=OSError("dato sensible")) as smtp:
            for _ in range(4):
                self.assertTrue(procesar_uno())
                EnvioNotificacion.objects.filter(pk=envio.pk).update(disponible_en=timezone.now())
            self.assertFalse(procesar_uno())
            self.assertEqual(smtp.call_count, 4)
        envio.refresh_from_db()
        self.assertEqual((envio.estado, envio.intentos, envio.ultimo_error), ("FALLIDA", 4, "OSError"))
        n2 = notificar(self.otro, "PERFIL_ACTUALIZADO", "Cambio2")
        PreferenciaNotificacion.objects.create(usuario=self.otro, evento="PERFIL_ACTUALIZADO", canal="CORREO", habilitada=False)
        with patch("apps.plataforma.notificaciones.send_mail") as smtp:
            while procesar_uno(): pass
            smtp.assert_not_called()
        self.assertEqual(EnvioNotificacion.objects.get(notificacion=n2, canal="CORREO").estado, "OMITIDA")

    def test_hu069_bandeja_propia_lectura_idempotente_y_preferencias_propias(self):
        n = notificar(self.general, "PERFIL_ACTUALIZADO", "Cambio")
        with patch("apps.plataforma.notificaciones.send_mail"):
            while procesar_uno(): pass
        self.assertEqual(self.c.get("/api/plataforma/notificaciones/").data["no_leidas"], 1)
        ruta = f"/api/plataforma/notificaciones/{n.pk}/leida/"
        self.como(self.otro)
        self.assertEqual(self.c.post(ruta, {}).status_code, 403)
        self.como(self.general)
        self.assertEqual(self.c.post(ruta, {}).status_code, 200)
        self.assertEqual(self.c.post(ruta, {}).status_code, 200)
        self.assertEqual(self.c.get("/api/plataforma/notificaciones/").data["no_leidas"], 0)
        self.assertEqual(self.c.put("/api/plataforma/preferencias/", {"evento": "PERFIL_ACTUALIZADO", "canal": "INTERNA", "habilitada": False, "usuario": self.otro.pk}, format="json").status_code, 400)

    def test_notificacion_de_contenido_programado_retirado_no_se_entrega(self):
        self.como(self.gestor)
        c = self.contenido()
        self.assertEqual(self.c.post(f"/api/plataforma/contenidos/{c.pk}/publicar/", {}).status_code, 200)
        self.c.post(f"/api/plataforma/contenidos/{c.pk}/retirar/", {"motivo": "Corrección"}, format="json")
        with patch("apps.plataforma.notificaciones.send_mail") as smtp:
            while procesar_uno(): pass
            # Solo podría haber entregas del evento de validación del socio.
            for llamada in smtp.call_args_list:
                self.assertNotEqual(llamada.args[0], "Nuevo contenido institucional")
        self.assertFalse(Notificacion.objects.filter(evento="CONTENIDO_PUBLICADO", estado="ENVIADA").exists())

    def test_publicar_encola_un_evento_y_el_trabajador_resuelve_destinatarios(self):
        self.como(self.gestor)
        c = self.contenido()
        with patch("apps.plataforma.notificaciones.send_mail") as smtp:
            self.assertEqual(self.c.post(f"/api/plataforma/contenidos/{c.pk}/publicar/", {}).status_code, 200)
            smtp.assert_not_called()
            self.assertFalse(Notificacion.objects.filter(evento="CONTENIDO_PUBLICADO").exists())
            self.assertTrue(procesar_uno())
            self.assertEqual(Notificacion.objects.filter(evento="CONTENIDO_PUBLICADO").count(), Usuario.objects.filter(estado="ACTIVA").count())
            while procesar_uno(): pass
        self.assertTrue(Notificacion.objects.filter(evento="CONTENIDO_PUBLICADO", estado="ENVIADA").exists())
