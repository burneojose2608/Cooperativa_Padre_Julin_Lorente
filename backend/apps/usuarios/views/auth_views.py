"""Capa de API: recibe la petición, valida formato, llama al servicio y responde."""
from rest_framework import status
from rest_framework.exceptions import ParseError, UnsupportedMediaType
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.usuarios.repositories import AuditoriaRepository, RolRepository
from apps.usuarios.services.roles_service import identificar_roles
from apps.usuarios.serializers import LoginSerializer, RegistroSerializer
from apps.usuarios.services import iniciar_sesion, registrar_socio


def _ip(request):
    return request.META.get("REMOTE_ADDR")


class LimiteAutenticacion(AnonRateThrottle):
    scope = "autenticacion"


class RegistroView(APIView):
    """POST /api/auth/registro/  ·  HU-001"""
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [LimiteAutenticacion]

    def post(self, request):
        s = RegistroSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        usuario = registrar_socio(**s.validated_data, ip=_ip(request))
        socio = getattr(usuario, "socio", None)
        return Response(
            {
                "id": usuario.id_usuario,
                "username": usuario.username,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "codigo_socio": socio.codigo_socio if socio else None,
                "roles": RolRepository.nombres_de(usuario),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/auth/login/  ·  HU-009"""
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [LimiteAutenticacion]

    def throttled(self, request, wait):
        AuditoriaRepository.registrar(accion="LOGIN", resultado="FALLO", ip=_ip(request))
        return super().throttled(request, wait)

    def handle_exception(self, error):
        if isinstance(error, (ParseError, UnsupportedMediaType)):
            AuditoriaRepository.registrar(accion="LOGIN", resultado="FALLO", ip=_ip(self.request))
        return super().handle_exception(error)

    def post(self, request):
        s = LoginSerializer(data=request.data)
        if not s.is_valid():
            AuditoriaRepository.registrar(accion="LOGIN", resultado="FALLO", ip=_ip(request))
            s.is_valid(raise_exception=True)
        return Response(iniciar_sesion(**s.validated_data, ip=_ip(request)))


class PerfilView(APIView):
    """GET /api/auth/yo/  ·  quién soy y con qué roles (requiere token)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "id": u.id_usuario, "username": u.username, "nombre": u.nombre,
            "apellido": u.apellido, "correo": u.correo,
            **identificar_roles(u),
        })
