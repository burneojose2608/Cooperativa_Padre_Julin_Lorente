import csv
import io
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from apps.usuarios.models import Usuario
from . import models as m
from . import negocio as n
from .api_negocio import filtrar_periodo, validar
from .documentos import pdf_texto


class CertificadoView(APIView):
    def get(self,request,pk):
        s=n.socio_de(request.user,'formacion')
        c=get_object_or_404(m.Certificado,pk=pk,inscripcion__socio=s,inscripcion__estado='APROBADO')
        u=s.usuario
        pdf=pdf_texto('Certificado de capacitación',[
            'Cooperativa de Ahorro y Crédito Padre Julián Lorente',
            f'Se certifica que {u.nombre} {u.apellido} aprobó:',c.inscripcion.capacitacion.titulo,
            f'Fecha de emisión: {c.emitido_en.date()}',f'Código de verificación: {c.codigo_verificacion}',
            f'Consulta: {settings.FRONTEND_URL}/verificar-certificado/{c.codigo_verificacion}',
            'Este certificado corresponde a las actividades del prototipo de formación.'])
        r=HttpResponse(pdf,content_type='application/pdf')
        r['Content-Disposition']=f'attachment; filename="certificado-{c.pk}.pdf"'
        r['Cache-Control']='private, no-store'
        return r


