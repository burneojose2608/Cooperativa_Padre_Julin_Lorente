"""Construye una especificación revisada; no escribe EA ni regenera la propuesta anterior."""
from pathlib import Path
import json, re, csv, xml.etree.ElementTree as E, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent
O=Path((B/'entrega-actual.txt').read_text(encoding='utf-8-sig').strip())
M=json.loads((B/'fuentes/modelo.json').read_text(encoding='utf-8'))
C={c['nombre']:c for c in M['clases']}
def change(n,attrs=None,ops=None,note=None):
    if attrs is not None:C[n]['atributos']=attrs
    if ops is not None:C[n]['operaciones']=ops
    if note:C[n]['nota']=note
def add(n,module,attrs,ops,note):
    C[n]=dict(nombre=n,modulo=module,atributos=attrs,operaciones=ops,nota=note)
R=M['asociaciones']; D=M['dependencias']
# Revisión de responsabilidades: el registro y la autorización dejan de concentrarse en ControlAcceso.
old=C['ControlAcceso']['operaciones']
change('ControlAcceso',[],[x for x in old if x.startswith(('validarCredenciales','registrarIntentoFallido'))],
       'Servicio de autenticación, sin estado propio. Lee cuenta activa y bloqueo; cinco fallos bloquean quince minutos. Los contadores pertenecen a Usuario. HU-009/010; autenticacion_service.py.')
add('ServicioRegistro','Identidad',[],[x for x in old if x.startswith(('registrarCuenta','validarUnicidad','registrarPersonal'))],
    'Coordina alta atómica, unicidad, padrón, consentimiento, socio opcional, roles y auditoría. Registro público implementado; alta de personal por comando/servicio; no administración completa. HU-001/005/006/008; registro_service.py y usuarios_internos_service.py.')
add('ServicioAutorizacion','Seguridad',[],[x for x in old if x.startswith(('autorizar','identificarRoles','asignarRol','revocarRol'))],
    'Consulta roles actuales y titularidad. Unión de accesos implementada; configuración dinámica completa de permisos y revocación administrativa planificadas. HU-012/013/014; roles_service.py y permissions.py.')
change('ValidacionAdministrativaSocio',[],['validarYHabilitar(cuenta: Usuario, administrador: Usuario, confirmacion: Booleano): Socio'],
       'Servicio manual temporal implementado por conversion_socio_service.py. Confirmación true estricta, administrador activo, cuenta general activa sin roles, padrón no inactivo; transacción e idempotencia. Evidencia en EventoAuditoria. No crea conversión comercial ni puntos. Fuente: conversion-administrativa-temporal.md; ampliación sin HU original exacta.')
C['Usuario']['atributos']+=['intentosFallidos: Entero','bloqueadoHasta: FechaHora [0..1]']
C['Socio']['atributos']=[x for x in C['Socio']['atributos'] if not x.startswith(('tipoSocio','agencia','productosSegmentacion'))]
C['Socio']['nota']+=' Los datos de segmentación no se afirman disponibles; P05 exige definir una fuente autorizada.'
change('ConsentimientoCuenta',['finalidad: Texto','aceptado: Booleano','aceptadoEn: FechaHora','versionPolitica: Texto'],[],
       'Evidencia inmutable de aceptación expresa. Solo se conserva si aceptado=true, con fecha y versión; finalidad explícita es propuesta de análisis pendiente de texto aprobado. Fecha/versión implementadas; HU-001, consentimiento.py; RNF-02.')
C['ConsentimientoProspecto']['atributos']+=['aceptado: Booleano']
C['ConsentimientoProspecto']['nota']+=' Aceptado=false mientras no confirma; aceptadoEn presente si y solo si aceptado=true. El plazo es configurable, sin duración inventada.'
change('AprobacionContenido',ops=[])
C['ContenidoInstitucional']['operaciones']+=['decidirAprobacion(aprobar: Booleano, motivo: Texto, responsable: Usuario): AprobacionContenido']
change('ActividadValidada',['tipo: TipoActividad','referenciaOrigen: Texto','fecha: FechaHora'],[],
       'Hecho reconocido tras validación de conversión, capacitación, asistencia, juego o reto. Objeto de valor inmutable, no tabla ni endpoint genérico. La referencia y el beneficiario identifican el origen; no se convierte la validación administrativa en actividad. HU-032/049/075/078.')
change('Conversion',ops=[])
change('MaterialEducativo',ops=['esAdmisible(): Booleano'])
change('Permiso',ops=[])
change('Certificado',ops=[x for x in C['Certificado']['operaciones'] if not x.startswith('emitir(')])
C['InscripcionCapacitacion']['operaciones']+=['emitirCertificado(ahora: FechaHora): Certificado']
change('EvidenciaSorteo',[x for x in C['EvidenciaSorteo']['atributos'] if not x.startswith('listaCongelada:')]+['evidenciaEjecucion: Texto [0..1]'])
add('ElegibleCongelado','Sorteos',['referenciaParticipacion: Texto','referenciaSocio: Texto','condicionValidada: Texto','ordenCanonico: Entero'],[],
    'Instantánea inmutable de cada participación elegible al cierre, no consulta de lista viva. Conserva identidad seudonimizada y condiciones que fundamentaron inclusión. El hash de EvidenciaSorteo se calcula sobre estas entradas con orden y serialización documentados. HU-050/053; propuesta de análisis.')
add('ReconocimientoIncentivo','Campanas',['fecha: FechaHora','versionReconocida: Texto','tipoReconocido: Texto','cantidadReconocida: Entero','condicionesReconocidas: Texto'],[],
    'Instantánea inmutable que impide alterar incentivos reconocidos cuando cambia la campaña. Tiene origen en actividad validada y versión del incentivo; no presupone tabla implementada. HU-029; Presentacion hoja RF-04, modificar campañas.')
add('ServicioNotificaciones','Notificaciones',[],['notificarEvento(evento: Texto, destinatario: Usuario): Notificacion','notificarGanadores(sorteo: Sorteo): Coleccion<Notificacion>','consultarHistorial(filtro: FiltroReporte, solicitante: Usuario): Coleccion<EnvioNotificacion>'],
    'Coordina eventos válidos, plantillas, preferencias y entregas sin bloquear negocio. Historial consultable con autorización. Módulo general planificado; recuperación por correo no demuestra su implementación. HU-052/068/070.')
