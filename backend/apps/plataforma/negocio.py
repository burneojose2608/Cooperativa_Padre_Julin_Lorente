"""Reglas transaccionales de referidos, incentivos y participación."""
from datetime import timedelta
from decimal import Decimal
import hashlib
import hmac
import json
import secrets

from django.conf import settings
from django.db import IntegrityError, models, transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.usuarios.models import Socio, Usuario, PadronPrueba, HistorialEstado
from apps.usuarios.permissions import permisos_de
from apps.usuarios.repositories import AuditoriaRepository, RolRepository
from .models import (CodigoReferido, ReglaPuntos, Campana, Prospecto, SolicitudContacto, Referido, Conversion,
    MovimientoPuntos, ActividadValidada, Nivel, Insignia, SocioInsignia, Inscripcion, Progreso, Evaluacion, IntentoEvaluacion,
    Certificado, Taller, AsistenciaTaller, Beneficio, Canje, Sorteo, ParticipacionSorteo, Ganador,
    Juego, Partida, Reto, ProgresoReto, SuspensionComunidad)
from .notificaciones import notificar

ADMIN = 'Administrador'
MARKETING = 'Responsable de Marketing'
RSE = 'Responsable de Responsabilidad Social'
GESTOR = 'Gestor de contenidos'


def exigir(usuario, modulo, roles, accion='gestionar'):
    if not usuario.is_active or not set(RolRepository.nombres_de(usuario)) & set(roles):
        raise PermissionDenied('Tu rol no permite esta operación.')
    if not permisos_de(usuario).filter(modulo=modulo, accion=accion).exists():
        raise PermissionDenied('El permiso para esta operación está deshabilitado.')


def socio_de(usuario, modulo):
    exigir(usuario, modulo, ['Socio'], 'participar')
    return socio_validado(usuario)


def socio_validado(usuario):
    socio = Socio.objects.filter(usuario=usuario, validado_en__isnull=False).first()
    if socio is None:
        raise PermissionDenied('Tu cuenta aún no está validada como socio. Consulta con la cooperativa.')
    return socio


def auditar(usuario, objeto, accion, **detalle):
    AuditoriaRepository.registrar(usuario=usuario, entidad=objeto._meta.db_table, registro_id=objeto.pk,
                                  accion=accion, resultado='EXITO', detalle=detalle)


def historial(usuario, objeto, anterior, nuevo, motivo):
    HistorialEstado.objects.create(usuario=usuario, entidad=objeto._meta.db_table, registro_id=objeto.pk,
                                   estado_anterior=anterior, estado_nuevo=nuevo, motivo=motivo)


def saldo(socio):
    valores = MovimientoPuntos.objects.filter(socio=socio).values('tipo').annotate(total=models.Sum('cantidad'))
    return sum(v['total'] * (1 if v['tipo'] in ('ACREDITACION', 'LIBERACION') else -1) for v in valores)


def puntos_logro(socio):
    valores = MovimientoPuntos.objects.filter(socio=socio, tipo__in=['ACREDITACION', 'REVERSO']).values('tipo').annotate(total=models.Sum('cantidad'))
    return sum(v['total'] * (1 if v['tipo']=='ACREDITACION' else -1) for v in valores)


def actualizar_logros(socio, anterior):
    total = puntos_logro(socio)
    nivel = Nivel.objects.filter(umbral_puntos__lte=total).order_by('-umbral_puntos').first()
    previo = Nivel.objects.filter(umbral_puntos__lte=anterior).order_by('-umbral_puntos').first()
    if nivel and (not previo or nivel.pk != previo.pk):
        notificar(socio.usuario, 'LOGRO', f'Has alcanzado el nivel {nivel.nombre}.', clave_evento=f'nivel:{socio.pk}:{nivel.pk}')
    for insignia in Insignia.objects.all():
        if insignia.criterio == 'PUNTOS':
            valor = total
        else:
            valor = MovimientoPuntos.objects.filter(socio=socio, tipo='ACREDITACION', origen_tipo=insignia.criterio).count()
        if valor >= insignia.umbral:
            _, nueva = SocioInsignia.objects.get_or_create(socio=socio, insignia=insignia)
            if nueva:
                notificar(socio.usuario, 'LOGRO', f'Obtuviste la insignia {insignia.nombre}.',
                          clave_evento=f'insignia:{socio.pk}:{insignia.pk}')