class VerificarCertificadoView(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[]
    throttle_classes=[AnonRateThrottle]
    def get(self,request,codigo):
        c=m.Certificado.objects.filter(codigo_verificacion=codigo,inscripcion__estado='APROBADO').first()
        return Response({'valido':bool(c),'titulo':c.inscripcion.capacitacion.titulo if c else None,
                         'emitido_en':c.emitido_en if c else None,'codigo':codigo if c else None})


def total(q): return q.aggregate(valor=models.Sum('cantidad'))['valor'] or 0


def celda_csv_segura(valor):
    texto = str(valor)
    if texto.startswith(('\t', '\r', '\n')) or texto.lstrip().startswith(('=', '+', '-', '@')):
        return "'" + texto
    return texto


class ReportesView(APIView):
    def get(self,request):
        tipo=request.query_params.get('tipo','general')
        roles={'general':[n.ADMIN],'referidos':[n.ADMIN,n.MARKETING],
               'social':[n.ADMIN,n.RSE],'gamificacion':[n.ADMIN]}
        if tipo not in roles: raise NotFound()
        n.exigir(request.user,'reportes',roles[tipo])
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')
        campo_fecha = serializers.DateField()
        if desde is not None and hasta is not None:
            if campo_fecha.run_validation(desde) > campo_fecha.run_validation(hasta):
                raise ValidationError({'hasta': 'La fecha final debe ser igual o posterior a la inicial.'})
        referidos=filtrar_periodo(m.Referido.objects.all(),request,'creado_en')
        if request.query_params.get('campana'):
            pk=serializers.IntegerField(min_value=1).run_validation(request.query_params['campana'])
            referidos=referidos.filter(campana_id=pk)
        if request.query_params.get('segmento'):
            referidos=referidos.filter(campana__segmentacion__has_key=request.query_params['segmento'])
        movimientos=filtrar_periodo(m.MovimientoPuntos.objects.all(),request,'creado_en')
        inscritos=filtrar_periodo(m.Inscripcion.objects.all(),request,'creado_en')
        certificados=filtrar_periodo(m.Certificado.objects.all(),request,'emitido_en')
        filas=[]
        if tipo in ['general','referidos']:
            cantidad=referidos.count();conversiones=referidos.filter(estado='CONVERTIDO').count()
            filas.extend([{'indicador':'Referidos','valor':cantidad},{'indicador':'Conversiones','valor':conversiones},
                {'indicador':'Tasa de conversión (%)','valor':round(100*conversiones/cantidad,2) if cantidad else 0}])
            conversiones_q=filtrar_periodo(m.Conversion.objects.filter(referido__in=referidos),request,'fecha_validacion')
            gastos=filtrar_periodo(m.GastoCampana.objects.all(),request,'fecha')
            if request.query_params.get('campana'): gastos=gastos.filter(campana_id=request.query_params['campana'])
            if request.query_params.get('segmento'): gastos=gastos.filter(campana__segmentacion__has_key=request.query_params['segmento'])
            costo=gastos.aggregate(total=models.Sum('importe'))['total']
            monto=conversiones_q.aggregate(total=models.Sum('monto_captado'))['total']
            filas.extend([{'indicador':'Costo registrado de captación','valor':costo if costo is not None else 'Sin gastos registrados'},
                {'indicador':'CAC por conversión','valor':round(costo/conversiones_q.count(),2) if costo is not None and conversiones_q.exists() else 'Sin datos suficientes'},
                {'indicador':'Volumen de captación confirmado','valor':monto if monto is not None else 'Sin montos confirmados'}])
            for c in m.Campana.objects.all():
                q=referidos.filter(campana=c)
                if q.exists(): filas.append({'indicador':f'Conversiones en {c.nombre}','valor':q.filter(estado='CONVERTIDO').count()})
        if tipo in ['general','social']:
            filas.extend([{'indicador':'Inscritos','valor':inscritos.count()},
                {'indicador':'Aprobados','valor':inscritos.filter(estado='APROBADO').count()},
                {'indicador':'Certificados','valor':certificados.count()},
                {'indicador':'Horas de formación aprobadas','valor':sum(i.capacitacion.duracion for i in inscritos.filter(estado='APROBADO').select_related('capacitacion'))}])
            rangos={'Menor de 18':0,'18 a 29':0,'30 a 59':0,'60 o más':0}
            for i in inscritos.select_related('socio__usuario'):
                nacimiento=i.socio.usuario.fecha_nacimiento;hoy=timezone.localdate()
                edad=hoy.year-nacimiento.year-((hoy.month,hoy.day)<(nacimiento.month,nacimiento.day))
                rangos['Menor de 18' if edad<18 else '18 a 29' if edad<30 else '30 a 59' if edad<60 else '60 o más']+=1
            filas.extend({'indicador':f'Inscripciones por edad: {k}','valor':v} for k,v in rangos.items())
        if tipo in ['general','gamificacion']:
            filas.extend([{'indicador':'Puntos emitidos','valor':total(movimientos.filter(tipo='ACREDITACION'))},
                {'indicador':'Puntos canjeados','valor':total(movimientos.filter(tipo='DESCUENTO'))},
                {'indicador':'Puntos revertidos','valor':total(movimientos.filter(tipo='REVERSO'))}])
            canjes=filtrar_periodo(m.Canje.objects.filter(estado__in=['APROBADA','ENTREGADA']),request,'creado_en')
            filas.extend({'indicador':f'Canjes de {b["beneficio__nombre"]}','valor':b['cantidad']}
                for b in canjes.values('beneficio__nombre').annotate(cantidad=models.Count('pk')))
            resultados = filtrar_periodo(m.Ganador.objects.filter(sorteo__estado='EJECUTADO'),request,'fecha')
            resumen = resultados.values('sorteo_id','sorteo__nombre').annotate(
                ganadores=models.Count('pk',filter=models.Q(es_suplente=False)),
                suplentes=models.Count('pk',filter=models.Q(es_suplente=True)),
            ).order_by('sorteo__nombre','sorteo_id')
            filas.append({'indicador':'Sorteos ejecutados','valor':resumen.count()})
            for resultado in resumen:
                nombre = resultado['sorteo__nombre']
                filas.extend([
                    {'indicador':f'Ganadores de {nombre}','valor':resultado['ganadores']},
                    {'indicador':f'Suplentes de {nombre}','valor':resultado['suplentes']},
                ])
        if tipo=='general':
            filas.insert(0,{'indicador':'Usuarios activos','valor':Usuario.objects.filter(estado='ACTIVA').count()})
            inicio_reciente = timezone.localdate() - timedelta(days=6)
            filas.append({'indicador':'Referidos de los últimos 7 días',
                          'valor':referidos.filter(creado_en__date__gte=inicio_reciente).count()})
        generado=timezone.now().isoformat()
        filtros={k:request.query_params[k] for k in ['tipo','desde','hasta','campana','segmento'] if k in request.query_params}
        formato=request.query_params.get('formato','json')
        if formato=='json': return Response({'generado_en':generado,'filtros':filtros,'resultados':filas})
        if formato=='csv':
            salida=io.StringIO(newline='');w=csv.writer(salida)
            w.writerow(['Generado',generado]);w.writerow(['Filtros',celda_csv_segura(filtros)]);w.writerow(['Indicador','Valor'])
            for f in filas: w.writerow([celda_csv_segura(f['indicador']),celda_csv_segura(f['valor'])])
            r=HttpResponse('\ufeff'+salida.getvalue(),content_type='text/csv; charset=utf-8')
        elif formato=='pdf':
            r=HttpResponse(pdf_texto('Reporte de la plataforma',[f'Generado: {generado}',f'Filtros: {filtros}',
                *[f'{f["indicador"]}: {f["valor"]}' for f in filas]]),content_type='application/pdf')
        else: raise NotFound('Formato no disponible; utiliza PDF o CSV.')
        r['Content-Disposition']=f'attachment; filename="reporte-{tipo}.{formato}"'
        r['Cache-Control']='private, no-store'
        return r
