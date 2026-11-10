"""Genera documentación de análisis; no abre ni modifica Enterprise Architect."""
from pathlib import Path
import csv
import json
import re

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]

# módulo | clase | atributos conceptuales | operaciones propuestas | responsabilidad y fuente
DATOS = """
Identidad|Usuario|id: Identificador; cedula: Texto; nombres: Texto; apellidos: Texto; correo: Texto; nombreUsuario: Texto; telefono: Texto; fechaNacimiento: Fecha; estado: EstadoCuenta; foto: Recurso [0..1]|calcularEdad(fecha: Fecha): Entero; actualizarContacto(correo: Texto, telefono: Texto, foto: Recurso [0..1]): Booleano; cambiarContrasena(actual: Secreto, nueva: Secreto): Booleano; cambiarEstado(estado: EstadoCuenta, motivo: Texto, responsable: Usuario): Booleano|Titular de la cuenta. Campos principales implementados; foto y gestión completa de estado/contacto son planificados. HU-001–008; models/usuario.py. Secreto es un parámetro transitorio, nunca un atributo público ni texto almacenado.
Identidad|Socio|codigoSocio: Texto; validadoEn: FechaHora; tipoSocio: Texto [0..1]; agencia: Texto [0..1]; productosSegmentacion: Conjunto<Texto>|esElegibleParaParticipar(fecha: FechaHora): Booleano|Condición cooperativa asociada a una cuenta. Código y validación implementados; datos de segmentación propuestos y pendientes de fuente P05. models/socio.py; HU-028.
Identidad|Rol|nombre: Texto|habilita(permiso: Permiso): Booleano|Conjunto de autorizaciones. Roles múltiples implementados; administración completa de permisos planificada. HU-012–014.
Identidad|Permiso|codigo: Texto; descripcion: Texto|permiteAccion(accion: Texto): Booleano|Capacidad autorizada; diseño SQL permiso/rol_permiso y HU-013. No presupone administración operativa completa.
Identidad|ConsentimientoCuenta|versionPolitica: Texto; finalidad: Texto; aceptadoEn: FechaHora|acreditaAceptacion(version: Texto): Booleano|Evidencia de aceptación de la cuenta. Fecha y versión implementadas; finalidad explícita propuesta. HU-001.
Identidad|EntradaPadron|cedula: Texto; activo: Booleano|habilitaCondicionSocio(): Booleano|Registro de prueba independiente de cuentas. No encontrado es resultado de consulta, no una fila ficticia. HU-006; models/padron.py.
Identidad|ValidacionAdministrativaSocio|fecha: FechaHora; confirmacionExpresa: Booleano; resultado: Texto|validarYHabilitar(cuenta: Usuario, administrador: Usuario): Socio|Concepto propuesto para explicar proceso manual temporal ya implementado por servicio y auditoría; no afirma tabla propia. No acredita puntos de referidos.
Seguridad|Sesion|iniciadaEn: FechaHora; venceEn: FechaHora; ultimoUso: FechaHora [0..1]; revocadaEn: FechaHora [0..1]|estaVigente(ahora: FechaHora): Booleano; registrarActividad(ahora: FechaHora): Booleano; cerrar(ahora: FechaHora): Booleano; expirarPorInactividad(ahora: FechaHora): Booleano|Sesión revocable implementada; iniciadaEn es atributo conceptual propuesto. No almacena JWT en claro. HU-009/HU-015; models/sesion.py.
Seguridad|RecuperacionAcceso|solicitadaEn: FechaHora; venceEn: FechaHora; usadaEn: FechaHora [0..1]; huellaEnlace: Texto|esUtilizable(ahora: FechaHora): Booleano; restablecerContrasena(nueva: Secreto): Booleano|Enlace de un uso, modelo TokenRecuperacion y servicio existentes. HU-011. Vigencia actual 30 minutos en servicio; no extender a todos los consentimientos.
Seguridad|ControlAcceso|intentosFallidos: Entero; bloqueadoHasta: FechaHora [0..1]|validarCredenciales(identificador: Texto, clave: Secreto): Sesion; registrarIntentoFallido(ahora: FechaHora): Booleano; autorizar(usuario: Usuario, accion: Texto, recurso: Referencia): Booleano|Responsabilidad conceptual agrupada de servicios existentes; estado de fallos físicamente en Usuario. HU-009/HU-010/HU-014. Permisos dinámicos completos no se presuponen implementados.
Auditoria|EventoAuditoria|accion: Texto; entidad: Texto; referencia: Texto [0..1]; fecha: FechaHora; resultado: Texto; origenConexion: Texto [0..1]| |Registro inmutable; actor opcional para acciones anónimas. Implementado para eventos concretos, no interfaz general completa. models/auditoria.py; RNF-06.
Auditoria|CambioEstado|entidad: Texto; referencia: Texto; anterior: Texto [0..1]; nuevo: Texto; fecha: FechaHora; motivo: Texto [0..1]| |Historial inmutable compartido por referido, campaña y canje. Diseño SQL historial_estado; motivo/observación propuestos por HU-024/HU-056.
Referidos|CodigoReferido|valor: Texto; activo: Booleano|esValido(): Booleano; generarEnlace(base: Texto): Texto|Identificador comercial no secuencial distinto de codigoSocio. SQL permite historial y un código activo por socio. HU-016/HU-019; módulo planificado.
Referidos|Prospecto|id: Identificador; nombres: Texto; huellaIdentificacion: Texto [0..1]; telefono: Texto [0..1]; correo: Texto [0..1]; productoInteres: Texto [0..1]|coincideCon(persona: Referencia): Booleano; tieneContactoUtilizable(): Booleano|Persona recomendada sin cuenta obligatoria. HU-017/HU-020. Al menos un contacto; datos mínimos de comparación pendientes de precisar.
Referidos|ConsentimientoProspecto|finalidad: Texto; versionPolitica: Texto; solicitadoEn: FechaHora; limiteConfirmacion: FechaHora; aceptadoEn: FechaHora [0..1]|confirmar(ahora: FechaHora): Booleano; estaConfirmado(): Booleano; plazoVencido(ahora: FechaHora): Booleano|Objeto propuesto de evidencia de consentimiento para un referido; SQL 02 solo cubre parte de las fechas. HU-023; no reutiliza ConsentimientoCuenta.
Referidos|Referido|id: Identificador; creadoEn: FechaHora; estado: EstadoReferido|validarRegistro(): Booleano; confirmarConsentimiento(ahora: FechaHora): Booleano; iniciarSeguimiento(responsable: Usuario): Booleano; rechazar(motivo: Texto, responsable: Usuario): Booleano; expirar(ahora: FechaHora): Booleano; confirmarConversion(tipo: TipoConversion, evidencia: Texto, responsable: Usuario): Conversion|Vínculo de recomendación. Valida código, autorreferido, padrón, duplicados y transición; conserva historial. HU-017–024; módulo planificado.
Referidos|Conversion|tipo: TipoConversion; validadaEn: FechaHora; evidenciaPrueba: Texto; claveOrigen: Texto|esReconocible(): Booleano|Hecho comercial validado una vez por prospecto; dispara reconocimiento único. SQL conversion y HU-018; evidencia detallada propuesta.
Campanas|Campana|nombre: Texto; tipo: Texto; objetivo: Texto; meta: Entero; unidadMeta: Texto; inicio: Fecha; fin: Fecha; estado: EstadoCampana|activar(fecha: Fecha): Booleano; suspender(motivo: Texto): Booleano; finalizar(fecha: Fecha): Booleano; admiteParticipacion(socio: Socio, fecha: Fecha): Booleano; modificarCondiciones(cambios: Condiciones, responsable: Usuario): Booleano; calcularTasaConversion(): Decimal; calcularAvanceMeta(): Decimal|Organiza objetivos, vigencia e incentivos. HU-025–030; planificado. unidadMeta propuesta pendiente de definición.
Campanas|Segmento|nombre: Texto; criteriosAutorizados: Conjunto<Criterio>|incluye(socio: Socio, fecha: Fecha): Booleano; contarElegibles(socios: Coleccion<Socio>): Entero|Selecciona por edad, tipo de socio, producto y agencia; combinación de criterios pendiente P05. HU-028.
Campanas|IncentivoCampana|tipo: Texto; cantidad: Entero; condiciones: Texto; version: Texto; vigenteDesde: Fecha; vigenteHasta: Fecha [0..1]|correspondeA(actividad: ActividadValidada): Booleano|Descomposición conceptual propuesta de incentivos de campaña (SQL los guarda como texto). Puntos o participaciones, sin efecto retroactivo. HU-025/HU-029.
Campanas|ParticipacionCampana|registradaEn: FechaHora; validadaEn: FechaHora [0..1]; versionCondiciones: Texto|validarElegibilidad(fecha: Fecha): Booleano|Registro propuesto de participación validada para monitoreo y CU-G06. No se exige inscripción manual universal ni se afirma tabla existente.
Gamificacion|ActividadValidada|tipo: Texto; referenciaOrigen: Texto; fecha: FechaHora; validada: Booleano|esReconocible(): Booleano|Objeto de valor propuesto de enlace entre hechos de negocio y reconocimiento; no duplica sus registros operativos. HU-032/HU-049/HU-075/HU-078.
Gamificacion|ReglaPuntos|tipoActividad: Texto; puntos: Entero; limitePeriodo: Entero [0..1]; periodo: Texto [0..1]; vigenteDesde: Fecha; vigenteHasta: Fecha [0..1]; version: Texto|calcularPuntos(actividad: ActividadValidada, acumuladoPeriodo: Entero): Entero; estaVigente(fecha: Fecha): Booleano|Regla sin efecto retroactivo. HU-031/HU-032; límites y versión no completos en SQL.
Gamificacion|CuentaPuntos|/saldoContable: Entero; /saldoReservado: Entero; /saldoDisponible: Entero|calcularSaldoContable(): Entero; calcularSaldoReservado(): Entero; calcularSaldoDisponible(): Entero; acreditar(actividad: ActividadValidada, regla: ReglaPuntos): MovimientoPuntos; reservar(canje: Canje, cantidad: Entero): MovimientoPuntos; confirmarDescuento(canje: Canje): MovimientoPuntos; liberarReserva(canje: Canje): MovimientoPuntos; revertir(original: MovimientoPuntos, motivo: Texto): MovimientoPuntos|Agregado conceptual propuesto, derivado del libro; no tabla de saldo. HU-032/HU-034/HU-036/HU-038/HU-059. Semántica de reserva según propuesta R6.
Gamificacion|MovimientoPuntos|id: Identificador; tipo: TipoMovimiento; cantidad: Entero; fecha: FechaHora; claveIdempotencia: Texto; motivo: Texto [0..1]| |Registro inmutable con cantidad positiva y signo semántico según tipo. Origen, beneficiario y reverso trazables; HU-036/HU-038/HU-059.
Gamificacion|Nivel|nombre: Texto; umbralPuntos: Entero|seAlcanzaCon(puntosBase: Entero): Booleano|Umbrales únicos. Base de puntos y descensos pendientes P06. HU-033/HU-037.
Gamificacion|Insignia|nombre: Texto; icono: Recurso; criterio: Texto|seCumplePara(socio: Socio, actividades: Coleccion<ActividadValidada>): Booleano|Define logro; icono requerido por HU-037 aunque no completo en SQL. HU-033/HU-037.
Gamificacion|InsigniaObtenida|obtenidaEn: FechaHora| |Registro único socio–insignia; no borrar al cambiar criterios. HU-033; SQL socio_insignia.
Gamificacion|Clasificacion|desde: Fecha; hasta: Fecha; criterioOrden: Texto|calcularPosicion(socio: Socio): Entero; generarVistaPublica(): Coleccion<PosicionPublica>|Consulta derivada con alias y exclusión pública. No necesita tabla propia. Criterio y empates pendientes P06. HU-035.
Formacion|Capacitacion|titulo: Texto; descripcion: Texto; duracionHoras: Decimal; requisitos: Texto; estado: Texto|puedeInscribirse(socio: Socio): Booleano; publicar(responsable: Usuario): Booleano; calcularTasaAprobacion(): Decimal|Oferta de educación financiera. Varias propiedades derivadas de HU aún sin persistencia completa. HU-039/HU-044.
Formacion|ModuloCapacitacion|titulo: Texto; orden: Entero; obligatorio: Booleano|estaCompletado(progreso: ProgresoModulo): Booleano|Corresponde a unidad del SQL; obligatoriedad propuesta para explicar avance. HU-040/HU-044.
Formacion|InscripcionCapacitacion|fecha: FechaHora; estado: Texto; /porcentajeAvance: Decimal|completarModulo(modulo: ModuloCapacitacion): ProgresoModulo; calcularAvance(): Decimal; puedeRendir(evaluacion: Evaluacion): Booleano|Vínculo único socio–capacitación. Fórmula y acceso a evaluación por definir P06. HU-039–041.
Formacion|ProgresoModulo|porcentaje: Decimal; completadoEn: FechaHora [0..1]|registrarFinalizacion(ahora: FechaHora): Booleano|Seguimiento por inscripción y módulo; entre 0 y 100. HU-040; SQL progreso.
Formacion|Evaluacion|notaMinima: Decimal; maximoIntentos: Entero; reglasCalificacion: Texto|permiteNuevoIntento(inscripcion: InscripcionCapacitacion): Booleano; calcularNota(respuestas: Coleccion<RespuestaActividad>): Decimal|Calificación en servidor y límite. HU-041/HU-044; reglas y máximo no completos en SQL.
Formacion|IntentoEvaluacion|numero: Entero; iniciadoEn: FechaHora; finalizadoEn: FechaHora [0..1]; nota: Decimal [0..1]; aprobado: Booleano [0..1]|calificar(): Decimal; alcanzaAprobacion(): Booleano|Intento asociado a inscripción y evaluación; aprobación válida genera actividad única. HU-041.
Formacion|Certificado|codigoVerificacion: Texto; emitidoEn: FechaHora; documento: Recurso|emitir(inscripcion: InscripcionCapacitacion): Booleano; verificarAutenticidad(codigo: Texto): Booleano; obtenerDocumento(solicitante: Usuario): Recurso|Solo tras aprobar, código único no secuencial y acceso al documento autorizado. HU-042/HU-043/HU-045.
Formacion|Taller|titulo: Texto; modalidad: Texto; lugarOEnlace: Texto; fecha: FechaHora; cupo: Entero; estado: Texto|calcularCuposDisponibles(): Entero; admiteInscripcion(socio: Socio): Booleano|Actividad con aforo; sin integración de videoconferencia inventada. HU-046/HU-047.
Formacion|InscripcionTaller|inscritaEn: FechaHora; asistio: Booleano; asistenciaRegistradaEn: FechaHora [0..1]|registrarAsistencia(responsable: Usuario): Booleano; habilitaReconocimiento(): Booleano|Representa inscripción y asistencia (tabla asistencia_taller). Una por socio–taller, premio una vez. HU-047.
Preguntas|Pregunta|enunciado: Texto; tipo: Texto; criterioCorreccion: Texto|evaluar(respuesta: RespuestaActividad): Decimal|Propietario exclusivo evaluación XOR juego según SQL 02. Parejas para emparejar pendientes P08. HU-041/HU-072.
Preguntas|OpcionPregunta|texto: Texto; correcta: Booleano| |Alternativa de pregunta. SQL solo permite una correcta; no extrapolar a todos los juegos. HU-041/HU-072.
Preguntas|RespuestaActividad|contenido: Texto; respondidaEn: FechaHora| |Objeto de valor propuesto, propiedad exclusiva de un intento de evaluación o una partida; referencia la pregunta respondida. HU-041/HU-074.
Sorteos|Sorteo|nombre: Texto; fecha: FechaHora; condiciones: Texto; numeroGanadores: Entero; numeroSuplentes: Entero; estado: Texto|verificarElegibilidad(socio: Socio): Booleano; congelarElegibles(): EvidenciaSorteo; ejecutar(responsable: Usuario): Coleccion<ResultadoSorteo>; publicarResultados(): Booleano|Ejecución única con lista congelada y selección segura. HU-048–053; campos de evidencia son propuesta, no funcionalidad existente.
Sorteos|ParticipacionSorteo|registradaEn: FechaHora; claveOrigen: Texto; elegibleAlCierre: Booleano|validarOrigen(): Booleano|Participación por socio, sorteo y actividad; sin duplicados no permitidos. HU-049.
Sorteos|PremioSorteo|descripcion: Texto; posicion: Entero; condicionesReclamo: Texto| |Premio configurado; SQL 02 premio_sorteo. HU-048/HU-052.
Sorteos|EvidenciaSorteo|listaCongelada: Coleccion<Texto>; hashLista: Texto; congeladaEn: FechaHora; ejecutadoEn: FechaHora [0..1]; referenciaMetodoSeleccion: Texto|verificarIntegridad(): Booleano|Registro propuesto para lista congelada, proceso y resultado; conservar inmutable tras ejecución. HU-050/HU-053.
Sorteos|ResultadoSorteo|posicion: Entero; esSuplente: Booleano; registradoEn: FechaHora|obtenerDatosPublicos(): DatosEnmascarados|Vincula participación de ese mismo sorteo; premio opcional para suplente. HU-050/HU-051; SQL ganador.
Recompensas|Beneficio|nombre: Texto; descripcion: Texto; costoPuntos: Entero; stock: Entero [0..1]; condiciones: Texto; inicio: Fecha [0..1]; fin: Fecha [0..1]; activo: Booleano|estaDisponible(fecha: Fecha): Booleano; cumpleCondiciones(socio: Socio): Booleano; calcularStockDisponible(): Entero|Stock nulo puede representar ilimitado según SQL; política de costo cero pendiente P02. Convenio vencido bloquea disponibilidad. HU-054/HU-057/HU-086.
Recompensas|Canje|solicitadoEn: FechaHora; puntosComprometidos: Entero; condicionesReconocidas: Texto; estado: EstadoCanje; entregadoEn: FechaHora [0..1]|solicitar(): Booleano; aprobar(responsable: Usuario): Booleano; rechazar(motivo: Texto, responsable: Usuario): Booleano; registrarEntrega(responsable: Usuario): Booleano|Coordina reserva, descuento/liberación y stock con CuentaPuntos; evidencia de condiciones propuesta. HU-055/HU-056/HU-058/HU-059.
Contenidos|ContenidoInstitucional|titulo: Texto; cuerpo: Texto; categoria: Texto; tipo: Texto; estado: Texto; desde: Fecha [0..1]; hasta: Fecha [0..1]; requiereAprobacion: Booleano|solicitarAprobacion(): Booleano; publicar(responsable: Usuario): Booleano; retirar(motivo: Texto): Booleano; esVisible(fecha: Fecha): Booleano|Noticias, comunicados y multimedia; distinta de publicación comunitaria. HU-060/HU-061/HU-063/HU-064/HU-065.
Contenidos|AprobacionContenido|decididaEn: FechaHora; decision: Texto; observacion: Texto [0..1]|aprobar(responsable: Usuario): Booleano|Evidencia propuesta de aprobación opcional por responsable designado; no tabla existente confirmada. HU-065.
Contenidos|MaterialEducativo|titulo: Texto; categoria: Texto; formato: Texto; tamanoBytes: Entero; recurso: Recurso|esAdmisible(): Booleano; puedeReutilizarse(): Booleano|Repositorio reutilizable; archivo máximo 10 MB y tipos autorizados. SQL material/contenido; HU-062/HU-044.
Notificaciones|PlantillaNotificacion|titulo: Texto; cuerpo: Texto; evento: Texto; canal: Canal; obligatoria: Booleano|prepararMensaje(datos: DatosEvento): Texto|Plantilla por evento y canal; naturaleza obligatoria propuesta pendiente P14. HU-066.
Notificaciones|PreferenciaNotificacion|evento: Texto; canal: Canal; habilitada: Booleano|permiteEnvio(obligatoria: Booleano): Booleano|No puede desactivar comunicación obligatoria. HU-067; SQL preferencia_notificacion.
Notificaciones|Notificacion|evento: Texto; creadaEn: FechaHora; leidaEn: FechaHora [0..1]; titulo: Texto; mensaje: Texto|marcarLeida(destinatario: Usuario): Booleano|Aviso de bandeja y sus envíos; separación conceptual propuesta respecto de fila SQL por canal. HU-068/HU-069.
Notificaciones|EnvioNotificacion|canal: Canal; estado: Texto; intentos: Entero; enviadaEn: FechaHora [0..1]; ultimoError: Texto [0..1]|programar(): Booleano; puedeReintentarse(): Booleano; registrarResultado(exito: Booleano, fecha: FechaHora): Booleano|Historial de entrega por canal sin bloquear operación principal; hasta tres reintentos, número total de intentos requiere convención explícita. HU-068/HU-070.
JuegosRetos|Juego|nombre: Texto; instrucciones: Texto; tipo: TipoJuego; activo: Booleano; maximoIntentos: Entero; criteriosPuntuacion: Texto; criteriosFinalizacion: Texto|admitePartida(socio: Socio): Booleano; calcularIntentosRestantes(socio: Socio): Entero; activar(): Booleano; desactivar(): Booleano|Juego educativo configurable; criterios derivados de HU pendientes de persistencia completa. HU-071/HU-072/HU-073/HU-076.
JuegosRetos|Partida|iniciadaEn: FechaHora; finalizadaEn: FechaHora [0..1]; puntuacion: Decimal [0..1]; resultadoValido: Booleano|calcularResultado(): Decimal; finalizar(): Booleano; habilitaReconocimiento(): Booleano|Resultado calculado en servidor; no aceptar puntaje final del cliente. HU-074/HU-075.
JuegosRetos|Reto|objetivo: Texto; tipoActividad: Texto; meta: Entero; inicio: Fecha; fin: Fecha; recompensa: Entero|estaVigente(fecha: Fecha): Booleano; cumpleObjetivo(progreso: ProgresoReto): Booleano|Tipo de actividad y cantidad medible; recompensa por regla vigente. HU-077.
JuegosRetos|ProgresoReto|avance: Entero; completadoEn: FechaHora [0..1]; recompensaReconocida: Booleano|incorporarActividad(actividad: ActividadValidada): Booleano; calcularPorcentaje(): Decimal; reconocerCumplimiento(fecha: Fecha): Booleano|Una recompensa por socio–reto; excluir duplicación de actividad. HU-078.
Comunidad|PerfilPublico|alias: Texto; camposVisibles: Conjunto<Texto>; participaClasificacionPublica: Booleano|definirPrivacidad(campos: Conjunto<Texto>): Booleano; obtenerDatosPublicos(): DatosPublicos|Información personal oculta por defecto; vista propia de clasificación incluso excluido de pública. HU-083/HU-035.
Comunidad|PublicacionComunidad|texto: Texto; imagenes: Coleccion<Recurso>; creadaEn: FechaHora; estadoModeracion: Texto|admiteInteraccion(): Booleano; publicar(autor: Socio): Booleano|Solo socios autenticados; imágenes autorizadas hasta 10 MB. HU-079/HU-080.
Comunidad|Comentario|texto: Texto; creadoEn: FechaHora; estadoModeracion: Texto|puedeMostrarse(): Booleano|Asociado a publicación y socio; contenido oculto no admite interacción. HU-080.
Comunidad|Reaccion|tipo: Texto; fecha: FechaHora| |Una reacción por socio–publicación según SQL; regla de cambio pendiente si se amplía. HU-080.
Comunidad|ReporteComunidad|motivo: Texto; fecha: FechaHora; estado: Texto|enviarAModeracion(): Booleano|Reporte de publicación o comentario, exclusivamente uno. HU-081; clase propuesta sin tabla equivalente confirmada.
Comunidad|DecisionModeracion|accion: Texto; motivo: Texto; fecha: FechaHora; suspensionHasta: FechaHora [0..1]|aplicar(responsable: Usuario): Booleano|Oculta/elimina contenido o suspende temporalmente con motivo; alcance y plazo pendientes P14. HU-082.
Bienestar|ConvenioBienestar|proveedor: Texto; descripcion: Texto; beneficioDescriptivo: Texto; condiciones: Texto; inicio: Fecha [0..1]; fin: Fecha [0..1]|estaVigente(fecha: Fecha): Booleano; habilitaBeneficio(fecha: Fecha): Booleano|Convenio informativo, sin datos clínicos de socios. HU-084/HU-085/HU-086.
Bienestar|RecursoBienestar|titulo: Texto; categoria: Texto|esVisible(fecha: Fecha): Booleano|Vincula contenido institucional y opcionalmente convenio. HU-085; SQL recurso_bienestar.
Reportes|ServicioReportes| |generarSupervision(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte; generarReferidosCampanas(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte; generarImpactoSocial(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte; generarGamificacion(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte; exportar(resultado: ResultadoReporte, formato: Texto, solicitante: Usuario): Recurso|Servicio de dominio propuesto para consultas y exportaciones según rol; sin atributos artificiales. HU-087–091.
Reportes|FiltroReporte|desde: Fecha [0..1]; hasta: Fecha [0..1]; campana: Referencia [0..1]; segmento: Referencia [0..1]; estado: Texto [0..1]|esValido(): Booleano|Objeto de valor propuesto, registra filtros aplicados sin datos técnicos del framework. HU-088–091.
Reportes|ResultadoReporte|tipo: Texto; generadoEn: FechaHora; indicadores: Coleccion<Indicador>; datosEnmascarados: Booleano| |Objeto de valor propuesto de salida; conserva fecha y filtros. HU-087–091. No obliga a persistir cada consulta.
"""

