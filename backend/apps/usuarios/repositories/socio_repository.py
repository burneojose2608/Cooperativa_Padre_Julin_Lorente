from apps.usuarios.models import Socio


class SocioRepository:
    @staticmethod
    def existe_codigo(codigo: str) -> bool:
        return Socio.objects.filter(codigo_socio=codigo).exists()

    @staticmethod
    def crear(usuario, codigo_socio: str) -> Socio:
        return Socio.objects.create(usuario=usuario, codigo_socio=codigo_socio)
