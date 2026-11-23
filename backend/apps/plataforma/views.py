from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models, transaction
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.usuarios.repositories import RolRepository
from apps.usuarios.permissions import tiene_permiso, tiene_rol, permisos_de
from apps.usuarios.views.gestion_views import validar
from .models import (CodigoReferido, ReglaPuntos, ContenidoInstitucional, MaterialEducativo,
                     ModuloCapacitacion, Notificacion, PreferenciaNotificacion)
from .serializers import ReglaSerializer, ContenidoSerializer, MaterialSerializer, PreferenciaSerializer, RetirarSerializer
from .contenidos import guardar_contenido, publicar_contenido, retirar_contenido, guardar_material, eliminar_material
from .notificaciones import EVENTOS, CANALES
from .negocio import socio_validado


def datos_contenido(c):
    return {"id": c.pk, "titulo": c.titulo, "cuerpo": c.cuerpo, "categoria": c.categoria,
            "tipo": c.tipo, "estado": c.estado, "desde": c.desde, "hasta": c.hasta,
            "autor": c.autor_id, "visible": c.es_visible(timezone.localdate()),
            "requiere_aprobacion": c.requiere_aprobacion, "aprobador": c.aprobador_id, "aprobado_en": c.aprobado_en,
            "materiales": [datos_material(m) for m in c.materiales.all()]}


def datos_material(m):
    return {"id": m.pk, "titulo": m.titulo, "categoria": m.categoria, "formato": m.formato,
            "tamano_bytes": m.tamano_bytes, "contenido": m.contenido_id,
            "modulos": list(m.modulos.values_list("pk", flat=True)), "autor": m.autor_id}


class CodigoReferidoView(APIView):
    permission_classes = [tiene_rol("Socio"), tiene_permiso("referidos", "compartir")]

    def get(self, request):
        socio = socio_validado(request.user)
        codigo = CodigoReferido.generar_para(socio)
        return Response({"codigo": codigo.valor, "enlace": codigo.generar_enlace(settings.FRONTEND_URL)})


class InvitacionView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [AnonRateThrottle]

    def get(self, request, codigo):
        fila = get_object_or_404(CodigoReferido.objects.select_related("socio__usuario"), valor=codigo)
        if not fila.es_valido():
            raise NotFound("La invitación no está disponible.")
        return Response({"codigo": fila.valor, "mensaje": "Te invitaron a conocer la plataforma de la cooperativa."})


class ReglasPuntosView(APIView):
    permission_classes = [tiene_rol("Administrador"), tiene_permiso("puntos", "configurar")]

    def get(self, request):
        hoy = timezone.localdate()
        return Response({"actividades": ReglaPuntos.ACTIVIDADES, "reglas": [
            {"id": r.pk, "tipo_actividad": r.tipo_actividad, "puntos": r.puntos,
             "limite_periodo": r.limite_periodo, "periodo": r.periodo,
             "vigente_desde": r.vigente_desde, "vigente_hasta": r.vigente_hasta, "version": r.version,
             "actual": (ReglaPuntos.vigente_para(r.tipo_actividad, hoy) or ReglaPuntos()).pk == r.pk}
            for r in ReglaPuntos.objects.order_by("-pk")]})

    def post(self, request):
        r = ReglaPuntos.configurar_version(validar(ReglaSerializer, request.data), request.user)
        return Response({"id": r.pk, "version": r.version}, status=201)


class ContenidosView(APIView):
    permission_classes = [tiene_rol("Gestor de contenidos"), tiene_permiso("contenidos", "gestionar")]

    def get(self, request):
        return Response([datos_contenido(c) for c in ContenidoInstitucional.objects.order_by("-pk")[:200]])

    def post(self, request):
        c = guardar_contenido(request.user, validar(ContenidoSerializer, request.data))
        return Response(datos_contenido(c), status=201)


class ContenidoDetalleView(APIView):
    permission_classes = [tiene_rol("Gestor de contenidos"), tiene_permiso("contenidos", "gestionar")]

    def put(self, request, id_contenido):
        get_object_or_404(ContenidoInstitucional, pk=id_contenido)
        c = guardar_contenido(request.user, validar(ContenidoSerializer, request.data), id_contenido)
        return Response(datos_contenido(c))


class PublicarContenidoView(APIView):
    permission_classes = [tiene_rol("Gestor de contenidos"), tiene_permiso("contenidos", "publicar")]

    def post(self, request, id_contenido):
        get_object_or_404(ContenidoInstitucional, pk=id_contenido)
        return Response(datos_contenido(publicar_contenido(request.user, id_contenido)))


class RetirarContenidoView(PublicarContenidoView):
    def post(self, request, id_contenido):
        get_object_or_404(ContenidoInstitucional, pk=id_contenido)
        motivo = validar(RetirarSerializer, request.data)["motivo"]
        return Response(datos_contenido(retirar_contenido(request.user, id_contenido, motivo)))