CLASES = []
for linea in DATOS.strip().splitlines():
    modulo, nombre, atributos, operaciones, nota = [x.strip() for x in linea.split('|')]
    CLASES.append(dict(modulo=modulo, nombre=nombre,
                       atributos=[x.strip() for x in atributos.split(';') if x.strip()],
                       operaciones=[x.strip() for x in operaciones.split(';') if x.strip()], nota=nota))
NOMBRES = {c['nombre'] for c in CLASES}

# extremo A | multiplicidad A | extremo B | multiplicidad B | significado
# La multiplicidad A indica cuántos A corresponden a un B y viceversa.
RELACIONES = """
Usuario|1|Socio|0..1|cuenta de la condición de socio
Usuario|0..*|Rol|0..*|roles asignados, sin herencia
Rol|0..*|Permiso|0..*|capacidades concedidas
Usuario|1|ConsentimientoCuenta|1..*|aceptaciones versionadas de la cuenta
Usuario|1|Sesion|0..*|sesiones de la cuenta
Usuario|1|RecuperacionAcceso|0..*|solicitudes de recuperación
Usuario|1|ControlAcceso|1|política conceptual y estado de intentos asociado
Usuario|0..1|EventoAuditoria|0..*|actor de evento; anónimo permitido
Usuario|0..1|CambioEstado|0..*|responsable del cambio; sistema permitido
Usuario|1|ValidacionAdministrativaSocio|0..1|cuenta destinataria validada exitosamente
Usuario|1|ValidacionAdministrativaSocio|0..*|administrador que confirma la validación
Socio|1|CodigoReferido|0..*|códigos históricos; como máximo uno activo
CodigoReferido|1|Referido|0..*|código utilizado al registrar
Prospecto|1|Referido|0..*|historial; a lo sumo un referido activo
Referido|1|ConsentimientoProspecto|0..*|solicitudes y evidencia versionada; a lo sumo una confirmación vigente
Referido|1|Conversion|0..1|hecho de conversión; también único por prospecto
Usuario|1|Conversion|0..*|responsable que valida evidencia comercial
Campana|0..1|Referido|0..*|campaña cuando corresponde
Usuario|1|Campana|0..*|creador autorizado
Campana|0..*|Segmento|0..*|público objetivo
Campana|1|IncentivoCampana|0..*|condiciones de reconocimiento por versión
Campana|1|ParticipacionCampana|0..*|participaciones para monitoreo
Socio|1|ParticipacionCampana|0..*|participante validado
Socio|1|CuentaPuntos|1|cuenta conceptual de puntos
CuentaPuntos|1|MovimientoPuntos|0..*|libro inmutable del socio
ReglaPuntos|0..1|MovimientoPuntos|0..*|regla aplicada cuando hay acreditación
ActividadValidada|0..1|MovimientoPuntos|0..*|origen de reconocimiento; canjes/reversos usan sus enlaces específicos
Socio|1|ActividadValidada|0..*|beneficiario del hecho reconocido
MovimientoPuntos|0..1|MovimientoPuntos|0..*|original del reverso; validar no exceder importe reversible
CuentaPuntos|0..*|Nivel|0..1|nivel calculado, base pendiente de política
Socio|1|InsigniaObtenida|0..*|logros propios
Insignia|1|InsigniaObtenida|0..*|tipo de logro obtenido una vez por socio
Socio|1|PerfilPublico|0..1|privacidad y alias; valores seguros por defecto al faltar
Capacitacion|1|ModuloCapacitacion|1..*|pertenencia exclusiva; composición conceptual
ModuloCapacitacion|0..*|MaterialEducativo|0..*|material reutilizable
Socio|1|InscripcionCapacitacion|0..*|inscrito, único por capacitación
Capacitacion|1|InscripcionCapacitacion|0..*|oferta elegida
InscripcionCapacitacion|1|ProgresoModulo|0..*|avance de la persona
ModuloCapacitacion|1|ProgresoModulo|0..*|unidad completada; pertenece a la misma capacitación
Capacitacion|1|Evaluacion|0..1|evaluación final propuesta; cardinalidad por validar con política formativa
InscripcionCapacitacion|1|IntentoEvaluacion|0..*|intentos del inscrito
Evaluacion|1|IntentoEvaluacion|0..*|evaluación rendida
InscripcionCapacitacion|1|Certificado|0..1|certificado tras aprobación
Evaluacion|0..1|Pregunta|0..*|propietario exclusivo XOR Juego
Juego|0..1|Pregunta|0..*|propietario exclusivo XOR Evaluacion
Pregunta|1|OpcionPregunta|0..*|alternativas exclusivas; composición conceptual
Pregunta|1|RespuestaActividad|0..*|pregunta respondida
IntentoEvaluacion|0..1|RespuestaActividad|0..*|propietario de respuesta XOR Partida
Partida|0..1|RespuestaActividad|0..*|propietario de respuesta XOR IntentoEvaluacion
Socio|1|InscripcionTaller|0..*|inscripción/asistencia única por taller
Taller|1|InscripcionTaller|0..*|asistencia con cupo controlado
Usuario|0..1|InscripcionTaller|0..*|responsable que confirma asistencia
Campana|1|Sorteo|0..*|campaña de sorteo según SQL; obligatoriedad pendiente P04
Sorteo|1|ParticipacionSorteo|0..*|participaciones registradas
Socio|1|ParticipacionSorteo|0..*|socio participante
ActividadValidada|1|ParticipacionSorteo|0..*|origen validado de participación
Sorteo|1|PremioSorteo|1..*|premios del sorteo
Sorteo|1|EvidenciaSorteo|0..1|lista y evidencia tras congelación
Sorteo|1|ResultadoSorteo|0..*|ganadores y suplentes, antes de ejecución vacío
ParticipacionSorteo|1|ResultadoSorteo|0..1|participación seleccionada del mismo sorteo
PremioSorteo|0..1|ResultadoSorteo|0..*|asignación; suplente puede no tener premio todavía
Socio|1|Canje|0..*|solicitudes propias
Beneficio|1|Canje|0..*|beneficio solicitado
Canje|0..1|MovimientoPuntos|0..*|reserva, descuento o liberación del canje
Usuario|0..1|Canje|0..*|responsable de decisión
Usuario|0..1|Canje|0..*|responsable de entrega, rol separado de aprobación
ConvenioBienestar|0..1|Beneficio|0..*|origen del beneficio, opcional
Usuario|1|ContenidoInstitucional|0..*|autor o gestor
ContenidoInstitucional|1|AprobacionContenido|0..*|decisiones versionadas de aprobación opcional
Usuario|1|AprobacionContenido|0..*|responsable designado
ContenidoInstitucional|1|MaterialEducativo|0..*|organización de material según diseño SQL; revisar con repositorio reutilizable
ContenidoInstitucional|1|RecursoBienestar|0..*|contenido informativo de bienestar
ConvenioBienestar|0..1|RecursoBienestar|0..*|convenio asociado cuando corresponde
Usuario|1|PreferenciaNotificacion|0..*|preferencias por evento y canal
Usuario|1|Notificacion|0..*|destinatario
Notificacion|1|EnvioNotificacion|0..*|entregas por canal
PlantillaNotificacion|1|EnvioNotificacion|0..*|plantilla usada para evento/canal
Socio|1|Partida|0..*|jugador
Juego|1|Partida|0..*|configuración del juego
Socio|1|ProgresoReto|0..*|progreso propio
Reto|1|ProgresoReto|0..*|reto medible
ReglaPuntos|0..1|Reto|0..*|regla de recompensa; referencia histórica a preservar
Socio|1|PublicacionComunidad|0..*|autor socio
PublicacionComunidad|1|Comentario|0..*|comentarios recibidos
Socio|1|Comentario|0..*|autor del comentario
PublicacionComunidad|1|Reaccion|0..*|reacciones recibidas
Socio|1|Reaccion|0..*|una por publicación según SQL
Socio|1|ReporteComunidad|0..*|persona que reporta
PublicacionComunidad|0..1|ReporteComunidad|0..*|objeto reportado XOR Comentario
Comentario|0..1|ReporteComunidad|0..*|objeto reportado XOR PublicacionComunidad
ReporteComunidad|1|DecisionModeracion|0..*|decisiones con motivo
Usuario|1|DecisionModeracion|0..*|gestor autorizado
Socio|0..1|DecisionModeracion|0..*|socio afectado si hay suspensión temporal
FiltroReporte|1|ResultadoReporte|0..*|filtros aplicados al resultado
"""
RELS = [linea.split('|') for linea in RELACIONES.strip().splitlines()]

