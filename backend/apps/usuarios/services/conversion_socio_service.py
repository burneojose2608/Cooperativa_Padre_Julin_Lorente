"""Política provisional: validación manual administrativa, sin cambiar credenciales."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.usuarios.models import Socio

from django.conf import settings
from django.db import transaction

from apps.usuarios.models import Usuario
from apps.usuarios.repositories import (
    AuditoriaRepository,
    RolRepository,
    SocioRepository,
    UsuarioRepository,
)
from apps.usuarios.repositories.padron_repository import PadronRepository
from .codigos_socio import ServicioSocios
from .excepciones import (
    ConfirmacionDeSocioRequerida,
    ConversionNoAutorizada,
    ConversionNoPermitida,
    ConversionTemporalDeshabilitada,
    CuentaNoEncontrada,
    SocioNoElegible,
)


class ValidacionAdministrativaSocio:
    """Servicio de aplicacion sin estado; coordina repositorios y reglas de negocio."""

    @staticmethod
    def comprobar_conversion_habilitada() -> None:
        if not settings.CONVERSION_SOCIOS_TEMPORAL_HABILITADA:
            raise ConversionTemporalDeshabilitada()

    @staticmethod
    def convertir_cuenta_a_socio(
        *,
        administrador: Usuario,
        id_usuario: int,
        confirmar_socio_activo: bool,
        ip: str | None = None,
    ) -> tuple[Socio, bool]:
        ValidacionAdministrativaSocio.comprobar_conversion_habilitada()
        # No confiar exclusivamente en el permiso HTTP ni en los roles del JWT.
        try:
            administrador = UsuarioRepository.obtener_por_id(administrador.pk)
        except Usuario.DoesNotExist:
            raise ConversionNoAutorizada() from None
        if not administrador.is_active or "Administrador" not in RolRepository.nombres_de(
            administrador
        ):
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
            socio = ServicioSocios.crear_socio_validado(usuario)
            RolRepository.asignar(usuario, RolRepository.obtener_por_nombre("Socio"))
            AuditoriaRepository.registrar(
                accion="CONVERTIR_SOCIO",
                resultado="EXITO",
                usuario=administrador,
                entidad="socio",
                registro_id=usuario.pk,
                ip=ip,
            )
        return socio, True