ACTIVIDADES = {'CONVERSION': 'CONVERSION_REFERIDO', 'CAPACITACION': 'CAPACITACION_APROBADA',
               'TALLER': 'ASISTENCIA_TALLER', 'JUEGO': 'JUEGO', 'RETO': 'RETO'}


@transaction.atomic
def acreditar(socio, origen, origen_id):
    """Sólo lo invocan actividades verificadas por los servicios del servidor."""
    socio = Socio.objects.select_for_update().select_related('usuario').get(pk=socio.pk)
    previo = MovimientoPuntos.objects.filter(origen_tipo=origen, origen_id=origen_id, tipo='ACREDITACION').first()
    if previo:
        if previo.socio_id != socio.pk:
            raise ValidationError('La actividad ya pertenece a otro participante.')
        return previo
    actividad, nueva = ActividadValidada.objects.get_or_create(origen_tipo=origen, origen_id=origen_id, defaults={'socio':socio})
    if not nueva:
        if actividad.socio_id != socio.pk: raise ValidationError('La actividad pertenece a otro participante.')
        return None
    regla = ReglaPuntos.vigente_para(ACTIVIDADES[origen], timezone.localdate())
    if not regla:
        raise ValidationError('El administrador debe configurar una regla de puntos vigente para esta actividad.')
    hoy = timezone.localdate()
    inicio = hoy if regla.periodo == 'DIA' else hoy.replace(day=1) if regla.periodo == 'MES' else hoy.replace(month=1, day=1)
    usados = MovimientoPuntos.objects.filter(socio=socio, tipo='ACREDITACION', regla__tipo_actividad=regla.tipo_actividad,
                                            creado_en__date__gte=inicio).count()
    movimiento = None
    if usados < regla.limite_periodo:
        anterior = puntos_logro(socio)
        movimiento = MovimientoPuntos.objects.create(socio=socio, regla=regla, tipo='ACREDITACION', cantidad=regla.puntos,
                                                 origen_tipo=origen, origen_id=origen_id)
        notificar(socio.usuario, 'PUNTOS', f'Recibiste {regla.puntos} puntos por {origen.lower()}.', clave_evento=f'puntos:{movimiento.pk}')
        actualizar_logros(socio, anterior)
    for sorteo in Sorteo.objects.select_for_update().filter(estado='ACTIVO', origen=origen, fecha__gte=timezone.now()):
        if sorteo.campana.estado == 'ACTIVA' and campana_visible(sorteo.campana, socio):
            if origen == 'CONVERSION' and Conversion.objects.get(pk=origen_id).referido.campana_id != sorteo.campana_id:
                continue
            ParticipacionSorteo.objects.get_or_create(sorteo=sorteo, origen_tipo=origen, origen_id=origen_id, defaults={'socio': socio})
    if origen != 'RETO':
        for reto in Reto.objects.filter(inicio__lte=hoy, fin__gte=hoy, actividad=origen):
            progreso, _ = ProgresoReto.objects.get_or_create(reto=reto, socio=socio)
            if progreso.completado_en:
                continue
            progreso.avance = ActividadValidada.objects.filter(socio=socio, origen_tipo=origen,
                                                               validada_en__date__gte=reto.inicio, validada_en__date__lte=reto.fin).count()
            if progreso.avance >= reto.meta:
                progreso.completado_en = timezone.now()
                acreditar(socio, 'RETO', progreso.pk)
            progreso.save()
    return movimiento


@transaction.atomic
def revertir(usuario, id_movimiento, motivo):
    exigir(usuario, 'gamificacion', [ADMIN])
    original = get_object_or_404(MovimientoPuntos, pk=id_movimiento, tipo='ACREDITACION')
    socio = Socio.objects.select_for_update().get(pk=original.socio_id)
    if not motivo.strip():
        raise ValidationError('Indica la justificación del reverso.')
    if MovimientoPuntos.objects.filter(origen_tipo=original.origen_tipo, origen_id=original.origen_id, tipo='REVERSO').exists():
        raise ValidationError('La actividad ya fue revertida.')
    if saldo(socio) < original.cantidad:
        raise ValidationError('El reverso dejaría un saldo negativo.')
    m = MovimientoPuntos.objects.create(socio=socio, tipo='REVERSO', cantidad=original.cantidad,
        origen_tipo=original.origen_tipo, origen_id=original.origen_id, motivo=motivo)
    auditar(usuario, m, 'REVERTIR_PUNTOS', motivo=motivo)
    return m


