"""API de los módulos de participación. Los campos editables son explícitos por recurso."""
from collections.abc import Mapping
from itertools import islice
from django.db import transaction, models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from apps.usuarios.models import Socio, Usuario, HistorialEstado
from apps.usuarios.permissions import permisos_de
from apps.usuarios.repositories import RolRepository
from apps.usuarios.serializers.gestion_serializers import EstrictoSerializer
from . import models as m
from . import negocio as n


class ReferirSerializer(EstrictoSerializer):
    codigo = serializers.CharField(max_length=16)
    cedula = serializers.RegexField(r'^[0-9]{10}$')
    nombre = serializers.CharField(max_length=150)
    correo = serializers.EmailField(required=False, allow_blank=True)
    telefono = serializers.RegexField(r'^[0-9+]{7,15}$', required=False, allow_blank=True)
    producto = serializers.CharField(max_length=150)
    campana = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    acepta_terminos = serializers.BooleanField()


class EstadoSerializer(EstrictoSerializer):
    estado = serializers.CharField(max_length=20)
    motivo = serializers.CharField(max_length=1000)
    tipo_evento = serializers.ChoiceField(choices=['APERTURA_CUENTA', 'PRODUCTO_CREDITICIO','TARJETA_ENTREGADA','SEGURO_CONTRATADO'], required=False)
    monto_captado = serializers.DecimalField(max_digits=18,decimal_places=2,min_value=0,required=False,allow_null=True)


def validar(clase, datos):
    s = clase(data=datos)
    s.is_valid(raise_exception=True)
    return s.validated_data


def banco_valido(preguntas):
    if not isinstance(preguntas, list) or not 1 <= len(preguntas) <= 100:
        raise ValidationError({'preguntas': 'Registra de 1 a 100 preguntas.'})
    for p in preguntas:
        if not isinstance(p, dict) or set(p) != {'enunciado', 'opciones', 'correcta'}:
            raise ValidationError({'preguntas': 'Cada pregunta necesita enunciado, opciones y correcta.'})
        if not isinstance(p['enunciado'], str) or not p['enunciado'].strip() or len(p['enunciado']) > 2000:
            raise ValidationError({'preguntas': 'El enunciado es obligatorio y admite hasta 2000 caracteres.'})
        if not isinstance(p['opciones'], list) or not 2 <= len(p['opciones']) <= 20 or any(
                not isinstance(o, str) or not o.strip() or len(o) > 500 for o in p['opciones']):
            raise ValidationError({'preguntas': 'Registra de 2 a 20 opciones de texto por pregunta.'})
        if type(p['correcta']) is not int or p['correcta'] not in range(len(p['opciones'])):
            raise ValidationError({'preguntas': 'La respuesta correcta es un índice de las opciones, empezando por 0.'})
    return preguntas


# recurso: entidad, módulo de permisos, roles gestores, campos editables, estados de catálogo.
RECURSOS = {
 'gastos': (m.GastoCampana, 'campanas', [n.ADMIN,n.MARKETING], ['campana','fecha','concepto','importe'], False),
 'campanas': (m.Campana, 'campanas', [n.ADMIN,n.MARKETING,n.RSE],
   ['nombre','tipo','objetivo','meta','incentivos','condiciones','inicio','fin','segmentacion'], None),
 'niveles': (m.Nivel, 'gamificacion', [n.ADMIN], ['nombre','umbral_puntos'], None),
 'insignias': (m.Insignia, 'gamificacion', [n.ADMIN], ['nombre','criterio','umbral','icono'], None),
 'capacitaciones': (m.Capacitacion, 'formacion', [n.ADMIN,n.RSE,n.GESTOR],
   ['titulo','modalidad','descripcion','duracion','requisitos'], {'estado':'PUBLICADA'}),
 'modulos': (m.ModuloCapacitacion, 'formacion', [n.ADMIN,n.RSE,n.GESTOR], ['capacitacion','orden','titulo'], False),
 'evaluaciones': (m.Evaluacion, 'formacion', [n.ADMIN,n.RSE,n.GESTOR], ['capacitacion','nota_minima','max_intentos','preguntas'], False),
 'talleres': (m.Taller, 'formacion', [n.ADMIN,n.RSE,n.GESTOR], ['titulo','fecha','cupo','modalidad','lugar','duracion'], {'estado':'PROGRAMADO'}),
 'convenios': (m.Convenio, 'bienestar', [n.ADMIN,n.RSE,n.GESTOR], ['entidad','tipo','descripcion','beneficio','condiciones','vigencia'], None),
 'beneficios': (m.Beneficio, 'recompensas', [n.ADMIN,n.MARKETING],
   ['nombre','descripcion','costo_puntos','stock','condiciones','desde','hasta','activo','convenio'], None),
 'sorteos': (m.Sorteo, 'sorteos', [n.ADMIN,n.MARKETING],
   ['campana','nombre','premio','fecha','condiciones','num_ganadores','num_suplentes','origen'], None),
 'juegos': (m.Juego, 'juegos', [n.ADMIN,n.GESTOR],
   ['nombre','tipo','max_intentos','instrucciones','preguntas','nota_minima'], {'estado':'ACTIVO'}),
 'retos': (m.Reto, 'juegos', [n.ADMIN,n.GESTOR,n.MARKETING], ['objetivo','meta','inicio','fin','actividad'], None),
 'plantillas': (m.PlantillaNotificacion, 'notificaciones', [n.ADMIN], ['evento','canal','titulo','cuerpo'], False),
}


