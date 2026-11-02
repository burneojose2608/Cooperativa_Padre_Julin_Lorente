"""Validación de la cédula ecuatoriana (RF-01-1).

Es la misma regla que aplica la base de datos (función cedula_ec_valida):
10 dígitos, provincia 01-24 o 30, tercer dígito menor a 6 y dígito
verificador correcto (módulo 10). Comprueba que el número sea
matemáticamente válido, no que la persona exista en el Registro Civil.
"""
from django.core.exceptions import ValidationError

COEFICIENTES = (2, 1, 2, 1, 2, 1, 2, 1, 2)


def es_cedula_valida(cedula: str) -> bool:
    if not isinstance(cedula, str) or len(cedula) != 10 or not cedula.isdigit():
        return False
    provincia = int(cedula[:2])
    if not (1 <= provincia <= 24 or provincia == 30):
        return False
    if int(cedula[2]) >= 6:
        return False
    total = 0
    for digito, coef in zip(cedula[:9], COEFICIENTES):
        producto = int(digito) * coef
        if producto >= 10:
            producto -= 9
        total += producto
    verificador = (10 - total % 10) % 10
    return verificador == int(cedula[9])


def validar_cedula(cedula: str) -> None:
    """Lanza ValidationError si la cédula no es válida."""
    if not es_cedula_valida(cedula):
        raise ValidationError("La cédula ingresada no es válida.", code="cedula_invalida")