# Una operación representativa por HU; la HU puede involucrar varias clases y reglas.
MAPEO = """
1 Usuario.calcularEdad G02
2 Usuario.calcularEdad G02
3 Usuario.actualizarContacto G02
4 Usuario.cambiarContrasena G02
5 Usuario.cambiarEstado G17
6 EntradaPadron.habilitaCondicionSocio G02
7 Usuario.cambiarEstado G17
8 Usuario.calcularEdad G02
9 ControlAcceso.validarCredenciales G01
10 ControlAcceso.validarCredenciales G01
11 RecuperacionAcceso.restablecerContrasena G01
12 Rol.habilita G01
13 Rol.habilita G17
14 ControlAcceso.autorizar G17
15 Sesion.cerrar G01
16 CodigoReferido.esValido G03
17 Referido.validarRegistro G04
18 Referido.confirmarConversion G16
19 CodigoReferido.generarEnlace G03
20 Referido.validarRegistro G15
21 Referido.iniciarSeguimiento G05
22 ServicioReportes.generarReferidosCampanas G14
23 ConsentimientoProspecto.confirmar G04
24 Referido.iniciarSeguimiento G15
25 Campana.activar G18
26 Campana.suspender G18
27 Campana.admiteParticipacion G06
28 Segmento.incluye G18
29 Campana.modificarCondiciones G18
30 Campana.calcularTasaConversion G18
31 ReglaPuntos.calcularPuntos G18
32 CuentaPuntos.acreditar G07
33 Nivel.seAlcanzaCon G07
34 CuentaPuntos.calcularSaldoDisponible G07
35 Clasificacion.calcularPosicion G07
36 CuentaPuntos.calcularSaldoContable G07
37 Insignia.seCumplePara G07
38 CuentaPuntos.revertir G07
39 Capacitacion.puedeInscribirse G08
40 InscripcionCapacitacion.calcularAvance G08
41 IntentoEvaluacion.calificar G08
42 Certificado.emitir G08
43 Certificado.obtenerDocumento G08
44 Capacitacion.publicar G19
45 Certificado.verificarAutenticidad G19
46 Taller.calcularCuposDisponibles G19
47 InscripcionTaller.registrarAsistencia G08
48 Sorteo.verificarElegibilidad G20
49 ParticipacionSorteo.validarOrigen G09
50 Sorteo.ejecutar G20
51 ResultadoSorteo.obtenerDatosPublicos G09
52 EnvioNotificacion.programar G20
53 EvidenciaSorteo.verificarIntegridad G20
54 Beneficio.estaDisponible G21
55 Canje.solicitar G10
56 Canje.aprobar G21
57 Beneficio.estaDisponible G10
58 Canje.registrarEntrega G21
59 CuentaPuntos.confirmarDescuento G21
60 ContenidoInstitucional.retirar G22
61 ContenidoInstitucional.publicar G22
62 MaterialEducativo.esAdmisible G22
63 ContenidoInstitucional.esVisible G11
64 ContenidoInstitucional.esVisible G22
65 AprobacionContenido.aprobar G22
66 PlantillaNotificacion.prepararMensaje G11
67 PreferenciaNotificacion.permiteEnvio G11
68 EnvioNotificacion.puedeReintentarse G11
69 Notificacion.marcarLeida G11
70 EnvioNotificacion.registrarResultado G11
71 Juego.activar G23
72 Pregunta.evaluar G23
73 Juego.admitePartida G12
74 Partida.calcularResultado G12
75 Partida.habilitaReconocimiento G23
76 Juego.calcularIntentosRestantes G12
77 Reto.cumpleObjetivo G23
78 ProgresoReto.reconocerCumplimiento G12
79 PublicacionComunidad.publicar G12
80 PublicacionComunidad.admiteInteraccion G12
81 ReporteComunidad.enviarAModeracion G24
82 DecisionModeracion.aplicar G24
83 PerfilPublico.definirPrivacidad G12
84 ConvenioBienestar.estaVigente G13
85 RecursoBienestar.esVisible G13
86 ConvenioBienestar.habilitaBeneficio G13
87 ServicioReportes.generarSupervision G25
88 ServicioReportes.generarReferidosCampanas G25
89 ServicioReportes.generarImpactoSocial G25
90 ServicioReportes.generarGamificacion G25
91 ServicioReportes.exportar G25
"""
MAP = {int(n): (op, 'CU-' + cu) for n, op, cu in (x.split() for x in MAPEO.strip().splitlines())}
# No atribuir a una operación de consulta/calculadora una responsabilidad de alta/configuración que no tiene.
SOPORTE = {
    1: 'Datos de Usuario y ConsentimientoCuenta; alta coordinada por registro_service.py, operación de registro a modelar como servicio si se requiere',
    2: 'Datos de Usuario y titularidad; consulta del perfil, no cálculo de edad como realización del requisito',
    5: 'Datos de Usuario, Rol y EventoAuditoria; alta/edición administrativa requiere coordinación adicional',
    8: 'Restricciones únicas de cedula/correo/nombreUsuario y alta atómica; calcularEdad no implementa unicidad',
    12: 'Asociación Usuario–Rol; obtención de roles y unión de accesos',
    13: 'Asociaciones Usuario–Rol–Permiso; administración de asignaciones, no solamente consulta habilita',
    16: 'Generación única no secuencial y asociación a Socio; esValido solo representa validación del valor',
    21: 'Consulta por titularidad e historial enmascarado; iniciarSeguimiento no es la operación de consulta',
    25: 'Atributos de Campana y configuración previa a activar',
    31: 'Configuración/versionado de ReglaPuntos además de calcularPuntos',
    33: 'Insignia, InsigniaObtenida y notificación además de Nivel',
    37: 'Configuración de Nivel e Insignia además de evaluar criterio',
    46: 'Configuración de Taller además del cálculo de cupos',
    48: 'Configuración de Sorteo y PremioSorteo además de elegibilidad',
    54: 'Configuración de Beneficio además de disponibilidad',
    58: 'Consulta de canjes por titular y filtro de estado; registrarEntrega no realiza la consulta',
    66: 'Configuración de PlantillaNotificacion además de preparación de mensaje',
    70: 'Consulta autorizada de envíos y filtros, no solo registro de resultado',
    72: 'Configuración de Juego/Pregunta/OpcionPregunta además de evaluar respuesta',
    77: 'Configuración de Reto además de comprobar cumplimiento',
    84: 'Configuración de ConvenioBienestar y prohibición de datos clínicos además de vigencia',
}

