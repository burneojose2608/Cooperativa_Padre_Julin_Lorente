"""Bandeja y cola duradera. La petición registra eventos sin esperar a un SMTP."""
from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import TYPE_CHECKING
from uuid import uuid4

from django.core.mail import send_mail
from django.db import connection, models, transaction
from django.utils import timezone

from .models import (Notificacion, EnvioNotificacion, PlantillaNotificacion,
                     PreferenciaNotificacion, ContenidoInstitucional)

if TYPE_CHECKING:
    from apps.usuarios.models import Usuario

EVENTOS = {
    "PERFIL_ACTUALIZADO": "Perfil actualizado",
    "CLAVE_ACTUALIZADA": "Contraseña actualizada",
    "SOCIO_VALIDADO": "Tu cuenta fue validada como socio",
    "CONTENIDO_PUBLICADO": "Nuevo contenido institucional",
    "REFERIDO": "Avance de tu referencia",
    "PUNTOS": "Puntos acreditados",
    "LOGRO": "Nuevo reconocimiento",
    "CANJE": "Estado de tu canje",
    "FORMACION": "Resultado de formación",
    "SORTEO": "Resultado de sorteo",
}
CANALES = ("INTERNA", "CORREO")
EVENTOS_OBLIGATORIOS = {"CLAVE_ACTUALIZADA", "SOCIO_VALIDADO"}


def permite_envio(usuario, evento, canal):
    if evento in EVENTOS_OBLIGATORIOS:
        return True
    preferencia = PreferenciaNotificacion.objects.filter(usuario=usuario, evento=evento, canal=canal).first()
    return preferencia is None or preferencia.permite_envio()


@transaction.atomic
def _registrar_evento(usuario, evento, mensaje, *, clave_evento=None, disponible_en=None):
    if evento not in EVENTOS:
        raise ValueError("Evento no registrado")
    if clave_evento:
        anterior = Notificacion.objects.filter(destinatario=usuario, clave_evento=clave_evento).first()
        if anterior:
            return anterior
    # No depende de plantillas configuradas a mano; conserva una instantánea del mensaje.
    plantilla = PlantillaNotificacion.objects.filter(evento=evento, canal="TODOS").order_by("pk").first()
    if plantilla is None:
        plantilla = PlantillaNotificacion.objects.create(evento=evento, titulo=EVENTOS[evento], cuerpo="{mensaje}")
    n, creada = Notificacion.objects.get_or_create(destinatario=usuario, clave_evento=clave_evento or uuid4().hex,
        defaults={"plantilla": plantilla, "evento": evento, "titulo": plantilla.titulo, "mensaje_base": mensaje,
                  "mensaje": plantilla.preparar_mensaje({"mensaje": mensaje})})
    if creada:
        for canal in CANALES:
            if permite_envio(usuario, evento, canal):
                EnvioNotificacion.objects.create(notificacion=n, canal=canal,
                                                disponible_en=disponible_en or timezone.now())
    return n


class ServicioNotificaciones:
    @staticmethod
    def notificar_evento(evento: str, destinatario: Usuario, mensaje: str = "", *,
                         clave_evento: str | None = None, disponible_en: datetime | None = None) -> Notificacion:
        return _registrar_evento(destinatario, evento, mensaje, clave_evento=clave_evento, disponible_en=disponible_en)

    @staticmethod
    def procesar_pendiente() -> bool:
        return procesar_uno()


def notificar(usuario, evento, mensaje, **opciones):
    return ServicioNotificaciones.notificar_evento(evento, usuario, mensaje, **opciones)


def notificar_contenido(contenido):
    """Registra un único evento; el trabajador resuelve los destinatarios después."""
    instante = timezone.make_aware(datetime.combine(contenido.desde, time.min))
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO aviso_contenido(id_contenido,version,disponible_en) VALUES (%s,%s,%s) "
                       "ON CONFLICT DO NOTHING", [contenido.pk, contenido.actualizado_en, instante])