def gestor(usuario, config):
    return puede_gestionar(usuario, config[1], config[2])


def puede_gestionar(usuario, modulo, roles):
    return (usuario.is_active and bool(set(RolRepository.nombres_de(usuario)) & set(roles))
            and permisos_de(usuario).filter(modulo=modulo, accion='gestionar').exists())


def configurar_serializer(config):
    modelo, _, _, campos, _ = config
    class RecursoSerializer(serializers.ModelSerializer):
        class Meta:
            model = modelo
            fields = campos

        def to_internal_value(self, data):
            extras = set(data)-set(campos)
            if extras: raise ValidationError({k: 'Campo no permitido.' for k in extras})
            return super().to_internal_value(data)

        def validate(self, datos):
            completos = {c: getattr(self.instance,c,None) for c in campos} if self.instance else {}
            completos.update(datos)
            for inicio, fin in [('inicio','fin'),('desde','hasta')]:
                if completos.get(inicio) and completos.get(fin) and completos[fin] < completos[inicio]:
                    raise ValidationError({fin: 'La fecha final no puede ser anterior al inicio.'})
            for campo in ['meta','duracion','cupo','max_intentos','num_ganadores','umbral','costo_puntos']:
                if completos.get(campo) is not None and completos[campo] < 1:
                    raise ValidationError({campo:'Debe ser mayor que cero.'})
            for campo in ['stock','num_suplentes','umbral_puntos']:
                if completos.get(campo) is not None and completos[campo] < 0:
                    raise ValidationError({campo:'No puede ser negativo.'})
            if completos.get('importe') is not None and completos['importe']<0:
                raise ValidationError({'importe':'No puede ser negativo.'})
            for campo in ['nota_minima']:
                if completos.get(campo) is not None and not 0 <= completos[campo] <= 100:
                    raise ValidationError({campo:'Debe estar entre 0 y 100.'})
            if 'preguntas' in datos: banco_valido(datos['preguntas'])
            if 'segmentacion' in datos:
                seg = datos['segmentacion']
                if not isinstance(seg,dict) or set(seg)-{'RANGO_EDAD','TIPO_SOCIO','PRODUCTO','AGENCIA'}:
                    raise ValidationError({'segmentacion':'Utiliza solamente los criterios autorizados.'})
                for k,v in seg.items():
                    if k=='RANGO_EDAD':
                        if not isinstance(v,list) or len(v)!=2 or any(type(x) is not int for x in v) or not 0<=v[0]<=v[1]<=120:
                            raise ValidationError({'segmentacion':'RANGO_EDAD necesita [edad mínima, edad máxima].'})
                    elif not isinstance(v,list) or not v or any(not isinstance(x,str) or not x.strip() for x in v):
                        raise ValidationError({'segmentacion':'Cada criterio necesita una lista de valores.'})
            if modelo is m.Juego and completos.get('tipo') not in ['TRIVIA','VERDADERO_FALSO','EMPAREJAR']:
                raise ValidationError({'tipo':'Selecciona TRIVIA, VERDADERO_FALSO o EMPAREJAR.'})
            if modelo in (m.Taller,m.Capacitacion) and completos.get('modalidad') not in ['PRESENCIAL','VIRTUAL','HIBRIDA']:
                raise ValidationError({'modalidad':'Selecciona PRESENCIAL, VIRTUAL o HIBRIDA.'})
            if modelo is m.Sorteo and completos.get('origen') not in ['CONVERSION','CAPACITACION','TALLER','JUEGO']:
                raise ValidationError({'origen':'Selecciona una actividad validada.'})
            if modelo is m.Reto and completos.get('actividad') not in ['CONVERSION','CAPACITACION','TALLER','JUEGO']:
                raise ValidationError({'actividad':'Selecciona una actividad validada.'})
            if modelo is m.Insignia and completos.get('criterio') not in ['PUNTOS','CONVERSION','CAPACITACION','TALLER','JUEGO','RETO']:
                raise ValidationError({'criterio':'Criterio no reconocido.'})
            if modelo is m.PlantillaNotificacion:
                from .notificaciones import EVENTOS
                if completos.get('evento') not in EVENTOS or completos.get('canal') not in ['TODOS','INTERNA','CORREO']:
                    raise ValidationError('Selecciona evento y canal válidos.')
            return datos
    return RecursoSerializer


