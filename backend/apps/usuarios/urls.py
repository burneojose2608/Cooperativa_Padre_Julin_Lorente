from django.urls import path
from .views.sesiones_views import ActividadView, LogoutView, RefreshConSesionView
from .views.conversion_views import CuentasGeneralesView, ConvertirSocioView

from .views import (AreaView, LoginView, PerfilView, RegistroView,
                    RestablecerClaveView, SolicitarRecuperacionView)

urlpatterns = [
    path("administracion/cuentas-generales/", CuentasGeneralesView.as_view(), name="cuentas-generales"),
    path("administracion/cuentas/<int:id_usuario>/convertir-socio/", ConvertirSocioView.as_view(), name="convertir-socio"),
    path("registro/", RegistroView.as_view(), name="registro"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshConSesionView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("actividad/", ActividadView.as_view(), name="actividad"),
    path("yo/", PerfilView.as_view(), name="perfil"),
    path("areas/<slug:area>/", AreaView.as_view(), name="area"),
    path("recuperar/", SolicitarRecuperacionView.as_view(), name="recuperar"),
    path("restablecer/", RestablecerClaveView.as_view(), name="restablecer"),
]
