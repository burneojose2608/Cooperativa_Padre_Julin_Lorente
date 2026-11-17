from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.usuarios.models import Socio, Usuario

import secrets

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.usuarios.repositories import SocioRepository
from .excepciones import ServicioNoDisponible

INTENTOS_GENERACION = 10
INTENTOS_INSERCION = 3


class ServicioSocios:
    """Servicio de aplicacion sin estado; coordina repositorios y reglas de negocio."""

    @staticmethod
    def generar_codigo_socio() -> str:
        """La restricción SQL conserva la garantía final frente a colisiones."""
        for _ in range(INTENTOS_GENERACION):
            codigo = f"SOC-{secrets.randbelow(10**6):06d}"
            if not SocioRepository.existe_codigo(codigo):
                return codigo
        raise ServicioNoDisponible()

    @staticmethod
    def crear_socio_validado(usuario: Usuario) -> Socio:
        """Reintenta solo colisiones del código, con rollback del savepoint interno.

        El caso de uso mantiene la transacción exterior de cuenta, rol y auditoría.
        Nunca se oculta una colisión de usuario ni otro error de integridad.
        """
        for _ in range(INTENTOS_INSERCION):
            try:
                with transaction.atomic():
                    socio = SocioRepository.crear(
                        usuario, ServicioSocios.generar_codigo_socio(), validado_en=timezone.now()
                    )
                    from apps.plataforma.models import CodigoReferido
                    from apps.plataforma.notificaciones import notificar
                    CodigoReferido.generar_para(socio)
                    notificar(usuario, "SOCIO_VALIDADO", "Ya puedes obtener y compartir tu código de referido.",
                              clave_evento=f"socio:{usuario.pk}")
                    return socio
            except IntegrityError as error:
                causa = error.__cause__
                restriccion = getattr(getattr(causa, "diag", None), "constraint_name", None)
                if (
                    getattr(causa, "sqlstate", None) != "23505"
                    or restriccion != "socio_codigo_socio_key"
                ):
                    raise
        raise ServicioNoDisponible()
