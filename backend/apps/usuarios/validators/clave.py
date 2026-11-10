import re

from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError

CONTRASENAS_COMUNES = CommonPasswordValidator()


def validar_clave(clave: str) -> None:
    """T-009: mínimo ocho caracteres, letras/números y rechazo de claves comunes."""
    # El paquete services exporta el registro; diferir evita un ciclo al importar
    # este validador directamente desde un comando o una herramienta de Django.
    from apps.usuarios.services.excepciones import ClaveDebil

    if len(clave) < 8 or not re.search(r"[A-Za-z]", clave) or not re.search(r"\d", clave):
        raise ClaveDebil(campo="clave")
    try:
        CONTRASENAS_COMUNES.validate(clave)
    except ValidationError:
        raise ClaveDebil(campo="clave") from None