def datos_objeto(objeto, gestion=False):
    datos = {'id': objeto.pk}
    for campo in objeto._meta.concrete_fields:
        if campo.primary_key: continue
        if campo.name in ('creado_por','evidencia'): continue
        valor = getattr(objeto,campo.attname)
        if campo.name == 'preguntas' and not gestion:
            valor = [{'enunciado':p['enunciado'],'opciones':p['opciones']} for p in valor]
        datos[campo.name] = valor
    if isinstance(objeto,m.Campana):
        q = m.Referido.objects.filter(campana=objeto)
        total = q.count()
        conversiones_q = m.Conversion.objects.filter(referido__campana=objeto)
        conversiones = q.filter(estado='CONVERTIDO').count()
        socios_ref = set(q.exclude(estado__in=['REGISTRADO','EXPIRADO']).values_list('codigo__socio_id',flat=True))
        socios_sorteo = set(m.ParticipacionSorteo.objects.filter(sorteo__campana=objeto).values_list('socio_id',flat=True))
        ids_conversion = list(conversiones_q.values_list('pk',flat=True))
        puntos_otorgados = (m.MovimientoPuntos.objects.filter(
            tipo='ACREDITACION',origen_tipo='CONVERSION',origen_id__in=ids_conversion
        ).aggregate(total=models.Sum('cantidad'))['total'] or 0) if ids_conversion else 0
        datos['indicadores'] = {'participantes':len(socios_ref | socios_sorteo),
            'referidos':total,'conversiones':conversiones,
            'tasa_conversion':round(100*conversiones/total,2) if total else 0,
            'puntos_otorgados':puntos_otorgados,
            'avance_meta':round(100*conversiones/objeto.meta,2) if objeto.meta else 0}
    if isinstance(objeto,m.Sorteo):
        datos['ganadores'] = []
        if objeto.estado == 'EJECUTADO':
            datos['ganadores'] = [{'alias':g.participacion.socio.alias or 'Socio',
                 'posicion':g.posicion,'suplente':g.es_suplente}
                 for g in m.Ganador.objects.filter(sorteo=objeto).select_related('participacion__socio').order_by('posicion')]
        if gestion: datos['evidencia'] = objeto.evidencia
    return datos


def campos_formulario(config):
    resultado=[]
    for nombre,campo in configurar_serializer(config)().fields.items():
        tipo = ('boolean' if isinstance(campo,serializers.BooleanField) else 'json' if isinstance(campo,serializers.JSONField)
            else 'datetime-local' if isinstance(campo,serializers.DateTimeField) else 'date' if isinstance(campo,serializers.DateField)
            else 'number' if isinstance(campo,(serializers.IntegerField,serializers.DecimalField,serializers.PrimaryKeyRelatedField))
            else 'textarea' if nombre in ['descripcion','instrucciones','condiciones','requisitos','objetivo','incentivos'] else 'text')
        item={'nombre':nombre,'tipo':tipo,'requerido':campo.required,'nulo':campo.allow_null}
        if isinstance(campo,serializers.DecimalField): item['decimal']=True
        opciones={'modalidad':['PRESENCIAL','VIRTUAL','HIBRIDA'],
                  'origen':['CONVERSION','CAPACITACION','TALLER','JUEGO'],
                  'actividad':['CONVERSION','CAPACITACION','TALLER','JUEGO'],
                  'criterio':['PUNTOS','CONVERSION','CAPACITACION','TALLER','JUEGO','RETO']}
        if config[0] is m.Juego: opciones['tipo']=['TRIVIA','VERDADERO_FALSO','EMPAREJAR']
        if config[0] is m.PlantillaNotificacion:
            from .notificaciones import EVENTOS
            opciones['evento']=list(EVENTOS);opciones['canal']=['TODOS','INTERNA','CORREO']
        if nombre in opciones: item['opciones']=[{'valor':v,'etiqueta':v.replace('_',' ').capitalize()} for v in opciones[nombre]]
        if isinstance(campo,serializers.PrimaryKeyRelatedField):
            item['opciones']=[{'valor':v.pk,'etiqueta':getattr(v,'titulo',getattr(v,'nombre',getattr(v,'entidad',str(v.pk))))}
                              for v in campo.queryset.order_by('-pk')[:200]]
        resultado.append(item)
    return resultado


