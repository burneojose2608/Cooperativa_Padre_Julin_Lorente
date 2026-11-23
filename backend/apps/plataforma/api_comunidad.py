from datetime import timedelta
from django.core.files.storage import default_storage
from django.db import transaction
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.usuarios.models import Socio
from apps.usuarios.serializers.gestion_serializers import EstrictoSerializer
from apps.usuarios.views.gestion_views import respuesta_foto
from . import models as m
from . import negocio as n
from .api_negocio import validar
from .archivos import guardar_archivo, borrar_archivo


def alias(usuario, predeterminado='Socio'):
    s=Socio.objects.filter(usuario=usuario).first()
    return s.alias if s and s.alias else predeterminado


def nombre_comentarista(usuario):
    nombres = usuario.nombre.split()
    return alias(usuario, nombres[0] if nombres else 'Socio')


def publicacion_datos(p):
    return {'id':p.pk,'alias':alias(p.usuario),'texto':p.texto,'fecha':p.creado_en,'imagen':bool(p.imagen),
      'tiene_foto': bool(p.usuario.foto),
      'comentarios':[{'id':c.pk,'alias':nombre_comentarista(c.usuario),'texto':c.texto,'fecha':c.creado_en,
                      'tiene_foto': bool(c.usuario.foto)}
          for c in m.Comentario.objects.filter(publicacion=p,estado='VISIBLE').select_related('usuario').order_by('pk')[:100]],
      'reacciones':m.Reaccion.objects.filter(publicacion=p).count()}


class ComunidadView(APIView):
    def get(self,request):
        n.socio_de(request.user,'comunidad')
        return Response({'resultados':[publicacion_datos(p) for p in m.Publicacion.objects.filter(
            estado_moderacion='VISIBLE').select_related('usuario').order_by('-pk')[:100]]})

    def post(self,request):
        n.comunidad_habilitada(request.user)
        class Datos(EstrictoSerializer):
            texto=serializers.CharField(max_length=10000)
            imagen=serializers.FileField(required=False)
        d=validar(Datos,request.data)
        ruta=''
        try:
            if d.get('imagen'): ruta,_,_=guardar_archivo(d['imagen'],carpeta='comunidad',solo_imagen=True)
            with transaction.atomic():
                p=m.Publicacion.objects.create(usuario=request.user,texto=d['texto'],imagen=ruta)
                n.auditar(request.user,p,'PUBLICAR_COMUNIDAD')
        except Exception:
            borrar_archivo(ruta)
            raise
        return Response(publicacion_datos(p),status=201)


class InteraccionView(APIView):
    @transaction.atomic
    def post(self,request,pk,accion):
        n.comunidad_habilitada(request.user)
        p=get_object_or_404(m.Publicacion.objects.select_for_update(),pk=pk,estado_moderacion='VISIBLE')
        if accion=='comentar':
            class Datos(EstrictoSerializer): texto=serializers.CharField(max_length=2000)
            d=validar(Datos,request.data)
            m.Comentario.objects.create(usuario=request.user,publicacion=p,**d)
        elif accion=='reaccionar':
            class Datos(EstrictoSerializer): tipo=serializers.ChoiceField(choices=['ME_GUSTA','APOYO','CELEBRO'])
            d=validar(Datos,request.data)
            m.Reaccion.objects.update_or_create(usuario=request.user,publicacion=p,defaults=d)
        elif accion=='reportar':
            class Datos(EstrictoSerializer):
                motivo=serializers.CharField(max_length=1000)
                comentario=serializers.IntegerField(min_value=1,required=False)
            d=validar(Datos,request.data)
            comentario=None
            if d.get('comentario'): comentario=get_object_or_404(m.Comentario,pk=d['comentario'],publicacion=p,estado='VISIBLE')
            m.ReporteComunidad.objects.create(usuario=request.user,publicacion=None if comentario else p,
                                               comentario=comentario,motivo=d['motivo'])
        else: raise NotFound()
        return Response({'mensaje':'Operación registrada.'})


class ImagenComunidadView(APIView):
    def get(self,request,pk):
        n.socio_de(request.user,'comunidad')
        p=get_object_or_404(m.Publicacion,pk=pk,estado_moderacion='VISIBLE')
        if not p.imagen or not default_storage.exists(p.imagen): raise NotFound()
        r=FileResponse(default_storage.open(p.imagen))
        r['X-Content-Type-Options']='nosniff';r['Cache-Control']='private, no-store'
        return r


class FotoAutorComunidadView(APIView):
    def get(self, request, pk):
        n.socio_de(request.user, 'comunidad')
        publicacion = get_object_or_404(
            m.Publicacion.objects.select_related('usuario'), pk=pk, estado_moderacion='VISIBLE',
        )
        return respuesta_foto(publicacion.usuario)