C['EnvioNotificacion']['operaciones']=[x for x in C['EnvioNotificacion']['operaciones'] if not x.startswith('consultarHistorial')]
C['Sorteo']['operaciones']+=['consultarHistorial(solicitante: Usuario): EvidenciaSorteo']
# Se eliminan vínculos que confundían estado de servicio con pertenencia persistente.
R=[r for r in R if 'ControlAcceso' not in (r[0],r[2]) and 'ValidacionAdministrativaSocio' not in (r[0],r[2])]
for r in R:
    if r[0:3:2]==['Capacitacion','Evaluacion']:r[3]='0..*'; r[4]='evaluaciones de la capacitación; SQL 01 permite varias, una final no aprobada'
    if r[0:3:2]==['CuentaPuntos','Nivel']: r[4]='nivel derivado; base de puntos y descensos pendientes P06'
    if r[0:3:2]==['PremioSorteo','ResultadoSorteo']: r[4]='premio para ganador; suplente puede no tener asignación, política de adjudicación pendiente'
R += [
 ['EvidenciaSorteo','1','ElegibleCongelado','0..*','entradas congeladas preservadas con su evidencia; ejecución requiere conjunto no vacío'],
 ['ParticipacionSorteo','1','ElegibleCongelado','0..1','participación de origen identificable aunque cambie elegibilidad posterior'],
 ['IncentivoCampana','1','ReconocimientoIncentivo','0..*','versión que originó condiciones reconocidas; no se modifica retroactivamente'],
 ['ActividadValidada','1','ReconocimientoIncentivo','0..*','hecho que fundamenta incentivo; unicidad por actividad, beneficiario e incentivo'],
 ['ReconocimientoIncentivo','0..1','MovimientoPuntos','0..*','origen promocional cuando aplica; no exige puntos a todo incentivo'],
 ['Referido','0..1','CambioEstado','0..*','historial propio conservado; sujeto exclusivo XOR campaña/canje/usuario'],
 ['Campana','0..1','CambioEstado','0..*','historial propio conservado; sujeto exclusivo XOR referido/canje/usuario'],
 ['Canje','0..1','CambioEstado','0..*','historial propio conservado; sujeto exclusivo XOR referido/campaña/usuario'],
 ['Usuario','0..1','CambioEstado','0..*','cuenta afectada por cambio; distinto del responsable, sujeto exclusivo'],
]
D=[x for x in D if x[0]!='ControlAcceso' and not (x[0] in ['Referido','Campana','Canje'] and x[1]=='CambioEstado')]
D += [
 ('ControlAcceso','Usuario','comprueba credenciales y estado; conserva contador en la cuenta'),
 ('ControlAcceso','Sesion','abre sesión revocable'),('ControlAcceso','EventoAuditoria','registra éxito o rechazo'),
 ('ServicioRegistro','Usuario','valida unicidad y registra cuenta'),('ServicioRegistro','EntradaPadron','consulta estado sin interpretar fallo como ausencia'),
 ('ServicioRegistro','ConsentimientoCuenta','exige y conserva aceptación'),('ServicioRegistro','Socio','habilita solo ante padrón activo'),
 ('ServicioRegistro','Rol','asigna roles autorizados'),('ServicioRegistro','EventoAuditoria','conserva evidencia del alta'),
 ('ServicioAutorizacion','Usuario','comprueba estado y titularidad'),('ServicioAutorizacion','Rol','consulta roles vigentes'),
 ('ServicioAutorizacion','Permiso','aplica capacidades; gestión completa planificada'),
 ('ValidacionAdministrativaSocio','Usuario','comprueba cuenta y administrador activo'),('ValidacionAdministrativaSocio','Rol','asigna Socio sin autoconversión'),
 ('ValidacionAdministrativaSocio','EventoAuditoria','audita confirmación manual temporal'),
 ('ServicioNotificaciones','PlantillaNotificacion','prepara aviso por evento'),('ServicioNotificaciones','PreferenciaNotificacion','respeta canales opcionales'),
 ('ServicioNotificaciones','Notificacion','genera aviso'),('ServicioNotificaciones','EnvioNotificacion','coordina entrega e historial'),
 ('ServicioNotificaciones','Sorteo','consulta ganadores autorizados'),
]
enums={
 'EstadoCuenta':['Activa','Suspendida','Desactivada'],
 'EstadoReferido':['Registrado','Confirmado','EnSeguimiento','Convertido','Rechazado','Expirado'],
 'EstadoCampana':['Borrador','Activa','Suspendida','Finalizada'],
 'TipoMovimiento':['Acreditacion','Reserva','Descuento','Liberacion','Reverso'],
 'EstadoCanje':['Pendiente','Aprobada','Rechazada','Entregada'],
 'Canal':['Plataforma','Correo'], 'TipoJuego':['Trivia','VerdaderoFalso','Emparejar'],
 'TipoConversion':['AperturaCuenta','ProductoCrediticio'],
 'TipoActividad':['ConversionReferido','CapacitacionAprobada','AsistenciaTaller','Juego','Reto'],
 'EstadoTaller':['Programado','Realizado','Cancelado'],
}
enum_sources={n:'backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos' for n in enums}
enum_sources['EstadoTaller']='backend/sql/02_ajustes_recomendados.sql, ck_taller_estado'
# Los tipos auxiliares opacos se expresan como texto de análisis; no se agregan DTO ni clases técnicas.
aux=['Identificador','Recurso','Referencia','Condiciones','DatosRegistro','DatosPerfil','DatosEvento','DatosPublicos','DatosEnmascarados','Indicador','Criterio','PosicionPublica','Secreto','DatosSeguimiento']
for c in C.values():
    for field in ['atributos','operaciones']:
        c[field]=[re.sub(r'\b('+ '|'.join(aux)+r')\b','Texto',x) for x in c[field]]
    # Los tipos configurables no tienen enumeraciones cerradas sin fuente.
    if c['nombre']=='Taller':c['atributos']=[x.replace('estado: Texto','estado: EstadoTaller') for x in c['atributos']]
    if c['nombre']=='ReglaPuntos':c['atributos']=[x.replace('tipoActividad: Texto','tipoActividad: TipoActividad') for x in c['atributos']]
    if c['nombre']=='FiltroReporte':c['atributos']=[x for x in c['atributos'] if not x.startswith(('campana:','segmento:'))]
