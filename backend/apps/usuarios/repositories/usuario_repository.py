from django.db.models import Q

from apps.usuarios.models import Usuario


class UsuarioRepository:
    @staticmethod
    def existe_cedula(cedula: str) -> bool:
        return Usuario.objects.filter(cedula=cedula).exists()

    @staticmethod
    def existe_correo(correo: str) -> bool:
        return Usuario.objects.filter(correo__iexact=correo).exists()

    @staticmethod
    def existe_username(username: str) -> bool:
        return Usuario.objects.filter(username__iexact=username).exists()

    @staticmethod
    def buscar_por_identificador(identificador: str):
        """Busca por cédula, correo o username (sin distinguir mayúsculas)."""
        return Usuario.objects.filter(
            Q(cedula=identificador) | Q(correo__iexact=identificador) | Q(username__iexact=identificador)
        ).first()

    @staticmethod
    def crear(*, clave: str, **datos) -> Usuario:
        usuario = Usuario(**datos)
        usuario.set_password(clave)  # se guarda cifrada, nunca en texto plano
        usuario.save()
        return usuario

    @staticmethod
    def guardar_intentos(usuario: Usuario, intentos: int, bloqueado_hasta=None) -> None:
        usuario.intentos_fallidos = intentos
        usuario.bloqueado_hasta = bloqueado_hasta
        usuario.save(update_fields=["intentos_fallidos", "bloqueado_hasta"])

    @staticmethod
    def cambiar_clave(usuario: Usuario, clave: str) -> None:
        usuario.set_password(clave)  # se guarda cifrada
        usuario.save(update_fields=["password"])
