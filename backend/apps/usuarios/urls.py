from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (AreaView, LoginView, PerfilView, RegistroView,
                    RestablecerClaveView, SolicitarRecuperacionView)

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("yo/", PerfilView.as_view(), name="perfil"),
    path("areas/<slug:area>/", AreaView.as_view(), name="area"),
    path("recuperar/", SolicitarRecuperacionView.as_view(), name="recuperar"),
    path("restablecer/", RestablecerClaveView.as_view(), name="restablecer"),
]
