"""Entidades del Sprint 2. Los nombres físicos históricos se mapean con db_column."""
from __future__ import annotations

import secrets
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING
from uuid import uuid4

from django.conf import settings
from django.db import models, transaction, IntegrityError
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

if TYPE_CHECKING:
    from apps.usuarios.models import Usuario, Socio


class CodigoReferido(models.Model):
    id_codigo = models.BigAutoField(primary_key=True)
    socio = models.ForeignKey("usuarios.Socio", db_column="id_socio", on_delete=models.DO_NOTHING)
    valor = models.CharField(max_length=16, unique=True, db_column="codigo")
    estado = models.CharField(max_length=10, default="ACTIVO")

    class Meta:
        managed = False
        db_table = "codigo_referido"

    @property
    def activo(self) -> bool:
        return self.estado == "ACTIVO"

    def es_valido(self) -> bool:
        return (self.activo and self.socio.validado_en is not None and self.socio.usuario.is_active
                and self.socio.usuario.roles_asignados.filter(rol__nombre="Socio").exists())

    def generar_enlace(self, base: str) -> str:
        return f"{base.rstrip('/')}/invitacion/{self.valor}"

    @staticmethod
    @transaction.atomic
    def generar_para(socio: Socio) -> CodigoReferido:
        from apps.usuarios.models import Socio
        socio = Socio.objects.select_for_update().select_related("usuario").get(pk=socio.pk)
        if socio.validado_en is None or not socio.usuario.is_active:
            raise PermissionDenied("La cooperativa debe validar tu condición de socio activo.")
        existente = CodigoReferido.objects.filter(socio=socio, estado="ACTIVO").first()
        if existente:
            return existente
        for _ in range(10):
            try:
                with transaction.atomic():
                    codigo = CodigoReferido.objects.create(socio=socio, valor=secrets.token_hex(8).upper())
                    from apps.usuarios.repositories import AuditoriaRepository
                    AuditoriaRepository.registrar(accion="GENERAR_CODIGO_REFERIDO", resultado="EXITO", usuario=socio.usuario,
                                                 entidad="codigo_referido", registro_id=codigo.pk)
                    return codigo
            except IntegrityError as error:
                if getattr(getattr(error.__cause__, "diag", None), "constraint_name", "") != "codigo_referido_codigo_key":
                    raise
        raise ValidationError("No se pudo generar el código. Inténtalo nuevamente.")


class ReglaPuntos(models.Model):
    ACTIVIDADES = ("CONVERSION_REFERIDO", "CAPACITACION_APROBADA", "ASISTENCIA_TALLER", "JUEGO", "RETO")
    id_regla = models.BigAutoField(primary_key=True)
    tipo_actividad = models.CharField(max_length=30, db_column="accion")
    puntos = models.IntegerField()
    limite_periodo = models.IntegerField(default=1)
    periodo = models.CharField(max_length=10, default="DIA")
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True)
    version = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = "regla_puntos"

    def esta_vigente(self, fecha: date) -> bool:
        return self.vigente_desde <= fecha and (self.vigente_hasta is None or fecha <= self.vigente_hasta)

    @staticmethod
    def vigente_para(tipo_actividad: str, fecha: date) -> ReglaPuntos | None:
        return ReglaPuntos.objects.filter(tipo_actividad=tipo_actividad, vigente_desde__lte=fecha).filter(
            models.Q(vigente_hasta__isnull=True) | models.Q(vigente_hasta__gte=fecha)).order_by("-pk").first()

    @staticmethod
    @transaction.atomic
    def configurar_version(condiciones: dict, administrador: Usuario) -> ReglaPuntos:
        from apps.usuarios.services.gestion_cuentas_service import exigir_administrador
        from apps.usuarios.repositories import AuditoriaRepository
        exigir_administrador(administrador)
        if condiciones["vigente_desde"] < timezone.localdate():
            raise ValidationError({"vigente_desde": "La nueva versión se aplica desde hoy o una fecha futura."})
        regla = ReglaPuntos.objects.create(**condiciones, version=uuid4().hex)
        AuditoriaRepository.registrar(accion="CONFIGURAR_REGLA_PUNTOS", resultado="EXITO", usuario=administrador,
                                     entidad="regla_puntos", registro_id=regla.pk)
        return regla