# Reemplazos con operaciones semánticamente correctas para consultas/altas de negocio.
ADICIONALES = {
    'Usuario': ['consultarPerfil(solicitante: Usuario): DatosPerfil'],
    'ControlAcceso': ['registrarCuenta(datos: DatosRegistro, consentimiento: ConsentimientoCuenta): Usuario',
                     'validarUnicidad(datos: DatosRegistro): Booleano',
                     'registrarPersonal(datos: DatosRegistro, roles: Coleccion<Rol>, administrador: Usuario): Usuario',
                     'identificarRoles(usuario: Usuario): Coleccion<Rol>',
                     'asignarRol(usuario: Usuario, rol: Rol, administrador: Usuario): Booleano',
                     'revocarRol(usuario: Usuario, rol: Rol, administrador: Usuario): Booleano'],
    'CodigoReferido': ['generarPara(socio: Socio): CodigoReferido'],
    'Referido': ['consultarSeguimiento(solicitante: Usuario): DatosSeguimiento'],
    'ReglaPuntos': ['configurarVersion(condiciones: Condiciones, administrador: Usuario): ReglaPuntos'],
    'Nivel': ['definirUmbral(puntos: Entero, administrador: Usuario): Booleano'],
    'Insignia': ['definirCriterio(criterio: Texto, administrador: Usuario): Booleano'],
    'Taller': ['programar(condiciones: Condiciones, responsable: Usuario): Booleano'],
    'Sorteo': ['configurar(condiciones: Condiciones, responsable: Usuario): Booleano'],
    'Beneficio': ['configurar(condiciones: Condiciones, responsable: Usuario): Booleano'],
    'Canje': ['consultarEstado(solicitante: Usuario): EstadoCanje'],
    'PlantillaNotificacion': ['definirContenido(titulo: Texto, cuerpo: Texto, responsable: Usuario): Booleano'],
    'EnvioNotificacion': ['consultarHistorial(filtro: FiltroReporte, solicitante: Usuario): Coleccion<EnvioNotificacion>'],
    'Juego': ['definirContenido(instrucciones: Texto, preguntas: Coleccion<Pregunta>, responsable: Usuario): Booleano'],
    'Reto': ['definirObjetivo(tipoActividad: Texto, cantidad: Entero, responsable: Usuario): Booleano'],
    'ConvenioBienestar': ['configurar(condiciones: Condiciones, responsable: Usuario): Booleano'],
}
for clase in CLASES:
    clase['operaciones'].extend(ADICIONALES.get(clase['nombre'], []))
