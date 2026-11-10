from apps.usuarios.models import Socio


class SocioRepository:
    @staticmethod
    def obtener_de(usuario):
        return Socio.objects.filter(usuario=usuario).first()

    @staticmethod
    def existe_codigo(codigo: str) -> bool:
        return Socio.objects.filter(codigo_socio=codigo).exists()

    @staticmethod
    def crear(usuario, codigo_socio: str, *, validado_en=None) -> Socio:
        return Socio.objects.create(usuario=usuario, codigo_socio=codigo_socio, validado_en=validado_en)