class ContenidoInstitucional(models.Model):
    id_contenido = models.BigAutoField(primary_key=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="autor_id")
    tipo = models.CharField(max_length=20)
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    categoria = models.CharField(max_length=100)
    estado = models.CharField(max_length=12, default="BORRADOR")
    desde = models.DateField(null=True)
    hasta = models.DateField(null=True)
    requiere_aprobacion = models.BooleanField(default=False)
    aprobador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  db_column="aprobador_id", null=True, related_name="contenidos_a_aprobar")
    aprobado_en = models.DateTimeField(null=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    motivo_retiro = models.TextField(default="")

    class Meta:
        managed = False
        db_table = "contenido"

    @staticmethod
    def registrar_borrador(responsable: Usuario, datos: dict) -> ContenidoInstitucional:
        return ContenidoInstitucional.objects.create(autor=responsable, **datos)

    def actualizar_datos(self, datos: dict) -> bool:
        for clave, valor in datos.items():
            setattr(self, clave, valor)
        self.estado = "BORRADOR"
        self.aprobado_en = None
        self.save()
        return True

    def publicar(self, responsable: Usuario) -> bool:
        if not all((self.titulo.strip(), self.cuerpo.strip(), self.categoria.strip(), self.desde)):
            raise ValidationError("Completa título, cuerpo, categoría y fecha de publicación.")
        if self.hasta and self.hasta < self.desde:
            raise ValidationError({"hasta": "La fecha de fin debe ser posterior al inicio."})
        if self.requiere_aprobacion and not self.aprobado_en:
            raise ValidationError("Este contenido requiere aprobación previa.")
        if self.tipo == "MULTIMEDIA" and not self.materiales.exists():
            raise ValidationError("Adjunta al menos un material al contenido multimedia antes de publicarlo.")
        self.estado = "PUBLICADO"
        self.motivo_retiro = ""
        self.save(update_fields=["estado", "motivo_retiro", "actualizado_en"])
        return True

    def retirar(self, motivo: str) -> bool:
        if not motivo.strip():
            raise ValidationError({"motivo": "Indica el motivo del retiro."})
        self.estado = "RETIRADO"
        self.motivo_retiro = motivo
        self.save(update_fields=["estado", "motivo_retiro", "actualizado_en"])
        return True

    def es_visible(self, fecha: date) -> bool:
        return self.estado == "PUBLICADO" and self.desde is not None and self.desde <= fecha and (
            self.hasta is None or fecha <= self.hasta)


class Capacitacion(models.Model):
    id_capacitacion = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    modalidad = models.CharField(max_length=20)
    estado = models.CharField(max_length=12)
    descripcion = models.TextField(default="")
    duracion = models.IntegerField(default=1)
    requisitos = models.TextField(default="")

    class Meta:
        managed = False
        db_table = "capacitacion"


class ModuloCapacitacion(models.Model):
    id_unidad = models.BigAutoField(primary_key=True)
    capacitacion = models.ForeignKey(Capacitacion, db_column="id_capacitacion", on_delete=models.DO_NOTHING)
    orden = models.SmallIntegerField()
    titulo = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = "unidad"


class MaterialEducativo(models.Model):
    id_material = models.BigAutoField(primary_key=True)
    contenido = models.ForeignKey(ContenidoInstitucional, db_column="id_contenido", null=True,
                                  related_name="materiales", on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    recurso = models.CharField(max_length=500, db_column="ruta_archivo")
    formato = models.CharField(max_length=100, db_column="tipo_archivo")
    tamano_bytes = models.IntegerField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, db_column="autor_id", null=True, on_delete=models.DO_NOTHING)
    modulos = models.ManyToManyField(ModuloCapacitacion, through="MaterialModulo")

    class Meta:
        managed = False
        db_table = "material"

    def es_admisible(self) -> bool:
        return 0 < self.tamano_bytes <= 10 * 1024 * 1024 and self.formato in (
            "application/pdf", "image/png", "image/jpeg", "image/webp", "video/mp4")


class MaterialModulo(models.Model):
    material = models.ForeignKey(MaterialEducativo, db_column="id_material", on_delete=models.CASCADE)
    modulo = models.ForeignKey(ModuloCapacitacion, db_column="id_unidad", on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "material_modulo"


class PlantillaNotificacion(models.Model):
    id_plantilla = models.BigAutoField(primary_key=True)
    evento = models.CharField(max_length=40)
    titulo = models.CharField(max_length=150, db_column="asunto")
    cuerpo = models.TextField()
    canal = models.CharField(max_length=8, default="TODOS")

    class Meta:
        managed = False
        db_table = "plantilla_notificacion"

    def preparar_mensaje(self, datos: dict) -> str:
        # Sustitución acotada de marcadores, nunca ejecución de plantillas del usuario.
        texto = self.cuerpo
        for clave, valor in datos.items():
            texto = texto.replace("{" + clave + "}", str(valor))
        return texto


class PreferenciaNotificacion(models.Model):
    id_preferencia = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, db_column="id_usuario", on_delete=models.DO_NOTHING)
    evento = models.CharField(max_length=40)
    canal = models.CharField(max_length=8)
    habilitada = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "preferencia_notificacion"
        unique_together = [("usuario", "evento", "canal")]

    def permite_envio(self, obligatoria: bool = False) -> bool:
        return obligatoria or self.habilitada


class Notificacion(models.Model):
    id_notificacion = models.BigAutoField(primary_key=True)
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, db_column="id_usuario", on_delete=models.DO_NOTHING)
    plantilla = models.ForeignKey(PlantillaNotificacion, db_column="id_plantilla", on_delete=models.DO_NOTHING)
    evento = models.CharField(max_length=40)
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    mensaje_base = models.TextField(default="")
    creada_en = models.DateTimeField(auto_now_add=True, db_column="creado_en")
    leida_en = models.DateTimeField(null=True)
    canal = models.CharField(max_length=8, default="INTERNA")
    estado = models.CharField(max_length=12, default="PENDIENTE")
    enviada_en = models.DateTimeField(null=True)
    clave_evento = models.CharField(max_length=160, null=True)

    class Meta:
        managed = False
        db_table = "notificacion"

    def marcar_leida(self, destinatario: Usuario) -> bool:
        if self.destinatario_id != destinatario.pk:
            raise PermissionDenied("Esta notificación pertenece a otra cuenta.")
        return bool(Notificacion.objects.filter(pk=self.pk, leida_en__isnull=True).update(leida_en=timezone.now()))


