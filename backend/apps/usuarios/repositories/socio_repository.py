from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from apps.usuarios.models import Usuario

from apps.usuarios.models import Socio


class SocioRepository:
    @staticmethod
    def obtener_de(usuario: Usuario) -> Socio | None:
        return Socio.objects.filter(usuario=usuario).first()

    @staticmethod
    def existe_codigo(codigo: str) -> bool:
        return Socio.objects.filter(codigo_socio=codigo).exists()

    @staticmethod
    def crear(usuario: Usuario, codigo_socio: str, *, validado_en: datetime | None = None) -> Socio:
        return Socio.objects.create(
            usuario=usuario, codigo_socio=codigo_socio, validado_en=validado_en
        )
