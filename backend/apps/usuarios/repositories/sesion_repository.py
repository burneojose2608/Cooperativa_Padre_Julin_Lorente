from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from apps.usuarios.models import Usuario

from apps.usuarios.models import Sesion


class SesionRepository:
    @staticmethod
    def crear(usuario: Usuario, vence_en: datetime, ahora: datetime) -> Sesion:
        return Sesion.objects.create(usuario=usuario, vence_en=vence_en, ultimo_uso=ahora)

    @staticmethod
    def obtener_para_actualizar(id_sesion: int, id_usuario: int) -> Sesion | None:
        return (
            Sesion.objects.select_for_update().filter(pk=id_sesion, usuario_id=id_usuario).first()
        )

    @staticmethod
    def guardar(sesion: Sesion, campos: list[str]) -> None:
        sesion.save(update_fields=campos)

    @staticmethod
    def revocar_del_usuario(usuario: Usuario, ahora: datetime) -> int:
        return Sesion.objects.filter(usuario=usuario, revocada_en__isnull=True).update(
            revocada_en=ahora
        )
