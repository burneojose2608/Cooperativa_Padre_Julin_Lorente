"""Mapeo de las entidades ya previstas por el esquema del proyecto."""
from django.db import models
from django.conf import settings
from django.utils import timezone


def fk(modelo, columna, **kwargs):
    if kwargs.pop('unique', False):
        return models.OneToOneField(modelo, db_column=columna, on_delete=models.DO_NOTHING, **kwargs)
    return models.ForeignKey(modelo, db_column=columna, on_delete=models.DO_NOTHING, **kwargs)


class Base(models.Model):
    class Meta:
        abstract = True
        managed = False


class Campana(Base):
    id_campana = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    inicio = models.DateField()
    fin = models.DateField()
    estado = models.CharField(max_length=12, default='BORRADOR')
    creado_por = fk(settings.AUTH_USER_MODEL, 'creado_por')
    creado_en = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=30)
    objetivo = models.CharField(max_length=300)
    meta = models.IntegerField()
    incentivos = models.TextField()
    condiciones = models.TextField(default='')
    segmentacion = models.JSONField(default=dict)
    class Meta(Base.Meta): db_table = 'campana'


class Prospecto(Base):
    id_prospecto = models.BigAutoField(primary_key=True)
    identificacion_hash = models.CharField(max_length=64, null=True)
    contacto = models.CharField(max_length=254)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15, null=True)
    correo = models.CharField(max_length=254, null=True)
    producto = models.CharField(max_length=150)
    estado = models.CharField(max_length=20, default='REGISTRADO')
    creado_en = models.DateTimeField(auto_now_add=True)
    consentimiento_en = models.DateTimeField(null=True)
    confirmado_en = models.DateTimeField(null=True)
    version_politica = models.CharField(max_length=40, default='1.0')
    token_hash = models.CharField(max_length=64, null=True)
    token_nonce = models.CharField(max_length=100, null=True)
    expira_en = models.DateTimeField(null=True)
    class Meta(Base.Meta): db_table = 'prospecto'


class SolicitudContacto(Base):
    id_solicitud = models.BigAutoField(primary_key=True)
    prospecto = fk(Prospecto, 'id_prospecto', unique=True)
    estado = models.CharField(max_length=12, default='PENDIENTE')
    intentos = models.IntegerField(default=0)
    disponible_en = models.DateTimeField(default=timezone.now)
    reservado_hasta = models.DateTimeField(null=True)
    reserva = models.UUIDField(null=True)
    class Meta(Base.Meta): db_table = 'solicitud_contacto'


class Referido(Base):
    id_referido = models.BigAutoField(primary_key=True)
    codigo = fk('plataforma.CodigoReferido', 'id_codigo')
    prospecto = fk(Prospecto, 'id_prospecto')
    campana = fk(Campana, 'id_campana', null=True)
    estado = models.CharField(max_length=15, default='REGISTRADO')
    creado_en = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'referido'


class Conversion(Base):
    id_conversion = models.BigAutoField(primary_key=True)
    referido = fk(Referido, 'id_referido', unique=True)
    tipo_evento = models.CharField(max_length=25)
    fecha_validacion = models.DateTimeField(auto_now_add=True)
    validado_por = fk(settings.AUTH_USER_MODEL, 'validado_por')
    monto_captado = models.DecimalField(max_digits=18, decimal_places=2, null=True)
    class Meta(Base.Meta): db_table = 'conversion'


class GastoCampana(Base):
    id_gasto = models.BigAutoField(primary_key=True)
    campana = fk(Campana, 'id_campana')
    fecha = models.DateField()
    concepto = models.CharField(max_length=300)
    importe = models.DecimalField(max_digits=18, decimal_places=2)
    class Meta(Base.Meta): db_table = 'gasto_campana'


class MovimientoPuntos(Base):
    id_movimiento = models.BigAutoField(primary_key=True)
    socio = fk('usuarios.Socio', 'id_socio')
    regla = fk('plataforma.ReglaPuntos', 'id_regla', null=True)
    tipo = models.CharField(max_length=12)
    cantidad = models.IntegerField()
    origen_tipo = models.CharField(max_length=12)
    origen_id = models.BigIntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(default='')
    class Meta(Base.Meta): db_table = 'movimiento_puntos'


class ActividadValidada(Base):
    id_actividad = models.BigAutoField(primary_key=True)
    socio = fk('usuarios.Socio', 'id_socio')
    origen_tipo = models.CharField(max_length=20)
    origen_id = models.BigIntegerField()
    validada_en = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'actividad_validada'


