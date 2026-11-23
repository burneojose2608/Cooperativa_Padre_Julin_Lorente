from django.urls import path
from . import views as v
from . import api_negocio as b
from . import api_comunidad as c
from . import api_reportes as r
from . import api_supervision as s

urlpatterns = [
    path("contenidos/aprobadores/", s.AprobadoresView.as_view()),
    path("contenidos/<int:pk>/aprobar/", s.AprobarContenidoView.as_view()),
    path("negocio/envios/", s.EnviosView.as_view()),
    path("negocio/segmentos/<int:pk>/", s.SegmentoSocioView.as_view()),
    path("negocio/referidos/", b.ReferidosView.as_view()),
    path("negocio/puntos/", b.PuntosView.as_view()),
    path("negocio/mis-actividades/", b.MisActividadesView.as_view()),
    path("negocio/canjes/", b.CanjesView.as_view()),
    path("negocio/ranking/", c.RankingView.as_view()),
    path("negocio/perfil-publico/", c.PerfilPublicoView.as_view()),
    path("negocio/comunidad/", c.ComunidadView.as_view()),
    path("negocio/comunidad/<int:pk>/imagen/", c.ImagenComunidadView.as_view()),
    path("negocio/comunidad/<int:pk>/foto-autor/", c.FotoAutorComunidadView.as_view()),
    path("negocio/comunidad/<int:pk>/comentarios/<int:comentario>/foto-autor/", c.FotoComentaristaView.as_view()),
    path("negocio/comunidad/<int:pk>/<str:accion>/", c.InteraccionView.as_view()),
    path("negocio/moderacion/", c.ModeracionView.as_view()),
    path("negocio/reportes/", r.ReportesView.as_view()),
    path("negocio/certificados/<int:pk>/pdf/", r.CertificadoView.as_view()),
    path("negocio/capacitaciones/<int:pk>/aula/", b.AulaView.as_view()),
    path("negocio/<str:recurso>/<int:pk>/participantes/", b.ParticipantesView.as_view()),
    path("negocio/<str:recurso>/<int:pk>/<str:accion>/", b.AccionView.as_view()),
    path("negocio/<str:recurso>/<int:pk>/", b.RecursoDetalleView.as_view()),
    path("negocio/<str:recurso>/", b.CatalogoView.as_view()),
    path("invitaciones/<str:codigo>/referir/", b.ReferidoPublicoView.as_view()),
    path("referidos/confirmar/<str:token>/", b.ConfirmarReferidoView.as_view()),
    path("certificados/verificar/<str:codigo>/", r.VerificarCertificadoView.as_view()),
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
