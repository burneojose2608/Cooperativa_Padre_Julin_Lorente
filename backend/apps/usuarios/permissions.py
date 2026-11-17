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


def permisos_de(usuario):
    from apps.usuarios.models import Permiso, RolPermiso, UsuarioRol
    roles = UsuarioRol.objects.filter(usuario=usuario).values("rol_id")
    ids = RolPermiso.objects.filter(rol_id__in=roles).values("permiso_id")
    return Permiso.objects.filter(pk__in=ids).order_by("modulo", "accion")


def tiene_permiso(modulo, accion):
    class TienePermiso(BasePermission):
        message = "Tu rol no tiene permiso para realizar esta operación."

        def has_permission(self, request, view):
            from apps.usuarios.services.roles_service import ServicioAutorizacion
            u = request.user
            return bool(u and u.is_authenticated and u.is_active
                        and ServicioAutorizacion.puede_realizar(u, modulo, accion))
    return TienePermiso