class Nivel(Base):
    id_nivel = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=60, unique=True)
    umbral_puntos = models.IntegerField(unique=True)
    class Meta(Base.Meta): db_table = 'nivel'


class Insignia(Base):
    id_insignia = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=80, unique=True)
    criterio = models.CharField(max_length=300)
    umbral = models.IntegerField(default=1)
    icono = models.CharField(max_length=100, default='', blank=True)
    class Meta(Base.Meta): db_table = 'insignia'


class SocioInsignia(Base):
    id_socio_insignia = models.BigAutoField(primary_key=True)
    socio = fk('usuarios.Socio', 'id_socio')
    insignia = fk(Insignia, 'id_insignia')
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'socio_insignia'


class Inscripcion(Base):
    id_inscripcion = models.BigAutoField(primary_key=True)
    socio = fk('usuarios.Socio', 'id_socio')
    capacitacion = fk('plataforma.Capacitacion', 'id_capacitacion')
    estado = models.CharField(max_length=12, default='INSCRITO')
    creado_en = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'inscripcion'


class Progreso(Base):
    id_progreso = models.BigAutoField(primary_key=True)
    inscripcion = fk(Inscripcion, 'id_inscripcion')
    unidad = fk('plataforma.ModuloCapacitacion', 'id_unidad')
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    class Meta(Base.Meta): db_table = 'progreso'


class Evaluacion(Base):
    id_evaluacion = models.BigAutoField(primary_key=True)
    capacitacion = fk('plataforma.Capacitacion', 'id_capacitacion')
    nota_minima = models.DecimalField(max_digits=5, decimal_places=2)
    max_intentos = models.IntegerField(default=3)
    preguntas = models.JSONField(default=list)
    class Meta(Base.Meta): db_table = 'evaluacion'


class IntentoEvaluacion(Base):
    id_intento = models.BigAutoField(primary_key=True)
    inscripcion = fk(Inscripcion, 'id_inscripcion')
    evaluacion = fk(Evaluacion, 'id_evaluacion')
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    aprobado = models.BooleanField(null=True)
    respuestas = models.JSONField(default=list)
    class Meta(Base.Meta): db_table = 'intento_evaluacion'


class Certificado(Base):
    id_certificado = models.BigAutoField(primary_key=True)
    inscripcion = fk(Inscripcion, 'id_inscripcion', unique=True)
    codigo_verificacion = models.CharField(max_length=32, unique=True)
    emitido_en = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'certificado'


class Taller(Base):
    id_taller = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    cupo = models.IntegerField()
    estado = models.CharField(max_length=12, default='PROGRAMADO')
    modalidad = models.CharField(max_length=20)
    lugar = models.CharField(max_length=500)
    duracion = models.IntegerField(default=1)
    class Meta(Base.Meta): db_table = 'taller'


class AsistenciaTaller(Base):
    id_asistencia = models.BigAutoField(primary_key=True)
    taller = fk(Taller, 'id_taller')
    socio = fk('usuarios.Socio', 'id_socio')
    asistio = models.BooleanField(default=False)
    registrado_en = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'asistencia_taller'


class Convenio(Base):
    id_convenio = models.BigAutoField(primary_key=True)
    entidad = models.CharField(max_length=150)
    tipo = models.CharField(max_length=40)
    vigencia = models.DateField(null=True)
    descripcion = models.TextField()
    condiciones = models.TextField()
    beneficio = models.TextField()
    class Meta(Base.Meta): db_table = 'convenio'


class Beneficio(Base):
    id_beneficio = models.BigAutoField(primary_key=True)
    convenio = fk(Convenio, 'id_convenio', null=True, related_name='beneficios')
    nombre = models.CharField(max_length=150)
    costo_puntos = models.IntegerField()
    stock = models.IntegerField(null=True)
    descripcion = models.TextField()
    condiciones = models.TextField()
    desde = models.DateField()
    hasta = models.DateField(null=True)
    activo = models.BooleanField(default=True)
    class Meta(Base.Meta): db_table = 'beneficio'


class Canje(Base):
    id_canje = models.BigAutoField(primary_key=True)
    socio = fk('usuarios.Socio', 'id_socio')
    beneficio = fk(Beneficio, 'id_beneficio')
    estado = models.CharField(max_length=10, default='PENDIENTE')
    aprobado_por = fk(settings.AUTH_USER_MODEL, 'aprobado_por', null=True)
    fecha_entrega = models.DateTimeField(null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    puntos = models.IntegerField()
    clave = models.UUIDField(null=True)
    class Meta(Base.Meta): db_table = 'canje'


class Sorteo(Base):
    id_sorteo = models.BigAutoField(primary_key=True)
    campana = fk(Campana, 'id_campana')
    premio = models.CharField(max_length=200)
    nombre = models.CharField(max_length=150)
    condiciones = models.TextField()
    origen = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=12, default='BORRADOR')
    num_ganadores = models.SmallIntegerField(default=1)
    num_suplentes = models.SmallIntegerField(default=0)
    evidencia = models.JSONField(default=dict)
    class Meta(Base.Meta): db_table = 'sorteo'


