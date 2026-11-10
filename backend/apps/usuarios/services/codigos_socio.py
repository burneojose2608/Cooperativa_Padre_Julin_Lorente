import secrets

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.usuarios.repositories import SocioRepository
from .excepciones import ServicioNoDisponible

INTENTOS_GENERACION = 10
INTENTOS_INSERCION = 3


def generar_codigo_socio() -> str:
    """La restricción SQL conserva la garantía final frente a colisiones."""
    for _ in range(INTENTOS_GENERACION):
        codigo = f"SOC-{secrets.randbelow(10**6):06d}"
        if not SocioRepository.existe_codigo(codigo):
            return codigo
    raise ServicioNoDisponible()


def crear_socio_validado(usuario):
    """Reintenta solo colisiones del código, con rollback del savepoint interno.

    El caso de uso mantiene la transacción exterior de cuenta, rol y auditoría.
    Nunca se oculta una colisión de usuario ni otro error de integridad.
    """
    for _ in range(INTENTOS_INSERCION):
        try:
            with transaction.atomic():
                return SocioRepository.crear(usuario, generar_codigo_socio(), validado_en=timezone.now())
        except IntegrityError as error:
            causa = error.__cause__
            restriccion = getattr(getattr(causa, "diag", None), "constraint_name", None)
            if (getattr(causa, "sqlstate", None) != "23505"
                    or restriccion != "socio_codigo_socio_key"):
                raise
    raise ServicioNoDisponible()
