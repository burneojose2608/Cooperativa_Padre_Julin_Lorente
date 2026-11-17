from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.usuarios.serializers import RestablecerClaveSerializer, SolicitarRecuperacionSerializer
from apps.usuarios.services.recuperacion_service import ServicioRecuperacion


class LimiteRecuperacion(AnonRateThrottle):
    scope = "recuperacion"


class SolicitarRecuperacionView(APIView):
    """POST /api/auth/recuperar/  ·  pide el enlace. Responde igual exista o no la cuenta."""

    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [LimiteRecuperacion]

    def post(self, request):
        s = SolicitarRecuperacionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ServicioRecuperacion.solicitar_recuperacion(
            identificador=s.validated_data["identificador"], ip=request.META.get("REMOTE_ADDR")
        )
        return Response(
            {
                "mensaje": "Si la cuenta existe y está activa, el código temporal aparece en la consola "
                "del backend. Cópialo para restablecer tu contraseña. Vence en 30 minutos."
            }
        )


class RestablecerClaveView(APIView):
    """POST /api/auth/restablecer/  ·  usa el enlace para poner una contraseña nueva."""

    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [LimiteRecuperacion]

    def post(self, request):
        s = RestablecerClaveSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ServicioRecuperacion.restablecer_clave(
            **s.validated_data, ip=request.META.get("REMOTE_ADDR")
        )
        return Response({"mensaje": "Tu contraseña fue actualizada. Ya puedes iniciar sesión."})