class ParticipacionSorteo(Base):
    id_participacion = models.BigAutoField(primary_key=True)
    sorteo = fk(Sorteo, 'id_sorteo')
    socio = fk('usuarios.Socio', 'id_socio')
    origen_tipo = models.CharField(max_length=20)
    origen_id = models.BigIntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'participacion_sorteo'


class Ganador(Base):
    id_ganador = models.BigAutoField(primary_key=True)
    sorteo = fk(Sorteo, 'id_sorteo')
    participacion = fk(ParticipacionSorteo, 'id_participacion')
    posicion = models.SmallIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    es_suplente = models.BooleanField(default=False)
    class Meta(Base.Meta): db_table = 'ganador'


class Juego(Base):
    id_juego = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=16)
    estado = models.CharField(max_length=10, default='INACTIVO')
    max_intentos = models.SmallIntegerField()
    instrucciones = models.TextField()
    preguntas = models.JSONField(default=list)
    nota_minima = models.IntegerField(default=60)
    class Meta(Base.Meta): db_table = 'juego'


class Partida(Base):
    id_partida = models.BigAutoField(primary_key=True)
    juego = fk(Juego, 'id_juego')
    socio = fk('usuarios.Socio', 'id_socio')
    puntuacion = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    finalizada_en = models.DateTimeField(null=True)
    respuestas = models.JSONField(default=list)
    class Meta(Base.Meta): db_table = 'partida'


class Reto(Base):
    id_reto = models.BigAutoField(primary_key=True)
    objetivo = models.CharField(max_length=200)
    meta = models.IntegerField()
    inicio = models.DateField()
    fin = models.DateField()
    actividad = models.CharField(max_length=30)
    class Meta(Base.Meta): db_table = 'reto'


class ProgresoReto(Base):
    id_progreso_reto = models.BigAutoField(primary_key=True)
    reto = fk(Reto, 'id_reto')
    socio = fk('usuarios.Socio', 'id_socio')
    avance = models.IntegerField(default=0)
    completado_en = models.DateTimeField(null=True)
    class Meta(Base.Meta): db_table = 'progreso_reto'


class Publicacion(Base):
    id_publicacion = models.BigAutoField(primary_key=True)
    usuario = fk(settings.AUTH_USER_MODEL, 'id_usuario')
    texto = models.TextField()
    imagen = models.CharField(max_length=500, default='')
    estado_moderacion = models.CharField(max_length=12, default='VISIBLE')
    creado_en = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'publicacion'


class Comentario(Base):
    id_comentario = models.BigAutoField(primary_key=True)
    publicacion = fk(Publicacion, 'id_publicacion')
    usuario = fk(settings.AUTH_USER_MODEL, 'id_usuario')
    texto = models.TextField()
    estado = models.CharField(max_length=12, default='VISIBLE')
    creado_en = models.DateTimeField(auto_now_add=True)
    class Meta(Base.Meta): db_table = 'comentario'


class Reaccion(Base):
    id_reaccion = models.BigAutoField(primary_key=True)
    publicacion = fk(Publicacion, 'id_publicacion')
    usuario = fk(settings.AUTH_USER_MODEL, 'id_usuario')
    tipo = models.CharField(max_length=20)
    class Meta(Base.Meta): db_table = 'reaccion'


class ReporteComunidad(Base):
    id_reporte = models.BigAutoField(primary_key=True)
    publicacion = fk(Publicacion, 'id_publicacion', null=True)
    comentario = fk(Comentario, 'id_comentario', null=True)
    usuario = fk(settings.AUTH_USER_MODEL, 'id_usuario')
    motivo = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    resuelto_en = models.DateTimeField(null=True)
    resolucion = models.TextField(default='')
    class Meta(Base.Meta): db_table = 'reporte_comunidad'


class SuspensionComunidad(Base):
    id_suspension = models.BigAutoField(primary_key=True)
    socio = fk('usuarios.Socio', 'id_socio')
    hasta = models.DateTimeField()
    motivo = models.TextField()
    responsable = fk(settings.AUTH_USER_MODEL, 'responsable_id')
    class Meta(Base.Meta): db_table = 'suspension_comunidad'
