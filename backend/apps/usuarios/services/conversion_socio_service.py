"""Política provisional: validación manual administrativa, sin cambiar credenciales."""
from django.conf import settings
from django.db import transaction

from apps.usuarios.models import Usuario
from apps.usuarios.repositories import AuditoriaRepository, RolRepository, SocioRepository, UsuarioRepository
from apps.usuarios.repositories.padron_repository import PadronRepository
from .codigos_socio import crear_socio_validado
from .excepciones import (ConfirmacionDeSocioRequerida, ConversionNoAutorizada,
                         ConversionNoPermitida, ConversionTemporalDeshabilitada,
                         CuentaNoEncontrada, SocioNoElegible)


def comprobar_conversion_habilitada():
    if not settings.CONVERSION_SOCIOS_TEMPORAL_HABILITADA:
        raise ConversionTemporalDeshabilitada()


def convertir_cuenta_a_socio(*, administrador, id_usuario, confirmar_socio_activo, ip=None):
    comprobar_conversion_habilitada()
    # No confiar exclusivamente en el permiso HTTP ni en los roles del JWT.
    try:
        administrador = UsuarioRepository.obtener_por_id(administrador.pk)
    except Usuario.DoesNotExist:
        raise ConversionNoAutorizada() from None
    if not administrador.is_active or "Administrador" not in RolRepository.nombres_de(administrador):
        raise ConversionNoAutorizada()
    if confirmar_socio_activo is not True:
        raise ConfirmacionDeSocioRequerida(campo="confirmar_socio_activo")

    with transaction.atomic():
        try:
            usuario = UsuarioRepository.obtener_para_actualizar(id_usuario)
        except Usuario.DoesNotExist:
            raise CuentaNoEncontrada() from None
        if not usuario.is_active:
            raise ConversionNoPermitida()
        roles = RolRepository.nombres_de(usuario)
        socio = SocioRepository.obtener_de(usuario)
        if socio and "Socio" in roles:
            return socio, False  # Reintento idempotente, sin nueva auditoría ni cambios.
        if socio or roles:
            raise ConversionNoPermitida()
        if not PadronRepository.confirmar_activo_manualmente(usuario.cedula):
            raise SocioNoElegible()
        socio = crear_socio_validado(usuario)
        RolRepository.asignar(usuario, RolRepository.obtener_por_nombre("Socio"))
        AuditoriaRepository.registrar(
            accion="CONVERTIR_SOCIO", resultado="EXITO", usuario=administrador,
            entidad="socio", registro_id=usuario.pk, ip=ip)
    return socio, True