class CatalogoView(APIView):
    def get(self,request,recurso):
        if recurso not in RECURSOS: raise NotFound()
        config=RECURSOS[recurso]
        gestion=gestor(request.user,config)
        socio=None if gestion else n.socio_de(request.user,config[1])
        if config[4] is False and not gestion: raise PermissionDenied()
        q=config[0].objects.order_by('-pk')
        if not gestion:
            if config[4]: q=q.filter(**config[4])
            hoy=timezone.localdate()
            if recurso=='beneficios':
                q=q.filter(activo=True,desde__lte=hoy).filter(models.Q(hasta__isnull=True)|models.Q(hasta__gte=hoy)).filter(
                    models.Q(stock__isnull=True)|models.Q(stock__gt=0)).filter(models.Q(convenio__isnull=True)|models.Q(convenio__vigencia__isnull=True)|models.Q(convenio__vigencia__gte=hoy))
            if recurso=='convenios': q=q.filter(models.Q(vigencia__isnull=True)|models.Q(vigencia__gte=hoy))
            if recurso=='retos': q=q.filter(inicio__lte=hoy,fin__gte=hoy)
            if recurso=='sorteos': q=q.exclude(estado='BORRADOR')
        if recurso == 'campanas' and socio:
            candidatas = q.filter(estado='ACTIVA', inicio__lte=hoy, fin__gte=hoy).iterator()
            filas = list(islice((c for c in candidatas if n.campana_visible(c, socio)), 200))
        else:
            filas = list(q[:200])
        resultados = [datos_objeto(o,gestion) for o in filas]
        if socio and recurso == 'juegos':
            usados = dict(m.Partida.objects.filter(socio=socio, juego__in=filas).values('juego_id')
                          .annotate(total=models.Count('pk')).values_list('juego_id','total'))
            for dato, juego in zip(resultados, filas):
                dato['intentos_restantes'] = max(0, juego.max_intentos - usados.get(juego.pk, 0))
        if socio and recurso == 'retos':
            avances = {p.reto_id:p for p in m.ProgresoReto.objects.filter(socio=socio, reto__in=filas)}
            for dato in resultados:
                progreso = avances.get(dato['id'])
                dato['avance'] = progreso.avance if progreso else 0
                dato['completado'] = bool(progreso and progreso.completado_en)
        if recurso == 'beneficios':
            convenios = dict(m.Convenio.objects.filter(pk__in=[b.convenio_id for b in filas if b.convenio_id])
                             .values_list('pk','entidad'))
            for dato in resultados:
                dato['entidad_convenio'] = convenios.get(dato['convenio'])
        return Response({'resultados':resultados, 'puede_gestionar':gestion,
                         'campos':campos_formulario(config) if gestion else []})

    @transaction.atomic
    def post(self,request,recurso):
        config=RECURSOS.get(recurso)
        if not config: raise NotFound()
        n.exigir(request.user,config[1],config[2])
        s=configurar_serializer(config)(data=request.data)
        s.is_valid(raise_exception=True)
        extra={}
        if recurso=='campanas': extra={'creado_por':request.user,'estado':'BORRADOR'}
        if recurso=='capacitaciones': extra={'estado':'BORRADOR'}
        if recurso in ('modulos','evaluaciones'):
            curso=m.Capacitacion.objects.select_for_update().get(pk=s.validated_data['capacitacion'].pk)
            if m.Inscripcion.objects.filter(capacitacion=curso).exists():
                raise ValidationError('Conserva el contenido de las capacitaciones con participantes; crea una nueva versión.')
            if recurso=='evaluaciones' and m.Evaluacion.objects.filter(capacitacion=curso).exists():
                raise ValidationError('Esta capacitación ya tiene una evaluación; edita la existente.')
        obj=s.save(**extra)
        n.auditar(request.user,obj,'CREAR_'+recurso.upper())
        return Response(datos_objeto(obj,True),status=201)