R += [['Campana','0..1','FiltroReporte','0..*','campaña seleccionada opcionalmente como filtro de consulta'],['Segmento','0..1','FiltroReporte','0..*','segmento seleccionado opcionalmente como filtro de consulta']]
R += [['Usuario','1','EvidenciaSorteo','0..*','responsable de ejecución que queda conservado en la evidencia del sorteo']]
C['CuentaPuntos']['operaciones']=[x.replace('revertir(original: MovimientoPuntos, motivo: Texto)', 'revertir(original: MovimientoPuntos, motivo: Texto, responsable: Usuario)') for x in C['CuentaPuntos']['operaciones']]
# Firma breve de alta: los demás atributos obligatorios pertenecen a la cuenta que se valida.
change('ServicioRegistro',ops=['registrarCuenta(cuenta: Usuario, clave: Texto, consentimiento: ConsentimientoCuenta): Usuario',
 'validarUnicidad(cuenta: Usuario): Booleano','registrarPersonal(cuenta: Usuario, roles: Coleccion<Rol>, administrador: Usuario): Usuario'])
C['ServicioRegistro']['nota']+=' El parámetro cuenta es una cuenta propuesta con sus datos obligatorios, aún sin alta; no es DTO ni habilita credenciales en texto almacenado. La clave es entrada transitoria.'
services={'ControlAcceso','ServicioRegistro','ServicioAutorizacion','ServicioReportes','ServicioNotificaciones','ValidacionAdministrativaSocio'}
records={'ConsentimientoCuenta','EventoAuditoria','CambioEstado','Conversion','MovimientoPuntos','InsigniaObtenida','PremioSorteo','EvidenciaSorteo','ResultadoSorteo','ElegibleCongelado','ReconocimientoIncentivo','AprobacionContenido','Certificado'}
values={'ActividadValidada','RespuestaActividad','FiltroReporte','ResultadoReporte'}
for n,c in C.items():
    c['estereotipo']='ServicioDominio' if n in services else 'Registro' if n in records else 'ObjetoValor' if n in values else 'Entidad'
    c['estado']='Propuesta de análisis' if n in values|{'CuentaPuntos','Clasificacion','ReconocimientoIncentivo','ElegibleCongelado','AprobacionContenido','ServicioReportes','ServicioNotificaciones','ReporteComunidad','DecisionModeracion','PerfilPublico','IncentivoCampana','ParticipacionCampana','ConsentimientoProspecto','EvidenciaSorteo'} else 'Planificado'
    if n in {'Usuario','Socio','Rol','ConsentimientoCuenta','ServicioRegistro','ServicioAutorizacion'}: c['estado']='Implementado parcialmente'
    if n in {'EntradaPadron','Sesion','RecuperacionAcceso','ControlAcceso','EventoAuditoria','ValidacionAdministrativaSocio'}:c['estado']='Implementado'
    c['nota']+=' Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.'