class FotoComentaristaView(APIView):
    def get(self, request, pk, comentario):
        n.socio_de(request.user, 'comunidad')
        autor = get_object_or_404(
            m.Comentario.objects.select_related('usuario'), pk=comentario, publicacion_id=pk,
            estado='VISIBLE', publicacion__estado_moderacion='VISIBLE',
        ).usuario
        return respuesta_foto(autor)


class ModeracionView(APIView):
    def get(self,request):
        n.exigir(request.user,'comunidad',[n.ADMIN,n.GESTOR])
        return Response({'resultados':[{'id':r.pk,'motivo':r.motivo,'publicacion':r.publicacion_id,
            'comentario':r.comentario_id,'fecha':r.creado_en,'texto':r.publicacion.texto if r.publicacion else r.comentario.texto}
            for r in m.ReporteComunidad.objects.filter(resuelto_en__isnull=True).select_related('publicacion','comentario').order_by('pk')[:200]]})

    @transaction.atomic
    def post(self,request):
        n.exigir(request.user,'comunidad',[n.ADMIN,n.GESTOR])
        class Datos(EstrictoSerializer):
            reporte=serializers.IntegerField(min_value=1)
            accion=serializers.ChoiceField(choices=['OCULTAR','ELIMINAR','DESCARTAR'])
            motivo=serializers.CharField(max_length=1000)
            suspension_dias=serializers.IntegerField(min_value=0,max_value=365,default=0)
        d=validar(Datos,request.data)
        r=get_object_or_404(m.ReporteComunidad.objects.select_for_update(),pk=d['reporte'],resuelto_en__isnull=True)
        objeto=r.publicacion or r.comentario
        if d['accion']!='DESCARTAR':
            campo='estado_moderacion' if r.publicacion else 'estado'
            setattr(objeto,campo,'OCULTA' if d['accion']=='OCULTAR' else 'ELIMINADA')
            objeto.save(update_fields=[campo])
        if d['suspension_dias']:
            s=get_object_or_404(Socio,usuario=objeto.usuario)
            m.SuspensionComunidad.objects.create(socio=s,hasta=timezone.now()+timedelta(days=d['suspension_dias']),
                                                 motivo=d['motivo'],responsable=request.user)
        r.resuelto_en=timezone.now();r.resolucion=d['motivo'];r.save()
        n.auditar(request.user,r,'MODERAR_COMUNIDAD',decision=d['accion'],motivo=d['motivo'])
        return Response({'mensaje':'Reporte resuelto.'})


class PerfilPublicoView(APIView):
    def get(self,request):
        s=n.socio_de(request.user,'comunidad')
        return Response({'alias':s.alias,'ranking_publico':s.ranking_publico})

    def put(self,request):
        s=n.socio_de(request.user,'comunidad')
        class Datos(EstrictoSerializer):
            alias=serializers.CharField(max_length=60)
            ranking_publico=serializers.BooleanField()
        d=validar(Datos,request.data)
        s.alias=d['alias'];s.ranking_publico=d['ranking_publico'];s.save(update_fields=['alias','ranking_publico'])
        return Response({'mensaje':'Preferencias públicas guardadas.'})


class RankingView(APIView):
    def get(self,request):
        s=n.socio_de(request.user,'gamificacion')
        class Filtros(EstrictoSerializer):
            desde=serializers.DateField(required=False)
            hasta=serializers.DateField(required=False)
        f=validar(Filtros,request.query_params)
        q=m.MovimientoPuntos.objects.filter(tipo='ACREDITACION',socio__usuario__estado='ACTIVA')
        if f.get('desde'): q=q.filter(creado_en__date__gte=f['desde'])
        if f.get('hasta'): q=q.filter(creado_en__date__lte=f['hasta'])
        # Reversos se descuentan por el origen original, no por la fecha de corrección.
        anulados=m.MovimientoPuntos.objects.filter(tipo='REVERSO').values_list('origen_tipo','origen_id')
        anulados=set(anulados)
        puntos={}
        for v in q.values('socio_id','cantidad','origen_tipo','origen_id'):
            if (v['origen_tipo'],v['origen_id']) not in anulados:
                puntos[v['socio_id']]=puntos.get(v['socio_id'],0)+v['cantidad']
        orden=sorted(puntos,key=lambda k:(-puntos[k],k))
        socios={p.pk:p for p in Socio.objects.filter(pk__in=orden)}
        return Response({'mi_posicion':orden.index(s.pk)+1 if s.pk in orden else None,
            'resultados':[{'posicion':i+1,'alias':socios[k].alias or 'Socio','puntos':puntos[k]}
                          for i,k in enumerate(orden) if socios[k].ranking_publico][:100]})