def campana_visible(campana, socio):
    hoy = timezone.localdate()
    if campana.estado != 'ACTIVA' or not campana.inicio <= hoy <= campana.fin:
        return False
    edad = hoy.year - socio.usuario.fecha_nacimiento.year - ((hoy.month, hoy.day) < (
        socio.usuario.fecha_nacimiento.month, socio.usuario.fecha_nacimiento.day))
    for criterio, valor in campana.segmentacion.items():
        if criterio == 'RANGO_EDAD':
            if not valor[0] <= edad <= valor[1]: return False
        elif socio.segmento.get(criterio) not in valor:
            return False
    return True


def huella(valor):
    return hmac.new(settings.SECRET_KEY.encode(), valor.strip().lower().encode(), hashlib.sha256).hexdigest()


@transaction.atomic
def registrar_referido(datos, usuario=None):
    codigo = get_object_or_404(CodigoReferido.objects.select_for_update().select_related('socio__usuario'), valor=datos['codigo'])
    if not codigo.es_valido(): raise ValidationError('No se puede registrar esta referencia.')
    if usuario is not None:
        socio = socio_de(usuario, 'referidos')
        if codigo.socio_id != socio.pk: raise PermissionDenied('Utiliza tu propio código de referido.')
    cedula = datos['cedula']
    if not datos['acepta_terminos']: raise ValidationError('Se requiere consentimiento para registrar los datos.')
    u = codigo.socio.usuario
    if cedula == u.cedula or datos.get('correo', '').lower() == u.correo.lower() or datos.get('telefono') == u.telefono:
        raise ValidationError('No se puede registrar esta referencia.')
    if PadronPrueba.objects.filter(cedula=cedula).exists() or Socio.objects.filter(usuario__cedula=cedula).exists():
        raise ValidationError('No se puede registrar esta referencia.')
    contacto = datos.get('correo') or datos.get('telefono')
    if not contacto: raise ValidationError('Indica correo o teléfono de contacto.')
    if Prospecto.objects.filter(models.Q(identificacion_hash=huella(cedula)) | models.Q(contacto__iexact=contacto)).exists():
        raise ValidationError('No se puede registrar esta referencia.')
    campana = None
    if datos.get('campana'):
        campana = get_object_or_404(Campana.objects.select_for_update(), pk=datos['campana'])
        if not campana_visible(campana, codigo.socio): raise ValidationError('La campaña no está disponible.')
    nonce = secrets.token_urlsafe(32)
    token = huella('contacto:'+nonce)
    try:
        with transaction.atomic():
            p = Prospecto.objects.create(identificacion_hash=huella(cedula), nombre=datos['nombre'], contacto=contacto,
                telefono=datos.get('telefono'), correo=datos.get('correo'), producto=datos['producto'],
                consentimiento_en=None, token_nonce=nonce, token_hash=huella(token),
                expira_en=timezone.now()+timedelta(hours=getattr(settings, 'CONSENTIMIENTO_REFERIDO_HORAS', 48)))
            r = Referido.objects.create(codigo=codigo, prospecto=p, campana=campana)
            SolicitudContacto.objects.create(prospecto=p)
    except IntegrityError:
        raise ValidationError('No se puede registrar esta referencia.') from None
    historial(usuario, r, '', 'REGISTRADO', 'Solicitud de confirmación de contacto')
    return r


@transaction.atomic
def confirmar_referido(token):
    token_hash = huella(token)
    r = get_object_or_404(Referido.objects.select_for_update(of=('self',)), prospecto__token_hash=token_hash)
    p = get_object_or_404(Prospecto.objects.select_for_update(), pk=r.prospecto_id, token_hash=token_hash)
    if r.estado != 'REGISTRADO': raise ValidationError('La confirmación ya fue utilizada.')
    if p.expira_en <= timezone.now(): raise ValidationError('El enlace de confirmación venció.')
    p.confirmado_en = timezone.now()
    p.consentimiento_en = p.confirmado_en
    p.token_hash = None
    p.token_nonce = None
    p.save(update_fields=['confirmado_en', 'consentimiento_en', 'token_hash', 'token_nonce'])
    r.estado = 'CONFIRMADO'
    r.save(update_fields=['estado'])
    historial(None, r, 'REGISTRADO', r.estado, 'Consentimiento confirmado por el prospecto')
    return r


