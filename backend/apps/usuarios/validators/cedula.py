"""Validación de la cédula (RF-01-1).

Regla simplificada: la cédula debe tener exactamente 10 dígitos numéricos.
No se calcula el dígito verificador ni se revisa la provincia, para que
cualquier persona pueda registrarse. Que no se repita lo garantiza el
servicio de registro (y la restricción UNIQUE de la base de datos).
"""
import re

from django.core.exceptions import ValidationError

_DIEZ_DIGITOS = re.compile(r"^[0-9]{10}$")


def es_cedula_valida(cedula: str) -> bool:
    return isinstance(cedula, str) and bool(_DIEZ_DIGITOS.match(cedula))


def validar_cedula(cedula: str) -> None:
    """Lanza ValidationError si la cédula no tiene 10 dígitos."""
    if not es_cedula_valida(cedula):
        raise ValidationError("La cédula debe tener 10 dígitos.", code="cedula_invalida")