class EnvioNotificacion(models.Model):
    id_envio = models.BigAutoField(primary_key=True)
    notificacion = models.ForeignKey(Notificacion, db_column="id_notificacion", on_delete=models.DO_NOTHING)
    canal = models.CharField(max_length=8)
    estado = models.CharField(max_length=12, default="PENDIENTE")
    intentos = models.IntegerField(default=0)
    enviada_en = models.DateTimeField(null=True)
    ultimo_error = models.TextField(default="")
    disponible_en = models.DateTimeField(default=timezone.now)
    reservado_hasta = models.DateTimeField(null=True)
    reserva = models.UUIDField(null=True)

    class Meta:
        managed = False
        db_table = "envio_notificacion"
        unique_together = [("notificacion", "canal")]

    def programar(self) -> bool:
        self.estado = "PENDIENTE"
        self.disponible_en = timezone.now()
        self.save(update_fields=["estado", "disponible_en"])
        return True

    def puede_reintentarse(self) -> bool:
        return self.intentos < 4  # entrega inicial y hasta tres reintentos

    def registrar_resultado(self, exito: bool, fecha: datetime) -> bool:
        self.estado = "ENVIADA" if exito else ("PENDIENTE" if self.puede_reintentarse() else "FALLIDA")
        self.enviada_en = fecha if exito else None
        self.disponible_en = fecha + timedelta(seconds=30 * 2 ** max(0, self.intentos - 1))
        return bool(EnvioNotificacion.objects.filter(pk=self.pk, reserva=self.reserva).update(
            estado=self.estado, enviada_en=self.enviada_en, disponible_en=self.disponible_en,
            ultimo_error=self.ultimo_error, reservado_hasta=None, reserva=None))


from .models_negocio import (Campana, Prospecto, SolicitudContacto, Referido, Conversion, GastoCampana, MovimientoPuntos, ActividadValidada, Nivel, Insignia,
    SocioInsignia, Inscripcion, Progreso, Evaluacion, IntentoEvaluacion, Certificado, Taller, AsistenciaTaller,
    Convenio, Beneficio, Canje, Sorteo, ParticipacionSorteo, Ganador, Juego, Partida, Reto, ProgresoReto,
    Publicacion, Comentario, Reaccion, ReporteComunidad, SuspensionComunidad)