@transaction.atomic
def cambiar_referido(usuario, pk, estado, motivo, tipo_evento=None, monto_captado=None):
    exigir(usuario, 'referidos', [ADMIN, MARKETING])
    r = get_object_or_404(Referido.objects.select_for_update(), pk=pk)
    destinos = {'CONFIRMADO': ['EN_SEGUIMIENTO', 'RECHAZADO'],
                'EN_SEGUIMIENTO': ['CONVERTIDO', 'RECHAZADO'], 'REGISTRADO': ['EXPIRADO']}
    if estado not in destinos.get(r.estado, []) or not motivo.strip():
        raise ValidationError('La transición no está permitida o falta el motivo.')
    if estado == 'EXPIRADO' and r.prospecto.expira_en > timezone.now():
        raise ValidationError('Aún no ha vencido el plazo de confirmación.')
    if estado == 'CONVERTIDO':
        if tipo_evento not in ['APERTURA_CUENTA', 'PRODUCTO_CREDITICIO', 'TARJETA_ENTREGADA', 'SEGURO_CONTRATADO']:
            raise ValidationError('Selecciona un evento comercial permitido para el prototipo.')
        c = Conversion.objects.create(referido=r, tipo_evento=tipo_evento, validado_por=usuario, monto_captado=monto_captado)
        acreditar(r.codigo.socio, 'CONVERSION', c.pk)
    historial(usuario, r, r.estado, estado, motivo)
    r.estado = estado
    r.save(update_fields=['estado'])
    notificar(r.codigo.socio.usuario, 'REFERIDO', f'Tu referencia cambió a {estado.lower()}.', clave_evento=f'referido:{r.pk}:{estado}')
    auditar(usuario, r, 'CAMBIAR_REFERIDO', estado=estado, motivo=motivo)
    return r


@transaction.atomic
def solicitar_canje(usuario, beneficio_id, clave):
    socio = socio_de(usuario, 'recompensas')
    socio = Socio.objects.select_for_update().get(pk=socio.pk)
    anterior = Canje.objects.filter(socio=socio, clave=clave).first()
    if anterior:
        if anterior.beneficio_id != beneficio_id: raise ValidationError('La clave ya corresponde a otra solicitud.')
        return anterior
    b = get_object_or_404(Beneficio.objects.select_for_update(), pk=beneficio_id)
    hoy = timezone.localdate()
    if not b.activo or b.desde > hoy or (b.hasta and b.hasta < hoy) or (b.stock is not None and b.stock <= 0):
        raise ValidationError('El beneficio no está disponible.')
    if b.convenio and b.convenio.vigencia and b.convenio.vigencia < hoy:
        raise ValidationError('El convenio ya venció.')
    if saldo(socio) < b.costo_puntos: raise ValidationError('Tus puntos disponibles son insuficientes.')
    c = Canje.objects.create(socio=socio, beneficio=b, puntos=b.costo_puntos, clave=clave)
    MovimientoPuntos.objects.create(socio=socio, tipo='RESERVA', cantidad=c.puntos, origen_tipo='CANJE', origen_id=c.pk)
    if b.stock is not None:
        b.stock -= 1
        b.save(update_fields=['stock'])
    historial(usuario, c, '', c.estado, 'Reserva de puntos y disponibilidad')
    return c


@transaction.atomic
def resolver_canje(usuario, pk, estado, motivo):
    exigir(usuario, 'recompensas', [ADMIN])
    c = get_object_or_404(Canje.objects.select_for_update(), pk=pk)
    socio = Socio.objects.select_for_update().get(pk=c.socio_id)
    b = Beneficio.objects.select_for_update().get(pk=c.beneficio_id)
    if not motivo.strip(): raise ValidationError('Indica el motivo o constancia de la operación.')
    if estado not in ({'APROBADA', 'RECHAZADA'} if c.estado == 'PENDIENTE' else {'ENTREGADA'} if c.estado == 'APROBADA' else set()):
        raise ValidationError('La solicitud no admite esta transición.')
    if c.estado == 'PENDIENTE':
        MovimientoPuntos.objects.create(socio=socio, tipo='LIBERACION', cantidad=c.puntos, origen_tipo='CANJE', origen_id=c.pk)
        if estado == 'APROBADA':
            MovimientoPuntos.objects.create(socio=socio, tipo='DESCUENTO', cantidad=c.puntos, origen_tipo='CANJE', origen_id=c.pk)
        elif b.stock is not None:
            b.stock += 1
            b.save(update_fields=['stock'])
    if estado == 'ENTREGADA': c.fecha_entrega = timezone.now()
    historial(usuario, c, c.estado, estado, motivo)
    c.estado = estado
    c.aprobado_por = usuario
    c.save()
    notificar(socio.usuario, 'CANJE', f'Tu solicitud de {b.nombre} está {estado.lower()}.', clave_evento=f'canje:{c.pk}:{estado}')
    auditar(usuario, c, 'RESOLVER_CANJE', estado=estado, motivo=motivo)
    return c