class PublicacionesView(APIView):
    def get(self, request):
        hoy = timezone.localdate()
        visibles = ContenidoInstitucional.objects.filter(estado="PUBLICADO", desde__lte=hoy).filter(
            models.Q(hasta__isnull=True) | models.Q(hasta__gte=hoy)).order_by("-desde", "-pk")
        return Response([datos_contenido(c) for c in visibles[:100]])


class MaterialesView(APIView):
    permission_classes = [tiene_rol("Gestor de contenidos", "Responsable de Responsabilidad Social"), tiene_permiso("materiales", "gestionar")]

    def get(self, request):
        return Response({"materiales": [datos_material(m) for m in MaterialEducativo.objects.order_by("-pk")[:200]],
            "modulos": [{"id": m.pk, "titulo": m.titulo, "capacitacion": m.capacitacion.titulo}
                        for m in ModuloCapacitacion.objects.select_related("capacitacion").order_by("capacitacion_id", "orden")]})

    def post(self, request):
        m = guardar_material(request.user, validar(MaterialSerializer, request.data))
        return Response(datos_material(m), status=201)


class MaterialDetalleView(APIView):
    permission_classes = [tiene_rol("Gestor de contenidos", "Responsable de Responsabilidad Social"), tiene_permiso("materiales", "gestionar")]
    def put(self, request, id_material):
        get_object_or_404(MaterialEducativo, pk=id_material)
        return Response(datos_material(guardar_material(request.user, validar(MaterialSerializer, request.data), id_material)))

    def delete(self, request, id_material):
        get_object_or_404(MaterialEducativo, pk=id_material)
        eliminar_material(request.user, id_material)
        return Response(status=204)


class MaterialArchivoView(APIView):
    def get(self, request, id_material):
        m = get_object_or_404(MaterialEducativo, pk=id_material)
        usuario = request.user
        roles = set(RolRepository.nombres_de(usuario))
        permisos = permisos_de(usuario)
        gestor = (bool(roles & {"Gestor de contenidos", "Responsable de Responsabilidad Social"})
                  and permisos.filter(modulo="materiales", accion="gestionar").exists())
        inscrito = (
            usuario.is_active and "Socio" in roles
            and permisos.filter(modulo="formacion", accion="participar").exists()
            and m.modulos.filter(
                capacitacion__estado="PUBLICADA",
                capacitacion__inscripcion__socio__usuario=usuario,
                capacitacion__inscripcion__socio__validado_en__isnull=False,
            ).exists()
        )
        if not gestor and not inscrito and not (m.contenido and m.contenido.es_visible(timezone.localdate())):
            raise NotFound("El material no está disponible.")
        if not default_storage.exists(m.recurso):
            raise NotFound("El archivo no está disponible.")
        respuesta = FileResponse(default_storage.open(m.recurso), as_attachment=True,
                                filename=m.recurso.rsplit("/", 1)[-1], content_type=m.formato)
        respuesta["X-Content-Type-Options"] = "nosniff"
        respuesta["Cache-Control"] = "private, no-store"
        return respuesta


class NotificacionesView(APIView):
    def get(self, request):
        q = Notificacion.objects.filter(destinatario=request.user, estado="ENVIADA").order_by("-creada_en", "-pk")
        return Response({"no_leidas": q.filter(leida_en__isnull=True).count(), "resultados": [
            {"id": n.pk, "evento": n.evento, "titulo": n.titulo, "mensaje": n.mensaje,
             "creada_en": n.creada_en, "leida_en": n.leida_en} for n in q[:100]]})


class NotificacionLeidaView(APIView):
    def post(self, request, id_notificacion):
        n = get_object_or_404(Notificacion, pk=id_notificacion, estado="ENVIADA")
        if n.destinatario_id != request.user.pk:
            raise PermissionDenied("No puedes acceder a las notificaciones de otra cuenta.")
        n.marcar_leida(request.user)
        return Response({"mensaje": "Notificación marcada como leída."})


class PreferenciasView(APIView):
    def get(self, request):
        existentes = {(p.evento, p.canal): p.habilitada for p in PreferenciaNotificacion.objects.filter(usuario=request.user)}
        from .notificaciones import EVENTOS_OBLIGATORIOS
        return Response([{"evento": evento, "titulo": titulo, "canal": canal, "obligatoria": evento in EVENTOS_OBLIGATORIOS,
                          "habilitada": evento in EVENTOS_OBLIGATORIOS or existentes.get((evento, canal), True)}
                         for evento, titulo in EVENTOS.items() for canal in CANALES])

    def put(self, request):
        datos = validar(PreferenciaSerializer, request.data)
        habilitada = datos.pop("habilitada")
        PreferenciaNotificacion.objects.update_or_create(usuario=request.user, **datos, defaults={"habilitada": habilitada})
        return Response({"mensaje": "Preferencia guardada."})
