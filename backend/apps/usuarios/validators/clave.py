import re

from apps.usuarios.services.excepciones import ClaveDebil


def validar_clave(clave: str) -> None:
    """Mínimo 8 caracteres, con letras y números."""
    if len(clave) < 8 or not re.search(r"[A-Za-z]", clave) or not re.search(r"\d", clave):
        raise ClaveDebil()