@transaction.atomic
def inscribir(usuario, pk, acepta_requisitos=False):
    from .models import Capacitacion
    socio = socio_de(usuario, 'formacion')
    curso = get_object_or_404(Capacitacion.objects.select_for_update(), pk=pk, estado='PUBLICADA')
    if curso.requisitos.strip() and not acepta_requisitos:
        raise ValidationError('Confirma que cumples los requisitos publicados para la capacitación.')
    i, _ = Inscripcion.objects.get_or_create(socio=socio, capacitacion=curso)
    return i


def calificar(preguntas, respuestas):
    if not preguntas or not isinstance(respuestas, list) or len(respuestas) != len(preguntas):
        raise ValidationError('Responde todas las preguntas de la actividad.')
    correctas = 0
    for p, r in zip(preguntas, respuestas):
        if type(r) is not int or r < 0 or r >= len(p['opciones']):
            raise ValidationError('Una respuesta no corresponde a las opciones disponibles.')
        correctas += r == p['correcta']
    return (Decimal(correctas) * 100 / Decimal(len(preguntas))).quantize(Decimal('0.01'))


@transaction.atomic
def evaluar(usuario, curso_id, respuestas):
    socio = socio_de(usuario, 'formacion')
    i = get_object_or_404(Inscripcion.objects.select_for_update(), socio=socio, capacitacion_id=curso_id)
    if i.capacitacion.estado != 'PUBLICADA': raise ValidationError('La capacitación no está disponible.')
    e = get_object_or_404(Evaluacion, capacitacion_id=curso_id)
    from .models import ModuloCapacitacion
    unidades = ModuloCapacitacion.objects.filter(capacitacion_id=curso_id).count()
    if not unidades or Progreso.objects.filter(inscripcion=i, porcentaje=100).count() != unidades:
        raise ValidationError('Completa todos los módulos antes de evaluar.')
    if i.estado == 'APROBADO': raise ValidationError('Ya aprobaste esta capacitación.')
    if IntentoEvaluacion.objects.filter(inscripcion=i).count() >= e.max_intentos:
        raise ValidationError('Alcanzaste el máximo de intentos.')
    nota = calificar(e.preguntas, respuestas)
    intento = IntentoEvaluacion.objects.create(inscripcion=i, evaluacion=e, respuestas=respuestas, nota=nota, aprobado=nota >= e.nota_minima)
    if intento.aprobado:
        i.estado = 'APROBADO'
        i.save(update_fields=['estado'])
        acreditar(socio, 'CAPACITACION', i.pk)
        Certificado.objects.get_or_create(inscripcion=i, defaults={'codigo_verificacion': secrets.token_hex(16)})
        auditar(usuario, intento, 'APROBAR_CAPACITACION', inscripcion=i.pk)
        notificar(usuario, 'FORMACION', 'Aprobaste la capacitación. Tu certificado está disponible.', clave_evento=f'curso:{i.pk}')
    return intento


@transaction.atomic
def inscribir_taller(usuario, pk):
    socio = socio_de(usuario, 'formacion')
    t = get_object_or_404(Taller.objects.select_for_update(), pk=pk, estado='PROGRAMADO')
    if t.fecha <= timezone.now(): raise ValidationError('La inscripción al taller está cerrada.')
    previo = AsistenciaTaller.objects.filter(taller=t, socio=socio).first()
    if previo: return previo
    if t.cupo is not None and AsistenciaTaller.objects.filter(taller=t).count() >= t.cupo:
        raise ValidationError('El taller ya no tiene cupos disponibles.')
    return AsistenciaTaller.objects.create(taller=t, socio=socio)


