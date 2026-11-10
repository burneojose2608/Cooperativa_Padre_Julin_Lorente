from datetime import datetime, timedelta, timezone as timezone_python

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.usuarios.repositories import AuditoriaRepository, UsuarioRepository
from apps.usuarios.models import Usuario
from apps.usuarios.repositories.sesion_repository import SesionRepository
from .roles_service import identificar_roles

MINUTOS_INACTIVIDAD = 15
CLAIM_SESION = "sid"
MENSAJE_SESION = "Tu sesión venció o fue cerrada. Inicia sesión nuevamente."


def _sesion_invalida():
    return AuthenticationFailed(MENSAJE_SESION, code="sesion_invalida")


def emitir_tokens(usuario, ahora):
    refresh = RefreshToken.for_user(usuario)
    vence_en = datetime.fromtimestamp(refresh["exp"], tz=timezone_python.utc)
    sesion = SesionRepository.crear(usuario, vence_en, ahora)
    refresh[CLAIM_SESION] = sesion.pk
    refresh["roles"] = identificar_roles(usuario)["roles"]
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def validar_sesion(*, id_sesion, usuario, tocar=True, ip=None):
    if type(id_sesion) is not int or id_sesion <= 0 or not usuario.is_active:
        raise _sesion_invalida()
    valida = False
    with transaction.atomic():
        sesion = SesionRepository.obtener_para_actualizar(id_sesion, usuario.pk)
        ahora = timezone.now()
        if sesion and sesion.revocada_en is None:
            inactiva = (sesion.ultimo_uso is None
                        or ahora - sesion.ultimo_uso >= timedelta(minutes=MINUTOS_INACTIVIDAD))
            if sesion.vence_en <= ahora or inactiva:
                sesion.revocada_en = ahora
                SesionRepository.guardar(sesion, ["revocada_en"])
                AuditoriaRepository.registrar(accion="SESION_EXPIRADA", resultado="EXITO", usuario=usuario,
                                              entidad="sesion", registro_id=sesion.pk, ip=ip)
            else:
                valida = True
                if tocar:
                    sesion.ultimo_uso = ahora
                    SesionRepository.guardar(sesion, ["ultimo_uso"])
    # Fuera del atomic para conservar revocación y auditoría del vencimiento.
    if not valida:
        raise _sesion_invalida()


def renovar_access(refresh_serializado, ip=None):
    try:
        refresh = RefreshToken(refresh_serializado)
        id_usuario = refresh.get("user_id")
        if type(id_usuario) is not int and not (isinstance(id_usuario, str) and id_usuario.isascii() and id_usuario.isdigit()):
            raise _sesion_invalida()
        usuario = UsuarioRepository.obtener_por_id(id_usuario)
    except (TokenError, Usuario.DoesNotExist):
        raise _sesion_invalida() from None
    validar_sesion(id_sesion=refresh.get(CLAIM_SESION), usuario=usuario, ip=ip)
    refresh["roles"] = identificar_roles(usuario)["roles"]
    return {"access": str(refresh.access_token)}


def cerrar_sesion(*, id_sesion, usuario, ip=None):
    if type(id_sesion) is not int or id_sesion <= 0:
        raise _sesion_invalida()
    with transaction.atomic():
        sesion = SesionRepository.obtener_para_actualizar(id_sesion, usuario.pk)
        if sesion is None:
            raise _sesion_invalida()
        if sesion.revocada_en is None:
            sesion.revocada_en = timezone.now()
            SesionRepository.guardar(sesion, ["revocada_en"])
            AuditoriaRepository.registrar(accion="LOGOUT", resultado="EXITO", usuario=usuario,
                                          entidad="sesion", registro_id=sesion.pk, ip=ip)