rules={
 'R01':('Registro vigente','Cédula Texto con diez dígitos ASCII y trim exterior; sin provincia ni verificador. Unicidad de cédula y de correo/usuario normalizados. Padrón activo crea socio; ausente cuenta general sin roles; inactivo rechaza; indisponible aborta. Alta atómica.', 'decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06','Sustentada', ['Usuario','ServicioRegistro','EntradaPadron','Socio']),
 'R02':('Roles y condición de socio','Usuario con cero o varios roles, y cero o un Socio; no herencia de actores. La autorización consulta roles actuales y titularidad. Cinco fallos bloquean quince minutos; inactividad de quince minutos invalida sesión.', 'HU-009/010/012/014/015; roles_service.py; sesiones_service.py','Sustentada',['Usuario','Rol','ServicioAutorizacion','ControlAcceso','Sesion']),
 'R03':('Validación temporal','Manual, confirmación estricta de administrador activo; destino general activo sin roles. Inactivo o inconsistencia rechaza. Repetición devuelve mismo socio. No cambia credenciales ni consentimiento. No reconoce puntos comerciales.', 'conversion-administrativa-temporal.md; conversion_socio_service.py','Sustentada',['ValidacionAdministrativaSocio','EventoAuditoria','Socio']),
 'R04':('Consentimientos separados','Cuenta y prospecto conservan finalidad, aceptación, fecha y versión. Prospecto no exige cuenta. Sin confirmación dentro del plazo configurable expira referido; no se inventa duración ni política completa de revocación. Finalidad/versionado del prospecto aún no completos en SQL.', 'HU-001/023; RNF-02/25; SQL 02; consentimiento.py','Parcial y propuesta explícita',['ConsentimientoCuenta','ConsentimientoProspecto','Prospecto','Referido']),
 'R05':('Referido y conversión','Código referido no equivale a codigoSocio. Evitar autorreferido, duplicado activo y prospecto ya socio. Conversión comercial con evidencia de prueba, responsable y fecha; una por prospecto y reconocimiento único. Aristas exactas del ciclo y retiro de consentimiento pendientes.', 'HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16','Sustentada con brecha de unicidad SQL por referido',['CodigoReferido','Prospecto','Referido','Conversion','CambioEstado']),
 'R06':('Campaña e incentivo','Vigencia y elegibilidad antes de participar. Cambios versionan condiciones sin alterar lo reconocido; instantánea propuesta en ReconocimientoIncentivo. Tasa de conversión según HU-030; meta requiere unidad definida. Fuente y combinación de segmentos pendientes P05.', 'HU-025–030; Presentacion RF-04; SQL 01–02','Sustentada; estructura de instantánea propuesta',['Campana','Segmento','IncentivoCampana','ReconocimientoIncentivo','ParticipacionCampana']),
 'R07':('Libro e idempotencia','Movimientos inmutables con cantidad positiva, tipo y origen identificable; clave de idempotencia por beneficiario/origen/tipo. Reversos compensan y referencian original, nunca lo editan. Límites por período configurables: unidad, zona horaria y efecto del reverso pendientes P16.', 'HU-031/032/036/038/059; SQL 01','Sustentada, detalle pendiente',['MovimientoPuntos','CuentaPuntos','ReglaPuntos','ActividadValidada']),
 'R08':('Saldos y reserva','Propuesta a validar P07: contable = acreditaciones - descuentos - reversos de acreditación; reservado = reservas abiertas; disponible = contable - reservado. Reserva no es descuento definitivo. Aprobar cierra reserva y registra un único descuento; rechazar libera. Ejemplo: 100 contable, reserva 30 => disponible 70; aprobar => contable 70, reservado 0, disponible 70. No se inventa saldo negativo, caducidad, ni política de reverso ya gastado.', 'HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07','Propuesta de análisis, no implementación',['CuentaPuntos','Canje','MovimientoPuntos']),
 'R09':('Niveles y clasificación','Umbrales y criterios configurados; base acumulada/disponible, descensos, empates y períodos pendientes P06. No deducir descenso por canje. Alias y exclusión pública respetados.', 'HU-033/035/037/083','Sustentada con política pendiente',['Nivel','Insignia','InsigniaObtenida','Clasificacion','PerfilPublico']),
 'R10':('Formación y asistencia','Inscripción única socio-capacitación y socio-taller. Progreso de módulos de la misma capacitación entre cero y cien; fórmula agregada y acceso a evaluación pendientes. Calificación en servidor, umbral e intentos configurados; certificado tras aprobar con código único no secuencial. Asistencia validada por responsable, distinta de inscripción, acreditada una vez.', 'HU-039–047; SQL 01–02','Sustentada; detalles pendientes',['Capacitacion','ModuloCapacitacion','InscripcionCapacitacion','ProgresoModulo','Evaluacion','IntentoEvaluacion','Certificado','Taller','InscripcionTaller']),
 'R11':('Preguntas y respuestas','Pregunta pertenece a evaluación XOR juego; respuesta a intento XOR partida. Alternativas pertenecen exclusivamente a pregunta. SQL solo permite una correcta como máximo; emparejamiento necesita política P08 y no se simula con esta restricción.', 'HU-041/072/074; SQL 02, ck_pregunta_dueno','Sustentada con brecha',['Pregunta','OpcionPregunta','RespuestaActividad','Evaluacion','Juego','Partida','IntentoEvaluacion']),
 'R12':('Sorteos verificables','Congelar entradas elegibles antes de selección; hash sobre contenido canónico congelado, registrar método, fecha, responsable, ganadores y suplentes. Ejecutar una sola vez, no reconsultar lista viva como evidencia. Resultado pertenece a participación del mismo sorteo. No define fórmula aleatoria ni adjudicación posterior sin política.', 'HU-048–053; SQL 01–02','Sustentada; evidencia estructurada propuesta',['Sorteo','ParticipacionSorteo','ElegibleCongelado','EvidenciaSorteo','PremioSorteo','ResultadoSorteo']),
 'R13':('Canjes y catálogo','Pendiente a Aprobada a Entregada, o Pendiente a Rechazada. Instantánea de costo y condiciones; saldo, reserva y stock coordinados sin doble descuento. Momento de reservar/devolver stock y costo cero pendientes P02/P07.', 'HU-054–059; SQL 01–02','Sustentada con pendientes',['Beneficio','Canje','CuentaPuntos']),
 'R14':('Contenido y comunidad','Institucional y comunitario tienen ciclo distinto. Aprobación institucional solo si aplica; responsable designado. Oculto no admite interacción. Reporte sobre publicación XOR comentario. Moderar con motivo/fecha/responsable; alcance y duración de suspensión pendientes. Material reutilizable, máximo diez MB y formatos de HU.', 'HU-060–065/079–083; SQL 01–02','Sustentada, moderación estructurada propuesta',['ContenidoInstitucional','AprobacionContenido','MaterialEducativo','PublicacionComunidad','Comentario','Reaccion','ReporteComunidad','DecisionModeracion','PerfilPublico']),
 'R15':('Juegos y retos','Resultado calculado por servidor y límite configurado de intentos. Solo resultado válido reconoce puntos. Reto medible y vigente, una recompensa por socio-reto y actividades sin duplicación. Sin fórmula inventada.', 'HU-071–078; SQL 01','Sustentada',['Juego','Partida','Reto','ProgresoReto']),
 'R16':('Bienestar','Convenios, recursos y beneficios informativos; convenio vencido impide ofrecer beneficio. Sin historiales clínicos, cuentas financieras reales, préstamos operativos ni integración productiva con core.', 'Acta, alcance; HU-084–086; RNF-24','Sustentada',['ConvenioBienestar','RecursoBienestar','Beneficio']),
 'R17':('Notificaciones','Eventos configurados y válidos, canales plataforma/correo, preferencias salvo obligatorias justificadas; catálogo obligatorio pendiente. Reintentos hasta tres según HU, convención de intento total por precisar. Historial autorizado y sin bloquear operación principal; SMTP real no verificado.', 'HU-052/066–070; RNF-18; SQL 01','Planificado',['ServicioNotificaciones','PlantillaNotificacion','PreferenciaNotificacion','Notificacion','EnvioNotificacion']),
 'R18':('Reportes y conservación','Reportes como consultas derivadas con filtros, autorización, enmascaramiento y exportación PDF/Excel/CSV neutralizando fórmulas. Preservar auditoría, conversiones, movimientos e instantáneas aunque cambie estado del sujeto; composición no implica borrado físico de evidencia.', 'HU-087–091; RNF-06/13/14; SQL 01–02','Planificado, auditoría parcial implementada',['ServicioReportes','FiltroReporte','ResultadoReporte','EventoAuditoria','CambioEstado','Conversion','MovimientoPuntos']),
}
rules['R02'][4].append('Permiso')
rules['R07']=(rules['R07'][0],rules['R07'][1]+' HU-036 exige saldo no negativo; HU-038 exige motivo obligatorio y rechazar reverso que lo deje negativo. Se conserva esta regla explícita; queda pendiente la interacción con reservas abiertas, no permitir deuda.',rules['R07'][2],rules['R07'][3],rules['R07'][4])
rules['R12']=(rules['R12'][0],rules['R12'][1]+' HU-050 exige generador aleatorio criptográficamente seguro. Quedan pendientes método concreto y custodia, sin rebajar ese requisito.',rules['R12'][2],rules['R12'][3],rules['R12'][4])
rules['R19']=('Recuperación de acceso','Enlace de un solo uso, con huella en vez de token en claro y vencimiento. Al restablecer contraseña revoca sesiones previas. Vigencia actual de treinta minutos es implementación revisada, no política general de notificaciones.', 'HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py','Implementado',['RecuperacionAcceso','Usuario','Sesion'])
for c in C.values():
    c['reglas']=[k for k,v in rules.items() if c['nombre'] in v[4]]
    assert c['reglas'],c['nombre']

