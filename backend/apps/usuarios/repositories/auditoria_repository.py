from apps.usuarios.models import Auditoria, Consentimiento


class AuditoriaRepository:
    @staticmethod
    def registrar(*, accion: str, resultado: str, usuario=None, entidad="usuario",
                  registro_id=None, ip=None) -> None:
        Auditoria.objects.create(
            usuario=usuario, entidad=entidad, accion=accion, resultado=resultado,
            registro_id=str(registro_id) if registro_id is not None else None, ip=ip,
        )


class ConsentimientoRepository:
    @staticmethod
    def registrar(usuario, version: str) -> None:
        Consentimiento.objects.create(usuario=usuario, version=version)
