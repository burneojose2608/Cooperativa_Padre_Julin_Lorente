from django.urls import path
from .views.sesiones_views import ActividadView, LogoutView, RefreshConSesionView
from .views.conversion_views import CuentasGeneralesView, ConvertirSocioView
from .views.gestion_views import (PerfilFotoView, CambiarClaveView, UsuariosView, UsuarioDetalleView,
    UsuarioEstadoView, UsuarioFotoView, UsuarioRolesView, RolesView, RolPermisosView, AuditoriaView)

from .views import (AreaView, LoginView, PerfilView, RegistroView,
                    RestablecerClaveView, SolicitarRecuperacionView)

urlpatterns = [
    path("yo/foto/", PerfilFotoView.as_view()),
    path("yo/clave/", CambiarClaveView.as_view()),
    path("administracion/usuarios/", UsuariosView.as_view()),
    path("administracion/usuarios/<int:id_usuario>/", UsuarioDetalleView.as_view()),
    path("administracion/usuarios/<int:id_usuario>/foto/", UsuarioFotoView.as_view()),
    path("administracion/usuarios/<int:id_usuario>/estado/", UsuarioEstadoView.as_view()),
    path("administracion/usuarios/<int:id_usuario>/roles/", UsuarioRolesView.as_view()),
    path("administracion/roles/", RolesView.as_view()),
    path("administracion/roles/<int:id_rol>/permisos/", RolPermisosView.as_view()),
    path("administracion/auditoria/", AuditoriaView.as_view()),
    path("administracion/cuentas-generales/", CuentasGeneralesView.as_view(), name="cuentas-generales"),
    path("administracion/cuentas/<int:id_usuario>/convertir-socio/", ConvertirSocioView.as_view(), name="convertir-socio"),
    path("registro/", RegistroView.as_view(), name="registro"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshConSesionView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("actividad/", ActividadView.as_view(), name="actividad"),
    path("yo/", PerfilView.as_view(), name="perfil"),
    path("yo/<int:id_usuario>/", PerfilView.as_view()),
    path("areas/<slug:area>/", AreaView.as_view(), name="area"),
    path("recuperar/", SolicitarRecuperacionView.as_view(), name="recuperar"),
    path("restablecer/", RestablecerClaveView.as_view(), name="restablecer"),
]