class RecursoDetalleView(APIView):
    @transaction.atomic
    def put(self,request,recurso,pk):
        config=RECURSOS.get(recurso)
        if not config: raise NotFound()
        n.exigir(request.user,config[1],config[2])
        obj=get_object_or_404(config[0].objects.select_for_update(),pk=pk)
        if recurso=='campanas' and obj.estado!='BORRADOR':
            if set(request.data)-{'nombre','objetivo','condiciones'}:
                raise ValidationError('Tras activar, solamente puedes editar nombre, objetivo y condiciones informativas.')
        if recurso=='sorteos' and obj.estado!='BORRADOR': raise ValidationError('Solo puedes editar sorteos en borrador.')
        if recurso=='juegos' and m.Partida.objects.filter(juego=obj).exists(): raise ValidationError('Crea otro juego para conservar los intentos y resultados existentes.')
        if recurso in ('evaluaciones','modulos') and m.Inscripcion.objects.filter(capacitacion=obj.capacitacion).exists():
            raise ValidationError('Conserva el contenido de las capacitaciones con participantes; crea una nueva versión.')
        s=configurar_serializer(config)(obj,data=request.data,partial=True)
        s.is_valid(raise_exception=True)
        campos_editados = sorted(s.validated_data)
        estado_actual = getattr(obj,'estado','')
        obj=s.save()
        if recurso=='campanas' and campos_editados:
            n.historial(request.user,obj,estado_actual,obj.estado,f"Modificación de campaña: {', '.join(campos_editados)}")
        n.auditar(request.user,obj,'EDITAR_'+recurso.upper(),campos=campos_editados)
        return Response(datos_objeto(obj,True))


