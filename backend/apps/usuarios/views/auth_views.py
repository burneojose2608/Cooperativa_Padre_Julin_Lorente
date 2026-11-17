"""Capa de API: recibe la petición, valida formato, llama al servicio y responde."""

from rest_framework import status
from rest_framework.exceptions import ParseError, UnsupportedMediaType
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.usuarios.repositories import AuditoriaRepository, RolRepository
from apps.usuarios.services.roles_service import ServicioAutorizacion
from apps.usuarios.serializers import LoginSerializer, RegistroSerializer
from apps.usuarios.services import ControlAcceso, ServicioRegistro


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
        usuario = ServicioRegistro.registrar_cuenta(**s.validated_data, ip=_ip(request))
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
        return Response(ControlAcceso.iniciar_sesion(**s.validated_data, ip=_ip(request)))


class PerfilView(APIView):
    """GET /api/auth/yo/  ·  quién soy y con qué roles (requiere token)"""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id_usuario: int | None = None) -> Response:
        self._comprobar_titular(request, id_usuario)
        from .gestion_views import perfil
        return Response(perfil(request.user))

    @staticmethod
    def _comprobar_titular(request: Request, id_usuario: int | None) -> None:
        from rest_framework.exceptions import PermissionDenied
        destino = id_usuario or request.query_params.get("id")
        if destino is not None and str(destino) != str(request.user.pk):
            raise PermissionDenied("Solo puedes consultar o modificar tu propio perfil.")

    def patch(self, request: Request, id_usuario: int | None = None) -> Response:
        self._comprobar_titular(request, id_usuario)
        from .gestion_views import perfil, validar
        from apps.usuarios.serializers.gestion_serializers import ContactoSerializer
        from apps.usuarios.services.gestion_cuentas_service import ServicioGestionCuentas
        u = ServicioGestionCuentas.actualizar_contacto(request.user, **validar(ContactoSerializer, request.data))
        return Response(perfil(u))
