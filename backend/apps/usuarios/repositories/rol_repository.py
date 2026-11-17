from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.usuarios.models import Usuario

from apps.usuarios.models import Rol, UsuarioRol


class RolRepository:
    @staticmethod
    def obtener_por_nombre(nombre: str) -> Rol:
        return Rol.objects.get(nombre=nombre)

    @staticmethod
    def asignar(usuario: Usuario, rol: Rol) -> None:
        UsuarioRol.objects.get_or_create(usuario=usuario, rol=rol)

    @staticmethod
    def nombres_de(usuario: Usuario) -> list[str]:
        return list(
            UsuarioRol.objects.filter(usuario=usuario)
            .order_by("rol__id_rol")
            .values_list("rol__nombre", flat=True)
        )