class AccionView(APIView):
    @transaction.atomic
    def post(self,request,recurso,pk,accion):
        u=request.user
        d=request.data
        if recurso=='referidos' and accion=='estado':
            x=validar(EstadoSerializer,d)
            r=n.cambiar_referido(u,pk,x['estado'],x['motivo'],x.get('tipo_evento'),x.get('monto_captado'))
            return Response({'id':r.pk,'estado':r.estado})
        if recurso=='beneficios' and accion=='canjear':
            class Datos(EstrictoSerializer):
                clave=serializers.UUIDField()
                acepta_condiciones=serializers.BooleanField()
            x=validar(Datos,d)
            if not x['acepta_condiciones']: raise ValidationError('Acepta las condiciones del beneficio.')
            r=n.solicitar_canje(u,pk,x['clave'])
            return Response({'id':r.pk,'estado':r.estado,'puntos':r.puntos},status=201)
        if recurso=='canjes' and accion=='estado':
            x=validar(EstadoSerializer,d)
            r=n.resolver_canje(u,pk,x['estado'],x['motivo'])
            return Response({'id':r.pk,'estado':r.estado})
        if recurso=='capacitaciones' and accion=='inscribir':
            class Datos(EstrictoSerializer): acepta_requisitos=serializers.BooleanField(default=False)
            x=validar(Datos,d)
            r=n.inscribir(u,pk,x['acepta_requisitos'])
            return Response({'id':r.pk,'estado':r.estado},status=201)
        if recurso=='capacitaciones' and accion=='progreso':
            class Datos(EstrictoSerializer): unidad=serializers.IntegerField(min_value=1)
            x=validar(Datos,d)
            socio=n.socio_de(u,'formacion')
            i=get_object_or_404(m.Inscripcion.objects.select_for_update(),socio=socio,capacitacion_id=pk,capacitacion__estado='PUBLICADA')
            unidad=get_object_or_404(m.ModuloCapacitacion,pk=x['unidad'],capacitacion_id=pk)
            m.Progreso.objects.update_or_create(inscripcion=i,unidad=unidad,defaults={'porcentaje':100})
            return Response({'mensaje':'Módulo completado.'})
        if recurso=='capacitaciones' and accion=='evaluar':
            class Datos(EstrictoSerializer): respuestas=serializers.ListField(child=serializers.IntegerField(min_value=0),max_length=100)
            x=validar(Datos,d)
            r=n.evaluar(u,pk,x['respuestas'])
            return Response({'nota':r.nota,'aprobado':r.aprobado})
        if recurso=='talleres' and accion=='inscribir':
            r=n.inscribir_taller(u,pk)
            return Response({'id':r.pk,'asistio':r.asistio},status=201)
        if recurso=='asistencias' and accion=='confirmar':
            r=n.asistencia(u,pk)
            return Response({'id':r.pk,'asistio':r.asistio})
        if recurso=='juegos' and accion=='iniciar':
            r=n.iniciar_partida(u,pk)
            return Response({'id':r.pk,'tipo':r.juego.tipo,'preguntas':[{'enunciado':p['enunciado'],'opciones':p['opciones']} for p in r.juego.preguntas]},status=201)
        if recurso=='partidas' and accion=='finalizar':
            class Datos(EstrictoSerializer): respuestas=serializers.ListField(child=serializers.IntegerField(min_value=0),max_length=100)
            x=validar(Datos,d)
            r=n.finalizar_partida(u,pk,x['respuestas'])
            return Response({'id':r.pk,'puntuacion':r.puntuacion})
        if recurso=='sorteos' and accion=='ejecutar':
            return Response(datos_objeto(n.ejecutar_sorteo(u,pk),True))
        if recurso=='movimientos' and accion=='revertir':
            class Datos(EstrictoSerializer): motivo=serializers.CharField(max_length=1000)
            r=n.revertir(u,pk,validar(Datos,d)['motivo'])
            return Response({'id':r.pk})
        if recurso=='campanas' and accion=='previsualizar':
            n.exigir(u,'campanas',RECURSOS['campanas'][2])
            c=get_object_or_404(m.Campana,pk=pk)
            c.estado='ACTIVA'
            cantidad=sum(n.campana_visible(c,s) for s in Socio.objects.filter(validado_en__isnull=False,usuario__estado='ACTIVA').select_related('usuario'))
            return Response({'socios_elegibles':cantidad})
        if recurso in RECURSOS and accion=='estado':
            config=RECURSOS[recurso]
            n.exigir(u,config[1],config[2])
            x=validar(EstadoSerializer,d)
            obj=get_object_or_404(config[0].objects.select_for_update(),pk=pk)
            transiciones={
                'campanas':{'BORRADOR':['ACTIVA'],'ACTIVA':['SUSPENDIDA','FINALIZADA'],'SUSPENDIDA':['ACTIVA','FINALIZADA']},
                'capacitaciones':{'BORRADOR':['PUBLICADA'],'PUBLICADA':['RETIRADA'],'RETIRADA':['PUBLICADA']},
                'talleres':{'PROGRAMADO':['REALIZADO','CANCELADO']},
                'juegos':{'INACTIVO':['ACTIVO'],'ACTIVO':['INACTIVO']},
                'sorteos':{'BORRADOR':['ACTIVO'],'ACTIVO':['CANCELADO']}}
            anterior=obj.estado if hasattr(obj,'estado') else ''
            if x['estado'] not in transiciones.get(recurso,{}).get(anterior,[]): raise ValidationError('Transición no permitida.')
            if recurso=='capacitaciones' and x['estado']=='PUBLICADA':
                if not m.ModuloCapacitacion.objects.filter(capacitacion=obj).exists() or not m.Evaluacion.objects.filter(capacitacion=obj).exists():
                    raise ValidationError('Configura módulos y evaluación antes de publicar.')
            if recurso=='juegos' and x['estado']=='ACTIVO': banco_valido(obj.preguntas)
            if recurso=='campanas' and x['estado']=='ACTIVA' and obj.fin<timezone.localdate(): raise ValidationError('La campaña ya venció.')
            obj.estado=x['estado'];obj.save(update_fields=['estado'])
            n.historial(u,obj,anterior,obj.estado,x['motivo'])
            n.auditar(u,obj,'CAMBIAR_ESTADO',estado=obj.estado,motivo=x['motivo'])
            return Response(datos_objeto(obj,True))
        raise NotFound('Operación no disponible.')


