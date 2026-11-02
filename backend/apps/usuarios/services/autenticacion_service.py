"""HU-009: Iniciar sesión e identificar el rol del usuario."""
from datetime import timedelta

from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.usuarios.repositories import AuditoriaRepository, UsuarioRepository

from .roles_service import identificar_roles

from .excepciones import CredencialesInvalidas, CuentaBloqueada, CuentaInactiva

MAX_INTENTOS = 5          # intentos fallidos antes de bloquear
MINUTOS_BLOQUEO = 15      # duración del bloqueo


def iniciar_sesion(*, identificador: str, clave: str, ip=None) -> dict:
    usuario = UsuarioRepository.buscar_por_identificador(identificador.strip())

    if usuario is None:
        AuditoriaRepository.registrar(accion="LOGIN", resultado="FALLO", ip=ip)
        raise CredencialesInvalidas()  # mismo mensaje exista o no la cuenta

    ahora = timezone.now()
    if usuario.bloqueado_hasta and usuario.bloqueado_hasta > ahora:
        AuditoriaRepository.registrar(accion="LOGIN", resultado="FALLO", usuario=usuario,
                                      registro_id=usuario.id_usuario, ip=ip)
        raise CuentaBloqueada()

    if not usuario.check_password(clave):
        intentos = usuario.intentos_fallidos + 1
        bloqueo = ahora + timedelta(minutes=MINUTOS_BLOQUEO) if intentos >= MAX_INTENTOS else None
        UsuarioRepository.guardar_intentos(usuario, 0 if bloqueo else intentos, bloqueo)
        AuditoriaRepository.registrar(accion="LOGIN", resultado="FALLO", usuario=usuario,
                                      registro_id=usuario.id_usuario, ip=ip)
        raise CredencialesInvalidas()

    if not usuario.is_active:
        raise CuentaInactiva()

    UsuarioRepository.guardar_intentos(usuario, 0, None)
    info = identificar_roles(usuario)
    roles = info["roles"]

    refresh = RefreshToken.for_user(usuario)
    refresh["roles"] = roles  # el access token hereda este dato
    AuditoriaRepository.registrar(accion="LOGIN", resultado="EXITO", usuario=usuario,
                                  registro_id=usuario.id_usuario, ip=ip)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "usuario": {
            "id": usuario.id_usuario,
            "username": usuario.username,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            **info,  # roles, rol_principal, area, areas
        },
    }
