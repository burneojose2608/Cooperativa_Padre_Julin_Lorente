"""HU-009: Iniciar sesión e identificar el rol del usuario."""
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone

from apps.usuarios.repositories import AuditoriaRepository, UsuarioRepository

from .roles_service import identificar_roles
from .sesiones_service import emitir_tokens

from .excepciones import CredencialesInvalidas

MAX_INTENTOS = 5          # intentos fallidos antes de bloquear
MINUTOS_BLOQUEO = 15      # duración del bloqueo


def iniciar_sesion(*, identificador: str, clave: str, ip=None) -> dict:
    resultado = None
    with transaction.atomic():
        # La fila bloqueada evita perder intentos cuando llegan peticiones simultáneas.
        usuario = UsuarioRepository.buscar_por_identificador(identificador.strip(), bloquear=True)
        ahora = timezone.now()
        bloqueado = usuario and usuario.bloqueado_hasta and usuario.bloqueado_hasta > ahora
        if usuario is None or not usuario.is_active or bloqueado:
            # Trabajo de hash sin guardar la clave, también si la cuenta no existe.
            make_password(clave)
        elif not usuario.check_password(clave):
            intentos = usuario.intentos_fallidos + 1
            bloqueo = ahora + timedelta(minutes=MINUTOS_BLOQUEO) if intentos >= MAX_INTENTOS else None
            UsuarioRepository.guardar_intentos(usuario, 0 if bloqueo else intentos, bloqueo)
        else:
            UsuarioRepository.guardar_intentos(usuario, 0, None)
            resultado = {
                **emitir_tokens(usuario, ahora),
                "usuario": {
                    "id": usuario.pk, "username": usuario.username,
                    "nombre": usuario.nombre, "apellido": usuario.apellido, "correo": usuario.correo,
                    **identificar_roles(usuario),
                },
            }
        AuditoriaRepository.registrar(
            accion="LOGIN", resultado="EXITO" if resultado else "FALLO", usuario=usuario,
            registro_id=usuario.pk if usuario else None, ip=ip)
    # Fuera del atomic: intentos y auditoría deben persistir también al rechazar.
    if resultado is None:
        raise CredencialesInvalidas()
    return resultado
