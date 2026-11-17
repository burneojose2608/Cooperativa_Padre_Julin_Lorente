from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.usuarios.models import Usuario

from apps.usuarios.models import Auditoria, Consentimiento


class AuditoriaRepository:
    @staticmethod
    def registrar(
        *,
        accion: str,
        resultado: str,
        usuario: Usuario | None = None,
        entidad: str = "usuario",
        registro_id: int | str | None = None,
        ip: str | None = None,
    ) -> None:
        Auditoria.objects.create(
            usuario=usuario,
            entidad=entidad,
            accion=accion,
            resultado=resultado,
            registro_id=str(registro_id) if registro_id is not None else None,
            ip=ip,
        )


class ConsentimientoRepository:
    @staticmethod
    def registrar(usuario: Usuario, version: str) -> None:
        Consentimiento.objects.create(usuario=usuario, version=version)
