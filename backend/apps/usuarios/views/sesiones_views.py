from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.usuarios.serializers.auth_serializers import RefreshSerializer
from apps.usuarios.services.sesiones_service import CLAIM_SESION, cerrar_sesion, renovar_access
from .auth_views import LimiteAutenticacion


class RefreshConSesionView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [LimiteAutenticacion]

    def get_authenticate_header(self, request):
        return 'Bearer realm="api"'

    def post(self, request):
        entrada = RefreshSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        return Response(renovar_access(entrada.validated_data["refresh"], ip=request.META.get("REMOTE_ADDR")))


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cerrar_sesion(id_sesion=request.auth.get(CLAIM_SESION), usuario=request.user,
                      ip=request.META.get("REMOTE_ADDR"))
        return Response(status=204)


class ActividadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # La autenticación ya comprobó y actualizó ultimo_uso; no revive sesiones.
        return Response(status=204)
