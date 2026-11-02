from rest_framework.permissions import BasePermission

from apps.usuarios.repositories import RolRepository


def tiene_rol(*roles_permitidos):
    """Permiso para vistas: solo entra quien tenga alguno de esos roles (se consulta la base)."""
    class TieneRol(BasePermission):
        message = "No tienes permiso para acceder a esta sección."

        def has_permission(self, request, view):
            u = request.user
            return bool(u and u.is_authenticated
                        and set(RolRepository.nombres_de(u)) & set(roles_permitidos))
    return TieneRol
