"""HU-012: Identificar los roles del usuario autenticado y a qué área pertenece.

Un usuario puede tener varios roles. El orden de AREAS es la prioridad: el primer rol
que tenga el usuario decide a qué pantalla lo lleva el login.
"""
from apps.usuarios.repositories import RolRepository

AREAS = (
    # (nombre del rol en la base de datos, código de área)
    ("Administrador", "admin"),
    ("Responsable de Marketing", "marketing"),
    ("Responsable de Responsabilidad Social", "rse"),
    ("Gestor de contenidos", "contenidos"),
    ("Socio", "socio"),
)
CODIGOS_DE_AREA = tuple(area for _, area in AREAS)


def identificar_roles(usuario) -> dict:
    """Devuelve los roles del usuario, su rol principal y las áreas a las que puede entrar."""
    roles = RolRepository.nombres_de(usuario)
    areas = [area for rol, area in AREAS if rol in roles]
    principal = next((rol for rol, _ in AREAS if rol in roles), None)
    return {
        "roles": roles,
        "rol_principal": principal,
        "area": areas[0] if areas else None,   # None = cuenta sin rol asignado
        "areas": areas,
    }


def tiene_acceso_a_area(usuario, area: str) -> bool:
    return area in identificar_roles(usuario)["areas"]