def rows(t):return [{c.tag:c.text or '' for c in r} for r in E.parse(O/f'antes-{t}.xml').findall('.//Row')]
obs={r['Object_ID']:r for r in rows('t_object')}; diagrams=rows('t_diagram'); dos=rows('t_diagramobjects')
cus={}
for d in diagrams:
    match=re.match(r'(CU-G\d+) - (.*?) \(Detalle\)',d['Name'])
    if not match:continue
    candidates=[obs[x['Object_ID']] for x in dos if x['Diagram_ID']==d['Diagram_ID'] and obs[x['Object_ID']]['Object_Type']=='UseCase']
    exact=[x for x in candidates if x['Name'].strip().casefold()==match[2].strip().casefold()]
    assert len(exact)==1,(d['Name'],exact)
    cu=exact[0];cus[match[1]]=dict(diagramaId=d['Diagram_ID'],diagramaGuid=d['ea_guid'],nombre=cu['Name'],id=int(cu['Object_ID']),guid=cu['ea_guid'])
# Se usan como punto de partida los vínculos semánticos previos, revisados contra CU reales.
trace=[]
backlog=json.loads((O/'fuentes/backlog.json').read_text(encoding='utf-8'))
byid={x['Work item ID']:x for x in backlog}
hu={re.match(r'HU-\d+',x['Summary'])[0]:x for x in backlog if re.match(r'HU-\d+',x['Summary'])}
for line in (B/'TRAZABILIDAD.md').read_text(encoding='utf-8').splitlines():
    if not re.match(r'\| HU-\d+:',line):continue
    cols=[x.strip() for x in line.strip('|').split('|')]
    key=re.match(r'HU-\d+',cols[0])[0];num=int(key[3:]);cname,op=cols[-1].split('.')
    op=op.removesuffix('()')
    if cname=='ControlAcceso':
        if op in ['registrarCuenta','validarUnicidad','registrarPersonal']:cname='ServicioRegistro'
        elif op in ['identificarRoles','asignarRol','autorizar']:cname='ServicioAutorizacion'
    if num==42:cname,op='InscripcionCapacitacion','emitirCertificado'
    if num in [52,68,70]:cname,op='ServicioNotificaciones',{52:'notificarGanadores',68:'notificarEvento',70:'consultarHistorial'}[num]
    if num==53:cname,op='Sorteo','consultarHistorial'
    if num==65:cname,op='ContenidoInstitucional','decidirAprobacion'
    cuCode=re.search(r'CU-G\d+',cols[-2])[0]
    row=hu[key];parent=byid.get(row['Parent'],{})
    status='Planificado'
    if num in [1,2,6,8,9,10,11,12,14,15]:status='Implementado en alcance vigente; aceptación completa no certificada'
    if num in [2,5,13]:status='Implementado parcialmente'
    if num in [3,4,7]:status='Planificado; no acreditado por la pantalla'
    sigs=[x for x in C[cname]['operaciones'] if x.startswith(op+'(')]
    assert len(sigs)==1,(key,cname,op)
    regs=C[cname]['reglas']
    source='documentacion/product_con_subtareas.csv; Work item ID '+row['Work item ID']
    extra=''
    if num in [1,6,8]:extra='Decisiones posteriores de registro general y cédula diez dígitos sustituyen partes del criterio original; CSV intacto.'
    trace.append(dict(hu=key,titulo=row['Summary'],workItem=row['Work item ID'],tipo=row['Work Type'],padreId=row['Parent'],padre=parent.get('Summary',''),ur=cols[2],rf=cols[3],rnf=cols[4],cuCodigo=cuCode,cu=cus[cuCode],clase=cname,operacion=sigs[0],reglas=regs,atributos='; '.join(C[cname]['atributos']),fuente=source,estado=status,cobertura='Correspondencia de análisis parcial; revisar criterios de aceptación y clases de apoyo',diferencia=extra,enlaceEA='Pendiente de creación y relectura'))
