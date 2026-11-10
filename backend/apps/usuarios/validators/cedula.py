"""Regla acordada: cédula textual formada por exactamente diez dígitos ASCII."""
import re

from django.core.exceptions import ValidationError


def es_cedula_valida(cedula: str) -> bool:
    return isinstance(cedula, str) and re.fullmatch(r"[0-9]{10}", cedula) is not None


def validar_cedula(cedula: str) -> None:
    if not es_cedula_valida(cedula):
        raise ValidationError("La cédula debe contener exactamente 10 dígitos, del 0 al 9.", code="cedula_invalida")