def datos_referido(r,gestion):
    p=r.prospecto
    datos_completos = gestion and p.consentimiento_en is not None
    contacto = '••••' if not p.consentimiento_en else p.contacto
    if p.consentimiento_en and not datos_completos:
        contacto = '••••' + p.contacto[-2:]
    return {'id':r.pk,'nombre':p.nombre if datos_completos else p.nombre[:1]+'•••','contacto':contacto,
            'producto':p.producto,'estado':r.estado,'campana':r.campana_id,'socio':r.codigo.socio_id,'creado_en':r.creado_en}


class ReferidosView(APIView):
    def get(self,request):
        gestion = puede_gestionar(request.user, 'referidos', [n.ADMIN, n.MARKETING])
        q=m.Referido.objects.select_related('prospecto','codigo__socio').order_by('-pk')
        if not gestion: q=q.filter(codigo__socio=n.socio_de(request.user,'referidos'))
        for campo in ['estado','campana','codigo__socio']:
            clave='socio' if campo=='codigo__socio' else campo
            if request.query_params.get(clave):
                valor=request.query_params[clave]
                if campo!='estado': valor=serializers.IntegerField(min_value=1).run_validation(valor)
                else: valor=serializers.ChoiceField(choices=['REGISTRADO','CONFIRMADO','EN_SEGUIMIENTO','CONVERTIDO','RECHAZADO','EXPIRADO']).run_validation(valor)
                q=q.filter(**{campo:valor})
        q=filtrar_periodo(q,request,'creado_en')
        return Response({'resultados':[datos_referido(r,gestion) for r in q[:200]],'puede_gestionar':gestion})

    def post(self,request):
        r=n.registrar_referido(validar(ReferirSerializer,request.data),request.user)
        return Response({'id':r.pk,'mensaje':'Solicitud registrada. El prospecto debe confirmar su consentimiento.'},status=201)


