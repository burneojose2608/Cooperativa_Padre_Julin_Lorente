from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.usuarios.services.roles_service import CODIGOS_DE_AREA, identificar_roles


class AreaView(APIView):
    """GET /api/auth/areas/<area>/  ·  200 si el usuario tiene el rol de esa área, 403 si no.
    Es la comprobación de seguridad real: el frontend solo la usa para decidir qué mostrar."""
    permission_classes = [IsAuthenticated]

    def get(self, request, area):
        if area not in CODIGOS_DE_AREA:
            raise Http404
        info = identificar_roles(request.user)
        if area not in info["areas"]:
            raise PermissionDenied("No tienes permiso para acceder a esta sección.")
        return Response({"area": area, "roles": info["roles"]})