assert len(trace)==91 and len({x['hu'] for x in trace})==91
assert {re.match(r'RF-\d+',x['rf'])[0] for x in trace}=={f'RF-{i:02}' for i in range(1,15)}
trace.sort(key=lambda x:x['hu'])
# Preferir el UseCase específico existente cuando su responsabilidad coincide.
detail_names={
1:'Registrar socio',2:'Consultar datos del perfil',3:'Editar datos de contacto',4:'Cambiar contraseña',5:'Registrar cuenta de personal',6:'Validar condición de socio (padrón de prueba)',7:'Suspender o desactivar cuenta',8:'Prevenir cuentas duplicadas',10:'Validar credenciales',11:'Recuperar contraseña',12:'Verificar cuenta activa y rol',13:'Asignar roles y permisos',15:'Cerrar sesión',16:'Generar código único no secuencial',19:'Compartir código',20:'Verificar duplicados y autorreferidos',21:'Mostrar estado e historial permitido',22:'Filtrar por estado o campaña',23:'Solicitar consentimiento del prospecto',24:'Actualizar estado con responsable y fecha',25:'Registrar condiciones y vigencia',26:'Gestionar estado de campaña',27:'Consultar campañas activas',28:'Segmentar público objetivo',29:'Modificar campaña',30:'Monitorear resultados de campaña',34:'Consultar saldo de puntos',35:'Consultar clasificación',39:'Inscribirse en capacitación',40:'Registrar avance de módulos',41:'Rendir evaluación',42:'Emitir certificado digital',43:'Consultar y descargar certificado',44:'Configurar módulos y criterios de evaluación',45:'Verificar certificado digital',47:'Registrar asistencia a taller',48:'Configurar condiciones de participación',49:'Registrar participación sin duplicados',51:'Consultar resultados de sorteo',52:'Notificar a ganadores',53:'Consultar historial del sorteo',54:'Configurar catálogo de beneficios',56:'Registrar decisión y responsable',57:'Consultar catálogo de beneficios',58:'Consultar historial de canjes',59:'Reservar puntos sin doble débito',60:'Crear o editar contenido',61:'Publicar comunicado',62:'Gestionar materiales educativos',63:'Consultar noticias institucionales',64:'Validar vigencia y permisos',67:'Configurar preferencias de avisos',69:'Consultar bandeja de notificaciones',71:'Guardar juego o reto',72:'Guardar juego o reto',73:'Participar en juego',74:'Registrar resultado validado',75:'Registrar resultado validado',76:'Validar límite de intentos',77:'Definir reglas y límites de intentos',78:'Participar en reto',79:'Publicar en comunidad',80:'Comentar o reaccionar',81:'Reportar publicación',82:'Registrar decisión y motivo',83:'Configurar perfil público',85:'Consultar convenios vigentes',86:'Consultar beneficio vinculado a recompensas',87:'Consultar panel de supervisión',88:'Consultar reporte de referidos y campañas',89:'Consultar reporte de impacto social',90:'Consultar reporte de puntos y recompensas',91:'Exportar reporte PDF o Excel/CSV'}
for t in trace:
    n=int(t['hu'][3:]);t['cuGrupoOriginal']=t['cuCodigo']
    t['correspondenciaCU']='Correspondencia semántica de análisis; no certifica aceptación'
    if n in detail_names:
        found=[x for x in obs.values() if x['Object_Type']=='UseCase' and x['Name'].casefold()==detail_names[n].casefold()]
        assert len(found)==1,(t['hu'],detail_names[n])
        ob=found[0]
        containing=[d for d in diagrams if re.match(r'CU-G\d+ -',d['Name']) and any(x['Diagram_ID']==d['Diagram_ID'] and x['Object_ID']==ob['Object_ID'] for x in dos)]
        chosen=next((d for d in containing if d['Name'].startswith(t['cuCodigo']+' -')),containing[0])
        t['cuCodigo']=re.match(r'CU-G\d+',chosen['Name'])[0]
        t['cu']=dict(diagramaId=chosen['Diagram_ID'],diagramaGuid=chosen['ea_guid'],nombre=ob['Name'],id=int(ob['Object_ID']),guid=ob['ea_guid'])
    if n in [14,31,32,33,36,37,38,46,65,66,68,70,84]:
        t['correspondenciaCU']='Apoyo general: falta CU específico de esta responsabilidad; enlace de análisis, no realización completa'
for c in C.values():
    direct=[t['hu'] for t in trace if t['clase']==c['nombre']]
    # Apoyo explícito: todas las HU del mismo grupo de reglas, no cobertura de aceptación automática.
    support=[t['hu'] for t in trace if set(t['reglas'])&set(c['reglas'])]
    c['huDirectas']=direct;c['huApoyo']=support
    c['fuentes']=[dict(id=k,titulo=rules[k][0],fuente=rules[k][2]) for k in c['reglas']]
    implemented_attrs={
      'Usuario':{'id','cedula','nombres','apellidos','correo','nombreUsuario','telefono','fechaNacimiento','estado','intentosFallidos','bloqueadoHasta'},
      'Socio':{'codigoSocio','validadoEn'},'Rol':{'nombre'},'EntradaPadron':{'cedula','activo'},
      'ConsentimientoCuenta':{'versionPolitica','aceptadoEn'},'Sesion':{'venceEn','ultimoUso','revocadaEn'},
      'RecuperacionAcceso':{'solicitadaEn','venceEn','usadaEn','huellaEnlace'},
      'EventoAuditoria':{'accion','entidad','referencia','fecha','resultado','origenConexion'}}
    c['atributosDetalle']=[]
    for x in c['atributos']:
        assert ':' in x
        name=x.split(':')[0].strip().lstrip('/')
        state='Implementado' if name in implemented_attrs.get(c['nombre'],set()) else 'Propuesta de análisis' if c['estado']=='Propuesta de análisis' or c['nombre'] in implemented_attrs else 'Planificado'
        c['atributosDetalle'].append(dict(firma=x,estado=state,fuente='; '.join(f['fuente'] for f in c['fuentes'])))
    c['operacionesDetalle']=[]
    for op in c['operaciones']:
        name=op.split('(')[0]
        kind='Consulta' if name.startswith(('calcular','consultar','es','esta','tiene','puede','permite','verificar','validarUnicidad','habilita','cumple','admite','coincide','seAlcanza','seCumple','obtener','identificar','contar','generarVistaPublica')) else 'Coordinación' if c['estereotipo']=='ServicioDominio' else 'Cambio de estado'
        implemented_ops={'Usuario':{'consultarPerfil'},'ControlAcceso':{'validarCredenciales','registrarIntentoFallido'},'ServicioRegistro':{'registrarCuenta','validarUnicidad','registrarPersonal'},'ServicioAutorizacion':{'identificarRoles','autorizar'},'ValidacionAdministrativaSocio':{'validarYHabilitar'},'Sesion':{'estaVigente','registrarActividad','cerrar','expirarPorInactividad'},'RecuperacionAcceso':{'esUtilizable','restablecerContrasena'},'EntradaPadron':{'habilitaCondicionSocio'}}
        state='Comportamiento equivalente implementado en servicios' if name in implemented_ops.get(c['nombre'],set()) else 'Propuesta de análisis' if c['estado']=='Propuesta de análisis' else 'Planificado'
        c['operacionesDetalle'].append(dict(firma=op,tipo=kind,fuente='; '.join(f['fuente'] for f in c['fuentes']),estado='Responsabilidad conceptual; '+state))
