from apps.usuarios.models import Rol, UsuarioRol


class RolRepository:
    @staticmethod
    def obtener_por_nombre(nombre: str) -> Rol:
        return Rol.objects.get(nombre=nombre)

    @staticmethod
    def asignar(usuario, rol: Rol) -> None:
        UsuarioRol.objects.get_or_create(usuario=usuario, rol=rol)

    @staticmethod
    def nombres_de(usuario) -> list[str]:
        return list(
            UsuarioRol.objects.filter(usuario=usuario)
            .order_by("rol__id_rol")
            .values_list("rol__nombre", flat=True)
        )