for n, op in {
    1:'ControlAcceso.registrarCuenta', 2:'Usuario.consultarPerfil', 5:'ControlAcceso.registrarPersonal',
    8:'ControlAcceso.validarUnicidad', 12:'ControlAcceso.identificarRoles', 13:'ControlAcceso.asignarRol',
    16:'CodigoReferido.generarPara', 21:'Referido.consultarSeguimiento', 31:'ReglaPuntos.configurarVersion',
    37:'Nivel.definirUmbral', 46:'Taller.programar', 48:'Sorteo.configurar', 54:'Beneficio.configurar',
    58:'Canje.consultarEstado', 66:'PlantillaNotificacion.definirContenido', 70:'EnvioNotificacion.consultarHistorial',
    72:'Juego.definirContenido', 77:'Reto.definirObjetivo', 84:'ConvenioBienestar.configurar',
}.items():
    MAP[n] = (op, MAP[n][1])

DEPENDENCIAS = [
    ('ControlAcceso','EntradaPadron','consulta condición para registrar'),
    ('ControlAcceso','Rol','identifica/asigna roles'),
    ('ControlAcceso','Sesion','abre y autoriza sesiones'),
    ('ControlAcceso','EventoAuditoria','deja evidencia'),
    ('ValidacionAdministrativaSocio','EntradaPadron','consulta/añade confirmación temporal autorizada'),
    ('ValidacionAdministrativaSocio','Socio','habilita condición, no conversión comercial'),
    ('RecuperacionAcceso','Sesion','revoca sesiones al restablecer'),
    ('Referido','EntradaPadron','descarta prospecto ya socio'),
    ('Referido','ActividadValidada','conversión validada produce actividad'),
    ('IntentoEvaluacion','ActividadValidada','aprobación produce actividad'),
    ('InscripcionTaller','ActividadValidada','asistencia produce actividad'),
    ('Partida','ActividadValidada','resultado válido produce actividad'),
    ('ProgresoReto','ActividadValidada','cumplimiento produce actividad'),
    ('Canje','CuentaPuntos','coordina reserva/descuento/liberación'),
    ('Clasificacion','CuentaPuntos','consulta puntos con política pendiente'),
    ('Clasificacion','PerfilPublico','respeta alias y exclusión'),
    ('ServicioReportes','Referido','consulta captación'),
    ('ServicioReportes','Campana','consulta resultados'),
    ('ServicioReportes','InscripcionCapacitacion','consulta formación'),
    ('ServicioReportes','Certificado','consulta certificados'),
    ('ServicioReportes','MovimientoPuntos','consulta puntos'),
    ('ServicioReportes','Canje','consulta recompensas'),
    ('ServicioReportes','ResultadoSorteo','consulta resultados enmascarados'),
    ('ServicioReportes','Usuario','autoriza según roles vigentes'),
    ('ServicioReportes','ResultadoReporte','genera salida y aplica privacidad'),
    ('Referido','CambioEstado','conserva seguimiento'),
    ('Campana','CambioEstado','conserva cambios'),
    ('Canje','CambioEstado','conserva decisiones y entrega'),
    ('CuentaPuntos','Notificacion','comunica reconocimientos'),
    ('Sorteo','Notificacion','comunica ganadores'),
    ('DecisionModeracion','Usuario','aplica suspensión autorizada cuando corresponde'),
]

