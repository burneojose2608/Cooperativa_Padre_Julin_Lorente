"""HU-011: recuperación temporal por código en consola del backend."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.usuarios.models import Usuario

import hashlib
import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.usuarios.repositories import (
    AuditoriaRepository,
    RecuperacionRepository,
    UsuarioRepository,
)
from apps.usuarios.validators.clave import validar_clave
from apps.usuarios.repositories.sesion_repository import SesionRepository

from .excepciones import ErrorDeNegocio

log = logging.getLogger(__name__)

MINUTOS_VIGENCIA = 30  # el enlace deja de servir después de este tiempo
SEGUNDOS_ENTRE_SOLICITUDES = 120


class EnlaceInvalido(ErrorDeNegocio):
    codigo = "enlace_invalido"
    mensaje = "El enlace no es válido o ya venció. Solicita uno nuevo."


class ServicioRecuperacion:
    """Servicio de aplicacion sin estado; coordina repositorios y reglas de negocio."""

    @staticmethod
    def _huella(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def _mostrar_codigo(usuario: Usuario, token: str) -> None:
        """Entrega temporal de práctica. Nunca usa SMTP ni devuelve el código por HTTP."""
        enlace = f"{settings.FRONTEND_URL.rstrip('/')}/restablecer?token={token}"
        print(
            f"\n===== RECUPERACIÓN DE CONTRASEÑA (práctica local) =====\n"
            f"Usuario: {usuario.username}\nCódigo de recuperación: {token}\n"
            f"Enlace: {enlace}\nVigencia: {MINUTOS_VIGENCIA} minutos. Un solo uso.\n"
            "=====================================================\n",
            flush=True,
        )

    @staticmethod
    def solicitar_recuperacion(*, identificador: str, ip: str | None = None) -> None:
        """Nunca revela si la cuenta existe: siempre termina igual para quien llama."""
        usuario = UsuarioRepository.buscar_por_identificador(identificador.strip())
        if usuario is None or not usuario.is_active:
            AuditoriaRepository.registrar(accion="RECUPERAR_SOLICITUD", resultado="FALLO", ip=ip)
            return
        token = secrets.token_urlsafe(32)
        with transaction.atomic():
            usuario = UsuarioRepository.obtener_para_actualizar(usuario.pk)
            if not usuario.is_active or RecuperacionRepository.hay_solicitud_reciente(usuario, SEGUNDOS_ENTRE_SOLICITUDES):
                return
            RecuperacionRepository.invalidar_pendientes(usuario)
            RecuperacionRepository.crear(
                usuario,
                ServicioRecuperacion._huella(token),
                timezone.now() + timedelta(minutes=MINUTOS_VIGENCIA),
            )
        try:
            ServicioRecuperacion._mostrar_codigo(usuario, token)
            resultado = "EXITO"
        except Exception:
            log.exception("No se pudo mostrar el código de recuperación")
            resultado = "FALLO"
        AuditoriaRepository.registrar(
            accion="RECUPERAR_SOLICITUD",
            resultado=resultado,
            usuario=usuario,
            registro_id=usuario.id_usuario,
            ip=ip,
        )

    @staticmethod
    def restablecer_clave(*, token: str, clave: str, ip: str | None = None) -> None:
        fila = RecuperacionRepository.obtener_vigente(ServicioRecuperacion._huella(token))
        if fila is None or not fila.usuario.is_active:
            AuditoriaRepository.registrar(accion="RECUPERAR_RESTABLECER", resultado="FALLO", ip=ip)
            raise EnlaceInvalido()
        validar_clave(clave)  # si es débil, el enlace NO se gasta y puede intentar de nuevo

        with transaction.atomic():
            usuario = UsuarioRepository.obtener_para_actualizar(fila.usuario_id)
            if not usuario.is_active or fila.vence_en <= timezone.now():
                raise EnlaceInvalido()
            if not RecuperacionRepository.marcar_usado(fila):
                raise EnlaceInvalido()
            UsuarioRepository.cambiar_clave(usuario, clave)
            SesionRepository.revocar_del_usuario(usuario, timezone.now())
            UsuarioRepository.guardar_intentos(usuario, 0, None)  # también desbloquea la cuenta
            RecuperacionRepository.invalidar_pendientes(usuario)
            AuditoriaRepository.registrar(
                accion="RECUPERAR_RESTABLECER",
                resultado="EXITO",
                usuario=usuario,
                registro_id=usuario.id_usuario,
                ip=ip,
            )
