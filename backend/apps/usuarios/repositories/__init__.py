from .auditoria_repository import AuditoriaRepository, ConsentimientoRepository
from .recuperacion_repository import RecuperacionRepository
from .rol_repository import RolRepository
from .socio_repository import SocioRepository
from .usuario_repository import UsuarioRepository

__all__ = ["UsuarioRepository", "SocioRepository", "RolRepository",
           "AuditoriaRepository", "ConsentimientoRepository", "RecuperacionRepository"]