@transaction.atomic
def asistencia(usuario, pk):
    exigir(usuario, 'formacion', [ADMIN, RSE, GESTOR])
    a = get_object_or_404(AsistenciaTaller.objects.select_for_update(), pk=pk)
    if a.taller.estado == 'CANCELADO' or a.taller.fecha > timezone.now():
        raise ValidationError('No puedes validar asistencia antes del taller ni en uno cancelado.')
    if not a.asistio:
        acreditar(a.socio, 'TALLER', a.pk)
        a.asistio = True
        a.save(update_fields=['asistio'])
        auditar(usuario, a, 'VALIDAR_ASISTENCIA')
    return a


@transaction.atomic
def iniciar_partida(usuario, pk):
    socio = socio_de(usuario, 'juegos')
    socio = Socio.objects.select_for_update().get(pk=socio.pk)
    juego = get_object_or_404(Juego.objects.select_for_update(), pk=pk, estado='ACTIVO')
    if Partida.objects.filter(socio=socio, juego=juego).count() >= juego.max_intentos:
        raise ValidationError('Alcanzaste el límite de intentos de este juego.')
    return Partida.objects.create(socio=socio, juego=juego)


@transaction.atomic
def finalizar_partida(usuario, pk, respuestas):
    socio = socio_de(usuario, 'juegos')
    p = get_object_or_404(Partida.objects.select_for_update(), pk=pk, socio=socio)
    if p.finalizada_en: return p
    if p.juego.estado != 'ACTIVO': raise ValidationError('El juego ya no está disponible.')
    p.puntuacion = calificar(p.juego.preguntas, respuestas)
    p.respuestas = respuestas
    p.finalizada_en = timezone.now()
    if p.puntuacion >= p.juego.nota_minima: acreditar(socio, 'JUEGO', p.pk)
    p.save()
    return p


@transaction.atomic
def ejecutar_sorteo(usuario, pk):
    exigir(usuario, 'sorteos', [ADMIN, MARKETING])
    s = get_object_or_404(Sorteo.objects.select_for_update(), pk=pk)
    if s.estado != 'ACTIVO' or s.fecha > timezone.now():
        raise ValidationError('El sorteo debe estar activo y haber alcanzado su fecha de ejecución.')
    candidatos = list(ParticipacionSorteo.objects.filter(sorteo=s, socio__usuario__estado='ACTIVA',
        socio__validado_en__isnull=False, socio__usuario__roles_asignados__rol__nombre='Socio').order_by('pk').distinct())
    # Un premio por socio, aun cuando posea varias participaciones.
    if len({c.socio_id for c in candidatos}) < s.num_ganadores + s.num_suplentes:
        raise ValidationError('No hay suficientes participantes elegibles para ganadores y suplentes.')
    congelada = [{'participacion': c.pk, 'socio': c.socio_id} for c in candidatos]
    serializada = json.dumps(congelada, separators=(',', ':'), sort_keys=True)
    s.evidencia = {'elegibles': congelada, 'sha256': hashlib.sha256(serializada.encode()).hexdigest(),
                  'fecha': timezone.now().isoformat(), 'algoritmo': 'secrets.SystemRandom', 'responsable': usuario.pk}
    s.save(update_fields=['evidencia'])
    ganadores = []
    for posicion in range(1, s.num_ganadores+s.num_suplentes+1):
        elegido = secrets.choice(candidatos)
        suplente = posicion > s.num_ganadores
        g = Ganador.objects.create(sorteo=s, participacion=elegido, posicion=posicion, es_suplente=suplente)
        ganadores.append(g)
        candidatos = [c for c in candidatos if c.socio_id != elegido.socio_id]
        if not suplente:
            notificar(elegido.socio.usuario, 'SORTEO', f'Ganaste {s.premio}. {s.condiciones}', clave_evento=f'ganador:{g.pk}')
    historial(usuario, s, s.estado, 'EJECUTADO', 'Selección aleatoria sobre lista congelada')
    s.estado = 'EJECUTADO'
    s.save(update_fields=['estado', 'evidencia'])
    auditar(usuario, s, 'EJECUTAR_SORTEO', sha256=s.evidencia['sha256'])
    return s


def comunidad_habilitada(usuario):
    socio = socio_de(usuario, 'comunidad')
    if SuspensionComunidad.objects.filter(socio=socio, hasta__gt=timezone.now()).exists():
        raise PermissionDenied('Tu participación en comunidad está suspendida temporalmente.')
    return socio
