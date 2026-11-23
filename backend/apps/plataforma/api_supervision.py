from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.usuarios.models import Usuario, Socio
from apps.usuarios.serializers.gestion_serializers import EstrictoSerializer
from . import models as m, negocio as n
from .api_negocio import validar


class AprobadoresView(APIView):
    def get(self,request):
        from .contenidos import exigir_permiso
        exigir_permiso(request.user,'contenidos','gestionar')
        return Response([{'id':u.pk,'nombre':f'{u.nombre} {u.apellido}'} for u in Usuario.objects.filter(
            estado='ACTIVA',roles_asignados__rol__nombre=n.GESTOR).distinct()])


class AprobarContenidoView(APIView):
    @transaction.atomic
    def post(self,request,pk):
        from .contenidos import exigir_permiso
        exigir_permiso(request.user,'contenidos','publicar')
        c=get_object_or_404(m.ContenidoInstitucional.objects.select_for_update(),pk=pk)
        if c.aprobador_id != request.user.pk: raise PermissionDenied('Solo el responsable designado puede aprobar.')
        if not c.requiere_aprobacion or c.estado!='BORRADOR': raise ValidationError('El contenido no está pendiente de aprobación.')
        c.aprobado_en=timezone.now();c.save(update_fields=['aprobado_en'])
        n.auditar(request.user,c,'APROBAR_CONTENIDO')
        return Response({'mensaje':'Contenido aprobado. Ya puede publicarse.'})


class EnviosView(APIView):
    def get(self,request):
        n.exigir(request.user,'notificaciones',[n.ADMIN])
        q=m.EnvioNotificacion.objects.select_related('notificacion__destinatario').order_by('-pk')
        for campo in ['estado','canal']:
            if request.query_params.get(campo): q=q.filter(**{campo:request.query_params[campo]})
        return Response({'resultados':[{'id':e.pk,'evento':e.notificacion.evento,'canal':e.canal,'estado':e.estado,
            'intentos':e.intentos,'enviada_en':e.enviada_en,'error':e.ultimo_error,
            'destinatario':e.notificacion.destinatario.correo[:2]+'•••@'+e.notificacion.destinatario.correo.split('@')[-1]}
             for e in q[:200]]})


class SegmentoSocioView(APIView):
    @transaction.atomic
    def put(self,request,pk):
        n.exigir(request.user,'campanas',[n.ADMIN])
        class Datos(EstrictoSerializer):
            TIPO_SOCIO=serializers.CharField(max_length=100,required=False)
            PRODUCTO=serializers.CharField(max_length=100,required=False)
            AGENCIA=serializers.CharField(max_length=100,required=False)
        datos=validar(Datos,request.data)
        s=get_object_or_404(Socio.objects.select_for_update(),pk=pk)
        s.segmento=datos;s.save(update_fields=['segmento'])
        n.auditar(request.user,s,'CONFIGURAR_SEGMENTO',segmento=datos)
        return Response({'mensaje':'Atributos de segmentación guardados.'})