@transaction.atomic
def _expandir_publicacion():
    from apps.usuarios.models import Usuario
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_aviso,id_contenido,version FROM aviso_contenido "
                       "WHERE procesado_en IS NULL AND disponible_en <= now() ORDER BY id_aviso "
                       "LIMIT 1 FOR UPDATE SKIP LOCKED")
        fila = cursor.fetchone()
        if fila is None:
            return False
        id_aviso, id_contenido, version = fila
        contenido = ContenidoInstitucional.objects.filter(pk=id_contenido, actualizado_en=version).first()
        cursor.execute("UPDATE aviso_contenido SET procesado_en=now() WHERE id_aviso=%s", [id_aviso])
    if contenido is None or not contenido.es_visible(timezone.localdate()):
        return True
    clave = f"contenido:{contenido.pk}:{contenido.actualizado_en.isoformat()}"
    # El fan-out también sucede fuera de la petición y usa memoria acotada.
    for usuario in Usuario.objects.filter(estado="ACTIVA").iterator(chunk_size=200):
        notificar(usuario, "CONTENIDO_PUBLICADO", contenido.titulo,
                  clave_evento=clave)
    return True


def _contenido_vigente(n):
    if n.evento != "CONTENIDO_PUBLICADO":
        return True
    try:
        _, id_contenido, version = n.clave_evento.split(":", 2)
        c = ContenidoInstitucional.objects.filter(pk=int(id_contenido)).first()
        return c is not None and c.actualizado_en.isoformat() == version and c.es_visible(timezone.localdate())
    except (AttributeError, ValueError):
        return False


def procesar_uno():
    from .contacto import procesar_contacto
    if procesar_contacto():
        return True
    if _expandir_publicacion():
        return True
    ahora = timezone.now()
    with transaction.atomic():
        consulta = EnvioNotificacion.objects.select_for_update(skip_locked=True).filter(
            disponible_en__lte=ahora).filter(
                models.Q(estado="PENDIENTE") | models.Q(estado="PROCESANDO", reservado_hasta__lt=ahora))
        envio = consulta.order_by("pk").first()
        if envio is None:
            return False
        if not envio.puede_reintentarse():
            envio.estado = "FALLIDA"
            envio.ultimo_error = "El trabajador agotó sus intentos antes de confirmar la entrega."
            envio.save(update_fields=["estado", "ultimo_error"])
            return True
        envio.estado = "PROCESANDO"
        envio.intentos += 1
        envio.reserva = uuid4()
        envio.reservado_hasta = ahora + timedelta(minutes=5)
        envio.save(update_fields=["estado", "intentos", "reserva", "reservado_hasta"])
    n = envio.notificacion
    if not n.destinatario.is_active or not permite_envio(n.destinatario, n.evento, envio.canal) or not _contenido_vigente(n):
        EnvioNotificacion.objects.filter(pk=envio.pk, reserva=envio.reserva).update(
            estado="OMITIDA", reserva=None, reservado_hasta=None)
        return True
    try:
        plantilla = PlantillaNotificacion.objects.filter(evento=n.evento, canal=envio.canal).order_by('-pk').first()
        titulo = plantilla.titulo if plantilla else n.titulo
        mensaje = plantilla.preparar_mensaje({"mensaje": n.mensaje_base or n.mensaje}) if plantilla else n.mensaje
        if envio.canal == "INTERNA":
            Notificacion.objects.filter(pk=n.pk).update(estado="ENVIADA", enviada_en=ahora, titulo=titulo, mensaje=mensaje)
        else:
            # Entrega al menos una vez: el proveedor puede recibir un duplicado si cae
            # el proceso después del envío y antes de confirmar. La bandeja es única.
            send_mail(titulo, mensaje, None, [n.destinatario.correo], fail_silently=False)
        envio.ultimo_error = ""
        envio.registrar_resultado(True, ahora)
    except Exception as error:
        # No almacenar credenciales, destinatarios ni textos de excepciones SMTP.
        envio.ultimo_error = type(error).__name__[:100]
        envio.registrar_resultado(False, ahora)
    return True