associations=[]
for i,(a,ma,b,mb,note) in enumerate(R,1):
    assert a in C and b in C,(a,b)
    assert ma in ['0..1','1','0..*','1..*'] and mb in ['0..1','1','0..*','1..*']
    composite=(a,b) in {('Capacitacion','ModuloCapacitacion'),('Pregunta','OpcionPregunta')}
    shared=set(C[a]['reglas'])&set(C[b]['reglas'])
    associations.append(dict(id=f'REL-{i:03}',a=a,ma=ma,b=b,mb=mb,nombre=note,rolA=a[0].lower()+a[1:],rolB=b[0].lower()+b[1:],composicion=composite,justificacion=note+('; pertenencia exclusiva y ciclo de configuración; preservar evidencia histórica antes de retirar' if composite else '; asociación sin propiedad de ciclo de vida'),fuente='; '.join(rules[k][2] for k in sorted(shared or set(C[b]['reglas'])))))
dependencies=[dict(id=f'DEP-{i:03}',a=a,b=b,nombre=n,fuente='; '.join(f['fuente'] for f in C[a]['fuentes'])) for i,(a,b,n) in enumerate(D,1)]
# Vistas limitadas y reutilización de elementos. Las vistas de relaciones muestran vínculos, las fichas conservan todo el detalle.
views=[]
def view(name,names,main=False):views.append(dict(id=f'V-{len(views):02}',nombre=name,clases=names,principal=main))
view('Diagrama de clases de negocio',['Usuario','Socio','CodigoReferido','Referido','Conversion','ActividadValidada','CuentaPuntos','Canje'],True)
view('Identidad y consentimiento',['Usuario','Socio','Rol','ConsentimientoCuenta','EntradaPadron','ServicioRegistro'])
view('Acceso y sesiones',['Usuario','ControlAcceso','Sesion','RecuperacionAcceso','ServicioAutorizacion','Rol','Permiso'])
view('Validación temporal y auditoría',['Usuario','Socio','ValidacionAdministrativaSocio','EntradaPadron','Rol','EventoAuditoria'])
view('Registro y seguimiento de referidos',['Socio','CodigoReferido','Prospecto','Referido','ConsentimientoProspecto','CambioEstado'])
view('Conversión comercial',['Referido','Prospecto','Conversion','Usuario','ActividadValidada','MovimientoPuntos'])
view('Campañas y condiciones reconocidas',['Campana','Segmento','IncentivoCampana','ParticipacionCampana','ReconocimientoIncentivo','ActividadValidada','Socio'])
view('Libro de puntos y reversos',['Socio','CuentaPuntos','MovimientoPuntos','ReglaPuntos','ActividadValidada','ReconocimientoIncentivo'])
view('Niveles y privacidad',['Socio','CuentaPuntos','Nivel','Insignia','InsigniaObtenida','Clasificacion','PerfilPublico'])
view('Capacitaciones y avance',['Socio','Capacitacion','ModuloCapacitacion','MaterialEducativo','InscripcionCapacitacion','ProgresoModulo'])
view('Evaluaciones y certificados',['InscripcionCapacitacion','Evaluacion','IntentoEvaluacion','Pregunta','RespuestaActividad','Certificado'])
view('Talleres y asistencia',['Socio','Taller','InscripcionTaller','Usuario','ActividadValidada'])
view('Sorteos y lista congelada',['Sorteo','ParticipacionSorteo','EvidenciaSorteo','ElegibleCongelado','Socio','Campana'])
view('Premios y resultados verificables',['Sorteo','ParticipacionSorteo','PremioSorteo','ResultadoSorteo','EvidenciaSorteo','Usuario'])
view('Beneficios y canjes',['Socio','Beneficio','Canje','CuentaPuntos','MovimientoPuntos','Usuario','ConvenioBienestar'])
view('Contenido institucional y materiales',['Usuario','ContenidoInstitucional','AprobacionContenido','MaterialEducativo','ModuloCapacitacion'])
view('Notificaciones y entregas',['Usuario','ServicioNotificaciones','PlantillaNotificacion','PreferenciaNotificacion','Notificacion','EnvioNotificacion'])
view('Juegos y respuestas',['Socio','Juego','Partida','Pregunta','OpcionPregunta','RespuestaActividad','ActividadValidada'])
view('Retos y reconocimiento',['Socio','Reto','ProgresoReto','ActividadValidada','ReglaPuntos','CuentaPuntos'])
view('Comunidad y moderación',['Socio','PublicacionComunidad','Comentario','Reaccion','ReporteComunidad','DecisionModeracion','Usuario'])
view('Bienestar y convenios',['ConvenioBienestar','RecursoBienestar','ContenidoInstitucional','Beneficio'])
view('Reportes y filtros',['ServicioReportes','FiltroReporte','ResultadoReporte','Campana','Segmento','Usuario'])
view('Conservación de historiales',['Referido','Campana','Canje','Usuario','CambioEstado','EventoAuditoria'])
# Cada relación/dependencia dispone de al menos una vista, con grupos pequeños adicionales de integración.
for rels in [associations,dependencies]:
    missing=[r for r in rels if not any(r['a'] in v['clases'] and r['b'] in v['clases'] for v in views)]
    while missing:
        first=missing.pop(0);names=list(dict.fromkeys([first['a'],first['b']]))
        group=[first]
        for r in missing[:]:
            union=list(dict.fromkeys(names+[r['a'],r['b']]))
            if len(union)<=6 and (r['a'] in names or r['b'] in names): names=union;group.append(r);missing.remove(r)
        view('Integración '+str(len(views)-22).zfill(2),names)
for v in views:
    v['relaciones']=[r['id'] for r in associations if r['a'] in v['clases'] and r['b'] in v['clases']]
    v['dependencias']=[r['id'] for r in dependencies if r['a'] in v['clases'] and r['b'] in v['clases']]