class ReferidoPublicoView(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[]
    throttle_classes=[AnonRateThrottle]
    def post(self,request,codigo):
        if not isinstance(request.data, Mapping):
            raise ValidationError('Envía los datos de la referencia como un formulario u objeto.')
        datos = request.data.copy()
        datos['codigo']=codigo
        n.registrar_referido(validar(ReferirSerializer,datos))
        return Response({'mensaje':'Solicitud registrada. Revisa el medio de confirmación de contacto.'},status=201)


class ConfirmarReferidoView(ReferidoPublicoView):
    def post(self,request,token):
        n.confirmar_referido(token)
        return Response({'mensaje':'Consentimiento confirmado. La cooperativa podrá dar seguimiento a tu solicitud.'})


class PuntosView(APIView):
    def get(self,request):
        s=n.socio_de(request.user,'gamificacion')
        total=n.puntos_logro(s)
        nivel=m.Nivel.objects.filter(umbral_puntos__lte=total).order_by('-umbral_puntos').first()
        return Response({'saldo':n.saldo(s),'puntos_logro':total,'nivel':nivel.nombre if nivel else 'Inicial',
            'insignias':[{'nombre':i.insignia.nombre,'icono':i.insignia.icono} for i in m.SocioInsignia.objects.filter(socio=s).select_related('insignia')],
            'movimientos':[{'id':p.pk,'tipo':p.tipo,'cantidad':p.cantidad,'origen_tipo':p.origen_tipo,'origen_id':p.origen_id,
                          'fecha':p.creado_en,'motivo':p.motivo} for p in m.MovimientoPuntos.objects.filter(socio=s).order_by('-pk')[:200]]})


class MisActividadesView(APIView):
    def get(self,request):
        s=n.socio_de(request.user,'formacion')
        return Response({'inscripciones':[{'id':i.pk,'capacitacion':i.capacitacion_id,'titulo':i.capacitacion.titulo,'estado':i.estado}
            for i in m.Inscripcion.objects.filter(socio=s).select_related('capacitacion')],
            'certificados':[{'id':c.pk,'titulo':c.inscripcion.capacitacion.titulo,'codigo':c.codigo_verificacion,'fecha':c.emitido_en}
                for c in m.Certificado.objects.filter(inscripcion__socio=s).select_related('inscripcion__capacitacion')],
            'talleres':[{'id':a.pk,'titulo':a.taller.titulo,'asistio':a.asistio} for a in m.AsistenciaTaller.objects.filter(socio=s).select_related('taller')],
            'partidas':[{'id':p.pk,'juego':p.juego.nombre,'puntuacion':p.puntuacion,'fecha':p.finalizada_en}
                        for p in m.Partida.objects.filter(socio=s).select_related('juego').order_by('-pk')[:100]],
            'retos':[{'id':p.pk,'objetivo':p.reto.objetivo,'avance':p.avance,'meta':p.reto.meta,'completado_en':p.completado_en}
                for p in m.ProgresoReto.objects.filter(socio=s).select_related('reto')]})


class AulaView(APIView):
    def get(self,request,pk):
        s=n.socio_de(request.user,'formacion')
        i=get_object_or_404(m.Inscripcion,socio=s,capacitacion_id=pk,capacitacion__estado='PUBLICADA')
        e=get_object_or_404(m.Evaluacion,capacitacion_id=pk)
        completos=set(m.Progreso.objects.filter(inscripcion=i,porcentaje=100).values_list('unidad_id',flat=True))
        unidades = list(m.ModuloCapacitacion.objects.filter(capacitacion_id=pk).order_by('orden'))
        terminadas = sum(u.pk in completos for u in unidades)
        porcentaje_avance = 100 * terminadas // len(unidades) if unidades else 0
        return Response({'inscripcion':i.pk,'estado':i.estado,'titulo':i.capacitacion.titulo,
            'porcentaje_avance':porcentaje_avance,
            'modulos':[{'id':u.pk,'titulo':u.titulo,'completado':u.pk in completos,
                'materiales':[{'id':a.pk,'titulo':a.titulo} for a in u.materialeducativo_set.all()]}
                for u in unidades],
            'preguntas':[{'enunciado':p['enunciado'],'opciones':p['opciones']} for p in e.preguntas],
            'nota_minima':e.nota_minima,'intentos_restantes':max(0,e.max_intentos-m.IntentoEvaluacion.objects.filter(inscripcion=i).count())})


class CanjesView(APIView):
    def get(self,request):
        gestion=gestor(request.user,RECURSOS['beneficios'])
        if gestion: n.exigir(request.user,'recompensas',[n.ADMIN])
        q=m.Canje.objects.select_related('beneficio').order_by('-pk')
        if not gestion: q=q.filter(socio=n.socio_de(request.user,'recompensas'))
        if request.query_params.get('estado'): q=q.filter(estado=request.query_params['estado'])
        return Response({'resultados':[{'id':c.pk,'beneficio':c.beneficio.nombre,'socio':c.socio_id,'puntos':c.puntos,
            'estado':c.estado,'fecha':c.creado_en,'entrega':c.fecha_entrega} for c in q[:200]],'puede_gestionar':gestion})


class ParticipantesView(APIView):
    def get(self,request,recurso,pk):
        n.exigir(request.user,'formacion',[n.ADMIN,n.RSE,n.GESTOR])
        if recurso=='talleres':
            return Response({'resultados':[{'id':a.pk,'socio':a.socio_id,'nombre':a.socio.usuario.nombre,'asistio':a.asistio}
                for a in m.AsistenciaTaller.objects.filter(taller_id=pk).select_related('socio__usuario')]})
        if recurso=='capacitaciones':
            curso = get_object_or_404(m.Capacitacion, pk=pk)
            total = m.ModuloCapacitacion.objects.filter(capacitacion=curso).count()
            inscripciones = m.Inscripcion.objects.filter(capacitacion=curso).select_related('socio__usuario')
            inscripciones = inscripciones.annotate(
                modulos_completados=models.Count('progreso',filter=models.Q(progreso__porcentaje=100),distinct=True),
                nota_maxima=models.Max('intentoevaluacion__nota'),
                intentos=models.Count('intentoevaluacion',distinct=True),
            )
            return Response({'resultados':[
                {'id':i.pk,'socio':i.socio_id,'nombre':i.socio.usuario.nombre,'estado':i.estado,
                 'modulos_completados':i.modulos_completados,
                 'porcentaje_avance':100*i.modulos_completados//total if total else 0,
                 'intentos':i.intentos,'nota_maxima':i.nota_maxima}
                for i in inscripciones
            ]})
        raise NotFound()


def filtrar_periodo(q,request,campo):
    for parametro,operador in [('desde','gte'),('hasta','lte')]:
        if request.query_params.get(parametro):
            fecha=serializers.DateField().run_validation(request.query_params[parametro])
            sufijo='__date' if isinstance(q.model._meta.get_field(campo),models.DateTimeField) else ''
            q=q.filter(**{f'{campo}{sufijo}__{operador}':fecha})
    return q
