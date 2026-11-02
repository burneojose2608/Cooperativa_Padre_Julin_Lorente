from .auth_views import LoginView, PerfilView, RegistroView
from .recuperacion_views import RestablecerClaveView, SolicitarRecuperacionView
from .roles_views import AreaView

__all__ = ["RegistroView", "LoginView", "PerfilView", "AreaView",
           "SolicitarRecuperacionView", "RestablecerClaveView"]
