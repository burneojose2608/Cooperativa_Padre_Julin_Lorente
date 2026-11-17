"""HU-012: Identificar los roles del usuario autenticado y a qué área pertenece.

Un usuario puede tener varios roles. El orden de AREAS es la prioridad: el primer rol
que tenga el usuario decide a qué pantalla lo lleva el login.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.usuarios.models import Usuario

from apps.usuarios.repositories import RolRepository
from apps.usuarios.permissions import permisos_de

AREAS = (
    # (nombre del rol en la base de datos, código de área)
    ("Administrador", "admin"),
    ("Responsable de Marketing", "marketing"),
    ("Responsable de Responsabilidad Social", "rse"),
    ("Gestor de contenidos", "contenidos"),
    ("Socio", "socio"),
)
CODIGOS_DE_AREA = tuple(area for _, area in AREAS)


class ServicioAutorizacion:
    """Servicio de aplicacion sin estado; coordina repositorios y reglas de negocio."""

    @staticmethod
    def puede_realizar(usuario: Usuario, modulo: str, accion: str) -> bool:
        if not usuario.is_active:
            return False
        return permisos_de(usuario).filter(modulo=modulo, accion=accion).exists()

    @staticmethod
    def identificar_roles(usuario: Usuario) -> dict:
        """Devuelve los roles del usuario, su rol principal y las áreas a las que puede entrar."""
        roles = RolRepository.nombres_de(usuario)
        areas = [area for rol, area in AREAS if rol in roles]
        principal = next((rol for rol, _ in AREAS if rol in roles), None)
        return {
            "permisos": [p.codigo for p in permisos_de(usuario)],
            "roles": roles,
            "rol_principal": principal,
            "area": areas[0] if areas else None,  # None = cuenta sin rol asignado
            "areas": areas,
        }

    @staticmethod
    def tiene_acceso_a_area(usuario: Usuario, area: str) -> bool:
        return area in ServicioAutorizacion.identificar_roles(usuario)["areas"]