model=dict(clases=list(C.values()),enumeraciones=[dict(nombre=n,valores=v,fuente=enum_sources[n]) for n,v in enums.items()],asociaciones=associations,dependencias=dependencies,vistas=views,reglas=[dict(id=k,titulo=v[0],texto=v[1],fuente=v[2],estado=v[3],clases=v[4]) for k,v in rules.items()],trazabilidad=trace,casosUso=cus)
(O/'modelo-revisado.json').write_text(json.dumps(model,ensure_ascii=False,indent=2),encoding='utf-8')
# Documentación completa nueva, preservando antecedentes.
catalog=['# Catálogo revisado de clases de análisis\n','Las firmas son responsabilidades conceptuales. Estado indica evidencia de comportamiento, no aprobación del diseño. Tipos Texto/Entero/Decimal/Booleano/Fecha/FechaHora, enumeraciones y conceptos. Coleccion y Conjunto indican multiplicidad de valores. Texto en entrada clave es transitorio y nunca atributo persistido. Los servicios no tienen atributos ficticios.\n']
for c in C.values():
    catalog += [f"## {c['nombre']}\n",f"Dominio: {c['modulo']}. Estereotipo: {c['estereotipo']}. Estado: **{c['estado']}**.\n",c['nota']+'\n','```text']
    catalog += ['- '+x for x in c['atributos']]+['+ '+x for x in c['operaciones']]+['```','Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.' if not c['operaciones'] else '']
    catalog += [f"- Atributo `{a['firma']}` — {a['estado']}; fuente: {a['fuente']}." for a in c['atributosDetalle']]
    catalog += ['Reglas: '+', '.join(c['reglas'])+'. HU directas: '+(', '.join(c['huDirectas']) or 'concepto de apoyo')+'.','Fuentes: '+'; '.join(f['fuente'] for f in c['fuentes'])+'.\n']
    for op in c['operacionesDetalle']:catalog.append(f"- `{op['firma']}` — {op['tipo']}; {op['estado']}. Fuente: {op['fuente']}.")
catalog+=['\n## Enumeraciones\n']+[f"- {n}: {', '.join(v)}. Fuente: {enum_sources[n]}." for n,v in enums.items()]
(O/'CATALOGO-REVISADO.md').write_text('\n'.join(catalog),encoding='utf-8')
lines=['# Relaciones y dependencias revisadas\n','Las multiplicidades junto a A cuentan cuántos A corresponden a un B; las de B, cuántos B corresponden a un A. Las asociaciones derivadas o de consulta se señalan en su significado; no afirman persistencia física.\n','| ID | A | mult A | B | mult B | Tipo | Significado y justificación | Fuente |','|---|---|---|---|---|---|---|---|']
for r in associations:lines.append(f"| {r['id']} | {r['a']} | {r['ma']} | {r['b']} | {r['mb']} | {'Composición' if r['composicion'] else 'Asociación'} | {r['justificacion']} | {r['fuente']} |")
lines+=['\n## Dependencias de coordinación y consulta\n','| ID | Cliente | Proveedor | Responsabilidad | Fuente |','|---|---|---|---|---|']+[f"| {r['id']} | {r['a']} | {r['b']} | {r['nombre']} | {r['fuente']} |" for r in dependencies]
(O/'RELACIONES.md').write_text('\n'.join(lines),encoding='utf-8')
lines=['# Reglas y decisiones de la entrega\n','No se aprueba una política por incluirla en el modelo. Las propuestas siguen explícitamente pendientes.\n']
for k,v in rules.items():lines += [f'## {k} {v[0]}\n',v[1],f'\nEstado: {v[3]}. Fuente: {v[2]}.\n']
lines+=['## Diferencias respecto de la propuesta inicial\n','- Registro y autorización se separan de ControlAcceso. Los contadores se conservan en Usuario; los servicios carecen de estado artificial.','- ValidacionAdministrativaSocio pasa a servicio sin registro propio ficticio; su evidencia está en EventoAuditoria.','- Consentimientos explicitan aceptación; finalidad explícita continúa propuesta donde falta persistencia.','- Se agregan ElegibleCongelado y ReconocimientoIncentivo para explicar evidencia e irreversibilidad de reconocimientos.','- Se permite más de una Evaluacion por capacitación, conforme SQL; no se aprueba silenciosamente una única evaluación final.','- Emitir certificado es responsabilidad de InscripcionCapacitacion; la decisión de aprobación institucional pertenece a ContenidoInstitucional.','- Se corrigen HU-052/053/068/070 para distinguir envío/coordinación, consulta de historial y comprobación de integridad.','- Datos institucionales para segmentación se retiran de Socio hasta definir fuente; no se presume acceso al core.','- Se mantienen campos configurables como Texto cuando no hay catálogo de estados aprobado; no se inventan enumeraciones.','\n## Pendientes conservados\n']
prior=(B/'DECISIONES-Y-REGLAS.md').read_text(encoding='utf-8')
lines.append(prior[prior.index('| P01'):prior.index('## Convenciones UML')])
lines+=['| P16 | Límites por período y reversos | Precisar unidad de límite, ventana/calendario, zona horaria, si reversar restituye cupo y qué hacer si puntos ya se gastaron. |','| P17 | Versionado de materiales, evaluaciones e incentivos | Definir retiro sin alterar intentos, certificados ni reconocimientos previos. |','| P18 | Evidencia de sorteo | Definir contenido canónico, método aprobado, custodia y política de suplentes; no se impone tecnología criptográfica concreta. |']
(O/'REGLAS-Y-PENDIENTES.md').write_text('\n'.join(lines),encoding='utf-8')
with (O/'TRAZABILIDAD.csv').open('w',encoding='utf-8-sig',newline='') as f:
    keys=['HU','WorkItem','Tipo','PadreID','HistoriaPadre','UR','RF','RNF','CU','CU_ID','CU_GUID','CU_nombre','Clase','Regla','Atributos','Operacion','Fuente','Estado','Cobertura','Diferencia','EnlaceEA']
    w=csv.writer(f);w.writerow(keys)
    for t in trace:w.writerow([t['hu'],t['workItem'],t['tipo'],t['padreId'],t['padre'],t['ur'],t['rf'],t['rnf'],t['cuCodigo'],t['cu']['id'],t['cu']['guid'],t['cu']['nombre'],t['clase'],','.join(t['reglas']),t['atributos'],t['operacion'],t['fuente'],t['estado'],t['cobertura'],t['diferencia'],t['enlaceEA']])
print(json.dumps({'clases':len(C),'asociaciones':len(R),'dependencias':len(D),'enumeraciones':len(enums),'vistas':len(views),'HU':len(trace),'CU':len(cus)},ensure_ascii=False))
