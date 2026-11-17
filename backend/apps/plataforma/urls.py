from django.urls import path
from . import views as v

urlpatterns = [
    path("referidos/codigo/", v.CodigoReferidoView.as_view()),
    path("invitaciones/<str:codigo>/", v.InvitacionView.as_view()),
    path("reglas-puntos/", v.ReglasPuntosView.as_view()),
    path("contenidos/", v.ContenidosView.as_view()),
    path("contenidos/<int:id_contenido>/", v.ContenidoDetalleView.as_view()),
    path("contenidos/<int:id_contenido>/publicar/", v.PublicarContenidoView.as_view()),
    path("contenidos/<int:id_contenido>/retirar/", v.RetirarContenidoView.as_view()),
    path("publicaciones/", v.PublicacionesView.as_view()),
    path("materiales/", v.MaterialesView.as_view()),
    path("materiales/<int:id_material>/", v.MaterialDetalleView.as_view()),
    path("materiales/<int:id_material>/archivo/", v.MaterialArchivoView.as_view()),
    path("notificaciones/", v.NotificacionesView.as_view()),
    path("notificaciones/<int:id_notificacion>/leida/", v.NotificacionLeidaView.as_view()),
    path("preferencias/", v.PreferenciasView.as_view()),
]