REGISTROS = {'ConsentimientoCuenta','EventoAuditoria','CambioEstado','ConsentimientoProspecto','Conversion',
             'MovimientoPuntos','InsigniaObtenida','EvidenciaSorteo','ResultadoSorteo','DecisionModeracion','AprobacionContenido'}
VALORES = {'ActividadValidada','RespuestaActividad','FiltroReporte','ResultadoReporte'}
SERVICIOS = {'ServicioReportes'}
def estereotipo(nombre):
    return 'Registro' if nombre in REGISTROS else 'ObjetoValor' if nombre in VALORES else 'ServicioDominio' if nombre in SERVICIOS else 'Entidad'

def generar():
    assert len(NOMBRES) == len(CLASES), 'Clases duplicadas'
    for a, ma, b, mb, nota in RELS:
        assert a in NOMBRES and b in NOMBRES, (a,b)
        assert ma in {'0..1','1','0..*','1..*'} and mb in {'0..1','1','0..*','1..*'}
    for a,b,_ in DEPENDENCIAS:
        assert a in NOMBRES and b in NOMBRES
    for n,(op,_) in MAP.items():
        nombre, metodo = op.split('.')
        clase = next(c for c in CLASES if c['nombre'] == nombre)
        assert any(x.startswith(metodo+'(') for x in clase['operaciones']), (n,op)

    intro = '''# Catálogo propuesto de clases de negocio

Modelo de análisis del alcance completo, revisado el 10 de noviembre de 2026. Las operaciones son responsabilidades propuestas; no constituyen un inventario literal de métodos del código. Los módulos posteriores a identidad/seguridad están planificados. Consultar DECISIONES-Y-REGLAS.md para evidencia, brechas y políticas pendientes.

Todos los atributos y operaciones no implementados explícitamente en la fuente citada son propuestas derivadas de requisitos. La misma clase puede combinar atributos existentes y planificados. No equivale a una especificación física completa de base de datos.

Convención: `- atributo: Tipo`, `+ operacion(parametro: Tipo): Retorno`; `/` marca un valor derivado; `[0..1]` indica dato opcional. Los registros inmutables pueden carecer de operaciones propias. `Identificador`, `Recurso`, `Referencia`, `Condiciones`, `DatosRegistro`, `DatosPerfil`, `DatosEvento`, `DatosSeguimiento`, `DatosPublicos`, `DatosEnmascarados`, `Indicador`, `Criterio` y `PosicionPublica` son tipos de análisis auxiliares, cuyo detalle debe concretarse si aporta comprensión; no son clases implementadas. `Secreto` es un dato transitorio de entrada. No se modela almacenamiento de contraseñas en claro.

No todas las relaciones son persistentes. CuentaPuntos, Clasificacion y ControlAcceso agrupan responsabilidades conceptuales. EntradaPadron se consulta por cédula; no se exige una FK permanente desde cada usuario. Los métodos de configuración describen cambios con sentido de negocio y permisos, sin operaciones de persistencia genéricas.

'''
    salida = [intro, f'Inventario: **{len(CLASES)} clases**, **{len(RELS)} asociaciones** y **{len(DEPENDENCIAS)} dependencias** propuestas. Las enumeraciones se definen en DECISIONES-Y-REGLAS.md.\n']
    for modulo in dict.fromkeys(c['modulo'] for c in CLASES):
        salida.append(f'\n## {modulo}\n')
        for c in (c for c in CLASES if c['modulo']==modulo):
            salida.extend([f"\n### {c['nombre']}\n", f"Estereotipo propuesto: `{estereotipo(c['nombre'])}`. {c['nota']}\n", '\n```text'])
            salida.extend('- '+x for x in c['atributos'])
            if c['atributos'] and c['operaciones']:
                salida.append('')
            salida.extend('+ '+x for x in c['operaciones'])
            if not c['operaciones']:
                salida.append('(Sin operaciones propias: registro u objeto de datos.)')
            salida.append('```\n')
    salida += ['\n## Asociaciones y multiplicidades\n',
               'Cada fila se lee: un A tiene la cantidad de B indicada en «B por A»; un B tiene la cantidad de A indicada en «A por B». Los nombres de roles se precisan mediante el significado. Restricciones condicionales prevalecen sobre el máximo general.\n',
               '| A | A por B | B | B por A | Significado y restricción |',
               '| --- | --- | --- | --- | --- |']
    salida += ['| '+' | '.join(r)+' |' for r in RELS]
    salida += ['\n## Dependencias de responsabilidad\n', '| Origen | Destino | Motivo |', '| --- | --- | --- |']
    salida += ['| '+' | '.join(r)+' |' for r in DEPENDENCIAS]
    salida += ['\nLa actividad comercial o formativa origina una ActividadValidada; los movimientos de canje enlazan directamente con Canje. Las dependencias a CambioEstado explican su uso, y su entidad/referencia identifica el objeto seguido sin crear una FK universal inexistente. Validar política de retención; ninguna composición autoriza borrar evidencia histórica.\n']
    (BASE/'CATALOGO-CLASES.md').write_text('\n'.join(salida), encoding='utf-8')

    with (REPO/'documentacion/product_con_subtareas.csv').open(encoding='utf-8-sig', newline='') as f:
        filas=list(csv.DictReader(f))
    porid={r['Work item ID']:r for r in filas}
    historias=sorted((r for r in filas if re.match(r'^HU-\d+',r['Summary'])), key=lambda r:int(re.match(r'HU-(\d+)',r['Summary'])[1]))
    assert len(historias)==91 and set(MAP)==set(range(1,92))
    inventario=json.loads((BASE/'inventario-ea.json').read_text(encoding='utf-8-sig'))
    diagramas=inventario['diagramas']
    out=['# Matriz propuesta de trazabilidad de negocio\n',
         '91 referencias HU originales extraídas del CSV, incluidas las subtareas de historias consolidadas. RF/UR/RNF corresponden al primer bloque de cada fila; no se suman los bloques consolidados de nuevo. La relación con clases, operaciones y CU es una propuesta de análisis, no prueba de implementación ni de enlaces ya creados en EA.\n',
         'El CU se identifica por el título real de un diagrama y su ID, no por un GUID inventado. La correspondencia semántica debe validarse contra los elementos UseCase y sus escenarios al crear trazabilidad nativa. CU-G11/G07/G18 agrupan algunas funciones administrativas cuyo caso específico no está separado; ampliar trazabilidad cuando corresponda.\n',
         '| HU y propósito | Padre consolidado si es subtarea | UR | RF | RNF | CU propuesto y diagrama EA | Clase y operación representativa |',
         '| --- | --- | --- | --- | --- | --- | --- |']
    for r in historias:
        num=int(re.match(r'HU-(\d+)',r['Summary'])[1])
        primera=re.split(r'\*Consolidación|\*Registro de conversión',r['Description'])[0]
        rf=list(dict.fromkeys(re.findall(r'RF-\d{2}-\d+',primera.split('*Trazabilidad:*')[-1].split('Dep.:')[0])))
        ur=list(dict.fromkeys(re.findall(r'UR-\d+',primera)))
        rnf=list(dict.fromkeys(re.findall(r'RNF-\d+',primera)))
        padre=porid.get(r['Parent'],{}).get('Summary','—') if r['Work Type']=='Sub-task' else '—'
        op,cu=MAP[num]
        ds=[d for d in diagramas if d['Name'].startswith(cu+' -')]
        assert len(ds)==1,(cu,ds)
        d=ds[0]
        celda=f"{d['Name']} (Diagram_ID {d['Diagram_ID']})"
        campos=[r['Summary'],padre,', '.join(ur) or '—',', '.join(rf) or '—',', '.join(rnf) or '—',celda,op+'()']
        out.append('| '+' | '.join(str(x).replace('|','/') for x in campos)+' |')
    out += ['\n## Elementos reales de casos de uso identificados en EA\n',
            'Se verificó que cada elemento principal aparece en su diagrama de detalle mediante t_diagramobjects. Los GUID siguientes se leyeron del repositorio; no son vínculos nuevos. La relación de estas clases propuestas a esos elementos todavía debe crearse.\n',
            '| Código del título | Diagram_ID | Object_ID principal | Nombre del UseCase | GUID del UseCase |',
            '| --- | --- | --- | --- | --- |']
    principales=[33,48,49,51,52,53,54,55,56,57,58,59,60,61,62,63,64,73,65,66,67,68,70,71,72]
    for indice,object_id in enumerate(principales,1):
        codigo=f'CU-G{indice:02}'
        diagrama=next(d for d in diagramas if d['Name'].startswith(codigo+' -'))
        elemento=next(e for e in inventario['elementos'] if e['Object_ID']==object_id)
        assert elemento['Object_Type']=='UseCase'
        assert any(x['Diagram_ID']==diagrama['Diagram_ID'] and x['Object_ID']==object_id for x in inventario['elementos_diagrama'])
        out.append(f"| {codigo} | {diagrama['Diagram_ID']} | {object_id} | {elemento['Name']} | `{elemento['ea_guid']}` |")
    out += ['\n## Reglas de lectura y cobertura\n',
            'La fuente de cada fila es `documentacion/product_con_subtareas.csv`, identificada por su HU y su Work item ID en el archivo. Cada operación figura con firma completa en CATALOGO-CLASES.md; sus atributos, asociaciones e invariantes completan el significado de la fila. Una operación representativa no cubre por sí sola todos los criterios de una historia.\n',
            '| HU | Regla o soporte adicional para evaluar cobertura |','| --- | --- |']
    for n,nota in SOPORTE.items():
        # Notas redactadas antes del reemplazo; quitar advertencias sobre operaciones antiguas.
        nota=nota.replace('; calcularEdad no implementa unicidad','').replace(', no cálculo de edad como realización del requisito','').replace('; iniciarSeguimiento no es la operación de consulta','').replace('; registrarEntrega no realiza la consulta','')
        out.append(f'| HU-{n:03} | {nota} |')
    out += ['\n## Estado y fuentes de evidencia\n',
            '| Ámbito | Estado observado | Fuente y límite |', '| --- | --- | --- |',
            '| Registro, padrón, login, roles actuales y sesiones | Implementado en el alcance descrito por Sprint 1 | matriz-trazabilidad.md y servicios de usuarios; pruebas referenciadas, no ejecutadas en esta revisión |',
            '| Recuperación de acceso | Implementación existente revisada | recuperacion_service.py y TokenRecuperacion; no equivale al módulo general de notificaciones |',
            '| Administración completa de usuarios, estados y permisos | Parcial / planificada según operación | Crear personal existe como comando/servicio; no afirmar CRUD administrativo completo por las pantallas de ejemplo |',
            '| Conversión administrativa temporal | Implementada, ampliación posterior | conversion-administrativa-temporal.md; no tiene HU original equivalente exacta y no sustituye HU-018 |',
            '| Referidos, campañas, puntos, formación, sorteos, canjes, contenido, comunidad, juegos, bienestar, reportes y notificaciones generales | Planificados con diseño parcial y pantallas demostrativas | CSV, SQL 01–02, demo.js; clases y operaciones del catálogo son propuestas, no evidencia operativa |',
            '\n## Trazabilidad pendiente de crear dentro de EA\n',
            'Crear enlaces nativos hacia los elementos reales de CU y requisitos, registrar GUID, y verificar por criterio de aceptación. El inventario conserva datos de consulta pero no certifica enlaces nuevos. El proceso administrativo temporal debe usar una referencia local de decisión, sin inventarle un RF/HU del backlog. Los conceptos auxiliares propuestos justifican su existencia por las HU de sus clases relacionadas y deben anotarse así en EA.\n']
    (BASE/'TRAZABILIDAD.md').write_text('\n'.join(out),encoding='utf-8')

    (BASE/'diagramas').mkdir(exist_ok=True)
    # Vistas modulares: clases del módulo con detalle; externas solo como referencia.
    for modulo in dict.fromkeys(c['modulo'] for c in CLASES):
        locales={c['nombre'] for c in CLASES if c['modulo']==modulo}
        relaciones=[r for r in RELS if r[0] in locales or r[2] in locales]
        deps=[r for r in DEPENDENCIAS if r[0] in locales]
        externas=({r[0] for r in relaciones}|{r[2] for r in relaciones}|{r[1] for r in deps})-locales
        p=['@startuml',f'title Modelo de análisis propuesto — {modulo}', 'skinparam classAttributeIconSize 0', 'hide empty members', 'left to right direction']
        p += [f'class {n} <<Referencia>>' for n in sorted(externas)]
        for c in (c for c in CLASES if c['nombre'] in locales):
            p.append(f"class {c['nombre']} <<{estereotipo(c['nombre'])}>> {{")
            p += ['  - '+a for a in c['atributos']]
            p += ['  + '+op for op in c['operaciones']]
            p.append('}')
        for a,ma,b,mb,nota in relaciones:
            con='*--' if (a,b) in {('Capacitacion','ModuloCapacitacion'),('Pregunta','OpcionPregunta')} else '--'
            p.append(f'{a} "{ma}" {con} "{mb}" {b} : {nota}')
        p += [f'{a} ..> {b} : {nota}' for a,b,nota in deps]
        p += ['legend bottom', 'Propuesta de análisis. Ver decisiones y pendientes.', 'Las referencias externas son los mismos conceptos de otros módulos.', 'No representa implementación ni importación verificada en EA.', 'endlegend','@enduml']
        (BASE/'diagramas'/f'{modulo}.puml').write_text('\n'.join(p)+'\n',encoding='utf-8')
    (BASE/'fuentes/modelo.json').write_text(json.dumps(dict(clases=CLASES,asociaciones=RELS,dependencias=DEPENDENCIAS),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Generadas {len(CLASES)} clases, {len(RELS)} asociaciones, {len(DEPENDENCIAS)} dependencias y {len(historias)} filas HU.')

if __name__=='__main__':
    generar()
