from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.usuarios.services.sesiones_service import CLAIM_SESION, MENSAJE_SESION, validar_sesion


class AutenticacionConSesion(JWTAuthentication):
    def authenticate(self, request):
        try:
            autenticacion = super().authenticate(request)
        except AuthenticationFailed:
            raise AuthenticationFailed(MENSAJE_SESION, code="sesion_invalida") from None
        if autenticacion is not None:
            usuario, token = autenticacion
            validar_sesion(id_sesion=token.get(CLAIM_SESION), usuario=usuario,
                           ip=request.META.get("REMOTE_ADDR"))
        return autenticacion
