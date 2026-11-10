"""RF-01: Recuperar contraseña. El usuario verifica su identidad con un enlace enviado a su correo."""
import hashlib
import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from apps.usuarios.repositories import (AuditoriaRepository, RecuperacionRepository, UsuarioRepository)
from apps.usuarios.validators.clave import validar_clave
from apps.usuarios.repositories.sesion_repository import SesionRepository

from .excepciones import ErrorDeNegocio

log = logging.getLogger(__name__)

MINUTOS_VIGENCIA = 30        # el enlace deja de servir después de este tiempo
SEGUNDOS_ENTRE_SOLICITUDES = 120  # evita llenar el correo de alguien con mensajes


class EnlaceInvalido(ErrorDeNegocio):
    codigo = "enlace_invalido"
    mensaje = "El enlace no es válido o ya venció. Solicita uno nuevo."


def _huella(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _enviar_correo(usuario, token: str) -> None:
    enlace = f"{settings.FRONTEND_URL.rstrip('/')}/restablecer?token={token}"
    send_mail(
        subject="Recupera tu contraseña - Cooperativa Padre Julián Lorente",
        message=(
            f"Hola {usuario.nombre},\n\n"
            "Recibimos una solicitud para restablecer tu contraseña. Abre este enlace para elegir una nueva:\n\n"
            f"{enlace}\n\n"
            f"El enlace vence en {MINUTOS_VIGENCIA} minutos y solo puede usarse una vez.\n"
            "Si no fuiste tú, ignora este mensaje: tu contraseña no cambiará."
        ),
        from_email=None,  # usa DEFAULT_FROM_EMAIL
        recipient_list=[usuario.correo],
    )
    if getattr(settings, "MOSTRAR_ENLACE_EN_CONSOLA", False):
        # Modo pruebas (sin correo configurado): la terminal parte y codifica el enlace del
        # correo, así que se muestra aquí completo y limpio para copiarlo.
        print(f"\n===== RECUPERAR CONTRASEÑA (modo pruebas, sin correo real) =====\n"
              f"Para: {usuario.correo}\nEnlace: {enlace}\n"
              f"================================================================\n", flush=True)


def solicitar_recuperacion(*, identificador: str, ip=None) -> None:
    """Nunca revela si la cuenta existe: siempre termina igual para quien llama."""
    usuario = UsuarioRepository.buscar_por_identificador(identificador.strip())
    if usuario is None or not usuario.is_active:
        AuditoriaRepository.registrar(accion="RECUPERAR_SOLICITUD", resultado="FALLO", ip=ip)
        return
    if RecuperacionRepository.hay_solicitud_reciente(usuario, SEGUNDOS_ENTRE_SOLICITUDES):
        return

    token = secrets.token_urlsafe(32)
    with transaction.atomic():
        RecuperacionRepository.invalidar_pendientes(usuario)
        RecuperacionRepository.crear(usuario, _huella(token),
                                     timezone.now() + timedelta(minutes=MINUTOS_VIGENCIA))
    try:
        _enviar_correo(usuario, token)
        resultado = "EXITO"
    except Exception:  # un fallo de correo no debe delatar nada a quien llama
        log.exception("No se pudo enviar el correo de recuperación")
        resultado = "FALLO"
    AuditoriaRepository.registrar(accion="RECUPERAR_SOLICITUD", resultado=resultado, usuario=usuario,
                                  registro_id=usuario.id_usuario, ip=ip)


def restablecer_clave(*, token: str, clave: str, ip=None) -> None:
    fila = RecuperacionRepository.obtener_vigente(_huella(token))
    if fila is None or not fila.usuario.is_active:
        AuditoriaRepository.registrar(accion="RECUPERAR_RESTABLECER", resultado="FALLO", ip=ip)
        raise EnlaceInvalido()
    validar_clave(clave)  # si es débil, el enlace NO se gasta y puede intentar de nuevo

    with transaction.atomic():
        if not RecuperacionRepository.marcar_usado(fila):
            raise EnlaceInvalido()
        usuario = fila.usuario
        UsuarioRepository.cambiar_clave(usuario, clave)
        SesionRepository.revocar_del_usuario(usuario, timezone.now())
        UsuarioRepository.guardar_intentos(usuario, 0, None)  # también desbloquea la cuenta
        RecuperacionRepository.invalidar_pendientes(usuario)
        AuditoriaRepository.registrar(accion="RECUPERAR_RESTABLECER", resultado="EXITO", usuario=usuario,
                                      registro_id=usuario.id_usuario, ip=ip)
