from typing import Protocol
from enum import Enum

from apps.usuarios.models.padron import PadronPrueba


class EstadoPadron(Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    NO_ENCONTRADO = "no_encontrado"


class Padron(Protocol):
    """Consulta el estado; ausencia de socio y fallo de acceso son casos distintos."""

    def consultar_estado(self, cedula: str) -> EstadoPadron: ...


class PadronRepository:
    """Adaptador PostgreSQL del padrón sintético; sin API pública."""

    @staticmethod
    def confirmar_activo_manualmente(cedula: str) -> bool:
        """Solo para el caso de uso administrativo: no reactiva filas inactivas."""
        fila, _ = PadronPrueba.objects.select_for_update().get_or_create(
            cedula=cedula, defaults={"activo": True})
        return fila.activo

    def consultar_estado(self, cedula: str) -> EstadoPadron:
        # Bloquea la fila hasta terminar el registro para que no cambie de
        # estado entre la comprobación y la asignación del rol de socio.
        socio = PadronPrueba.objects.select_for_update().filter(cedula=cedula).first()
        if socio is None:
            return EstadoPadron.NO_ENCONTRADO
        return EstadoPadron.ACTIVO if socio.activo else EstadoPadron.INACTIVO
