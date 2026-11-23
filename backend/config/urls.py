from django.db import connection
from django.http import JsonResponse
from django.urls import include, path
from django.utils import timezone


def estado_salud(_request):
    """Endpoint de monitoreo de disponibilidad (T-029 / RNF-08) sin exponer datos internos."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse({"estado": "ok", "base_datos": "ok", "fecha": timezone.now().isoformat()})
    except Exception:
        return JsonResponse({"estado": "degradado", "base_datos": "error"}, status=503)


urlpatterns = [
    path("api/salud/", estado_salud),
    path("api/plataforma/", include("apps.plataforma.urls")),
    path("api/auth/", include("apps.usuarios.urls")),
]
