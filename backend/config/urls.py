from django.urls import include, path

urlpatterns = [
    path("api/plataforma/", include("apps.plataforma.urls")),
    path("api/auth/", include("apps.usuarios.urls")),
]
