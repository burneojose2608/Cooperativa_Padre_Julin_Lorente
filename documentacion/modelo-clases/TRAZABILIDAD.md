# Matriz propuesta de trazabilidad de negocio

91 referencias HU originales extraídas del CSV, incluidas las subtareas de historias consolidadas. RF/UR/RNF corresponden al primer bloque de cada fila; no se suman los bloques consolidados de nuevo. La relación con clases, operaciones y CU es una propuesta de análisis, no prueba de implementación ni de enlaces ya creados en EA.

El CU se identifica por el título real de un diagrama y su ID, no por un GUID inventado. La correspondencia semántica debe validarse contra los elementos UseCase y sus escenarios al crear trazabilidad nativa. CU-G11/G07/G18 agrupan algunas funciones administrativas cuyo caso específico no está separado; ampliar trazabilidad cuando corresponda.

| HU y propósito | Padre consolidado si es subtarea | UR | RF | RNF | CU propuesto y diagrama EA | Clase y operación representativa |
| --- | --- | --- | --- | --- | --- | --- |
| HU-001: Registrar socio con validación de cédula, padrón y duplicados | — | UR-01 | RF-01-1 | RNF-01, RNF-02, RNF-07, RNF-20, RNF-23 | CU-G02 - Gestionar perfil (Detalle) (Diagram_ID 40) | ControlAcceso.registrarCuenta() |
| HU-002: Consultar y actualizar mi perfil | — | UR-02 | RF-01-2 | RNF-10 | CU-G02 - Gestionar perfil (Detalle) (Diagram_ID 40) | Usuario.consultarPerfil() |
| HU-003: Editar los datos de contacto del perfil | HU-002: Consultar y actualizar mi perfil | UR-03 | RF-01-3 | RNF-07, RNF-20, RNF-26 | CU-G02 - Gestionar perfil (Detalle) (Diagram_ID 40) | Usuario.actualizarContacto() |
| HU-004: Cambiar la contraseña | — | UR-06 | RF-01-4 | RNF-01, RNF-06 | CU-G02 - Gestionar perfil (Detalle) (Diagram_ID 40) | Usuario.cambiarContrasena() |
| HU-005: Administrar cuentas de usuarios y sus estados | — | UR-04 | RF-01-5 | RNF-06, RNF-10 | CU-G17 - Administrar usuarios y permisos (Detalle) (Diagram_ID 41) | ControlAcceso.registrarPersonal() |
| HU-006: Validar la condición de socio activo | HU-001: Registrar socio con validación de cédula, padrón y duplicados | UR-01 | RF-01-6 | RNF-23 | CU-G02 - Gestionar perfil (Detalle) (Diagram_ID 40) | EntradaPadron.habilitaCondicionSocio() |
| HU-007: Gestionar el estado de las cuentas | HU-005: Administrar cuentas de usuarios y sus estados | UR-04 | RF-01-7 | RNF-06, RNF-11 | CU-G17 - Administrar usuarios y permisos (Detalle) (Diagram_ID 41) | Usuario.cambiarEstado() |
| HU-008: Prevenir cuentas duplicadas | HU-001: Registrar socio con validación de cédula, padrón y duplicados | UR-01 | RF-01-8 | RNF-20 | CU-G02 - Gestionar perfil (Detalle) (Diagram_ID 40) | ControlAcceso.validarUnicidad() |
| HU-009: Iniciar y cerrar sesión con validación de credenciales y roles | — | UR-05 | RF-02-1 | RNF-03, RNF-09, RNF-21 | CU-G01 - Iniciar Sesión (Detalle) (Diagram_ID 7) | ControlAcceso.validarCredenciales() |
| HU-010: Validar credenciales de acceso | HU-009: Iniciar y cerrar sesión con validación de credenciales y roles | UR-05 | RF-02-2 | RNF-01, RNF-06, RNF-21 | CU-G01 - Iniciar Sesión (Detalle) (Diagram_ID 7) | ControlAcceso.validarCredenciales() |
| HU-011: Recuperar la contraseña por correo | — | UR-06 | RF-02-3 | RNF-01, RNF-21 | CU-G01 - Iniciar Sesión (Detalle) (Diagram_ID 7) | RecuperacionAcceso.restablecerContrasena() |
| HU-012: Identificar los roles del usuario autenticado | HU-009: Iniciar y cerrar sesión con validación de credenciales y roles | UR-07 | RF-02-4 | RNF-10 | CU-G01 - Iniciar Sesión (Detalle) (Diagram_ID 7) | ControlAcceso.identificarRoles() |
| HU-013: Administrar roles, permisos y acceso seguro | — | UR-07 | RF-02-5 | RNF-06, RNF-10 | CU-G17 - Administrar usuarios y permisos (Detalle) (Diagram_ID 41) | ControlAcceso.asignarRol() |
| HU-014: Autorizar el acceso según rol en el servidor | HU-013: Administrar roles, permisos y acceso seguro | UR-07 | RF-02-6 | RNF-10, RNF-20 | CU-G17 - Administrar usuarios y permisos (Detalle) (Diagram_ID 41) | ControlAcceso.autorizar() |
| HU-015: Cerrar sesión e invalidarla en el servidor | HU-009: Iniciar y cerrar sesión con validación de credenciales y roles | UR-05 | RF-02-7 | RNF-11 | CU-G01 - Iniciar Sesión (Detalle) (Diagram_ID 7) | Sesion.cerrar() |
| HU-016: Generar y compartir mi código de referido | — | UR-08 | RF-03-1 | RNF-06 | CU-G03 - Generar código de referido (Detalle) (Diagram_ID 42) | CodigoReferido.generarPara() |
| HU-017: Registrar prospectos referidos con validaciones y consentimiento | — | UR-09 | RF-03-2 | RNF-02, RNF-20, RNF-21 | CU-G04 - Registrar persona referida (Detalle) (Diagram_ID 43) | Referido.validarRegistro() |
| HU-018: Gestionar seguimiento, estados y conversión de referidos | — | UR-11 | RF-03-3 | RNF-06, RNF-12, RNF-13 | CU-G16 - Confirmar conversión a socio (Detalle) (Diagram_ID 47) | Referido.confirmarConversion() |
| HU-019: Compartir código o enlace de referido | HU-016: Generar y compartir mi código de referido | UR-08 | RF-03-4 | RNF-03 | CU-G03 - Generar código de referido (Detalle) (Diagram_ID 42) | CodigoReferido.generarEnlace() |
| HU-020: Prevenir referidos inválidos | HU-017: Registrar prospectos referidos con validaciones y consentimiento | UR-44 | RF-03-5 | RNF-17 | CU-G15 - Validar registros de referidos (Detalle) (Diagram_ID 46) | Referido.validarRegistro() |
| HU-021: Consultar mis referidos | — | UR-10 | RF-03-6 | RNF-10, RNF-14 | CU-G05 - Consultar estado de referidos (Detalle) (Diagram_ID 44) | Referido.consultarSeguimiento() |
| HU-022: Consultar resultados de referidos (Marketing) | — | UR-45 | RF-03-7 | RNF-14 | CU-G14 - Consultar prospectos referidos (Detalle) (Diagram_ID 45) | ServicioReportes.generarReferidosCampanas() |
| HU-023: Confirmar el consentimiento del prospecto | HU-017: Registrar prospectos referidos con validaciones y consentimiento | UR-43 | RF-03-8 | RNF-02, RNF-25 | CU-G04 - Registrar persona referida (Detalle) (Diagram_ID 43) | ConsentimientoProspecto.confirmar() |
| HU-024: Gestionar los estados del referido | HU-018: Gestionar seguimiento, estados y conversión de referidos | UR-10, UR-11 | RF-03-9 | RNF-06, RNF-13 | CU-G15 - Validar registros de referidos (Detalle) (Diagram_ID 46) | Referido.iniciarSeguimiento() |
| HU-025: Crear y activar campañas | — | UR-12 | RF-04-1 | RNF-06, RNF-07 | CU-G18 - Gestionar Campañas e incentivos (Detalle) (Diagram_ID 49) | Campana.activar() |
| HU-026: Gestionar el estado de las campañas | HU-025: Crear y activar campañas | UR-15 | RF-04-2 | RNF-06 | CU-G18 - Gestionar Campañas e incentivos (Detalle) (Diagram_ID 49) | Campana.suspender() |
| HU-027: Consultar campañas vigentes | — | UR-14 | RF-04-3 | RNF-03 | CU-G06 - Participar en campañas (Detalle) (Diagram_ID 48) | Campana.admiteParticipacion() |
| HU-028: Segmentar y modificar campañas con historial | — | UR-13 | RF-04-4 | RNF-06 | CU-G18 - Gestionar Campañas e incentivos (Detalle) (Diagram_ID 49) | Segmento.incluye() |
| HU-029: Modificar campañas conservando el historial | HU-028: Segmentar y modificar campañas con historial | UR-15 | RF-04-5 | RNF-06 | CU-G18 - Gestionar Campañas e incentivos (Detalle) (Diagram_ID 49) | Campana.modificarCondiciones() |
| HU-030: Monitorear los resultados de una campaña | — | UR-46 | RF-04-6 | RNF-04 | CU-G18 - Gestionar Campañas e incentivos (Detalle) (Diagram_ID 49) | Campana.calcularTasaConversion() |
| HU-031: Configurar reglas de puntuación | — | UR-16 | RF-05-1 | RNF-06 | CU-G18 - Gestionar Campañas e incentivos (Detalle) (Diagram_ID 49) | ReglaPuntos.configurarVersion() |
| HU-032: Acreditar puntos y registrar movimientos inmutables | — | UR-16 | RF-05-2 | RNF-12 | CU-G07 - Consultar puntos y logros (Detalle) (Diagram_ID 13) | CuentaPuntos.acreditar() |
| HU-033: Calcular nivel e insignias | — | UR-18 | RF-05-3 | — | CU-G07 - Consultar puntos y logros (Detalle) (Diagram_ID 13) | Nivel.seAlcanzaCon() |
| HU-034: Consultar puntos y logros | — | UR-17 | RF-05-4 | RNF-10 | CU-G07 - Consultar puntos y logros (Detalle) (Diagram_ID 13) | CuentaPuntos.calcularSaldoDisponible() |
| HU-035: Consultar clasificaciones | — | UR-19 | RF-05-5 | RNF-14 | CU-G07 - Consultar puntos y logros (Detalle) (Diagram_ID 13) | Clasificacion.calcularPosicion() |
| HU-036: Registrar movimientos inmutables de puntos | HU-032: Acreditar puntos y registrar movimientos inmutables | UR-17 | RF-05-6 | RNF-06, RNF-12 | CU-G07 - Consultar puntos y logros (Detalle) (Diagram_ID 13) | CuentaPuntos.calcularSaldoContable() |
| HU-037: Configurar niveles e insignias | — | UR-18 | RF-05-7 | — | CU-G07 - Consultar puntos y logros (Detalle) (Diagram_ID 13) | Nivel.definirUmbral() |
| HU-038: Revertir puntos de acciones invalidadas | — | UR-47 | RF-05-8 | RNF-06, RNF-12 | CU-G07 - Consultar puntos y logros (Detalle) (Diagram_ID 13) | CuentaPuntos.revertir() |
| HU-039: Inscribirme y avanzar en capacitaciones | — | UR-20 | RF-06-1 | RNF-17 | CU-G08 - Participar en capacitaciones (Detalle) (Diagram_ID 50) | Capacitacion.puedeInscribirse() |
| HU-040: Realizar módulos y registrar avance | HU-039: Inscribirme y avanzar en capacitaciones | UR-21 | RF-06-2 | RNF-17 | CU-G08 - Participar en capacitaciones (Detalle) (Diagram_ID 50) | InscripcionCapacitacion.calcularAvance() |
| HU-041: Rendir la evaluación de una capacitación | — | UR-22 | RF-06-3 | RNF-17 | CU-G08 - Participar en capacitaciones (Detalle) (Diagram_ID 50) | IntentoEvaluacion.calificar() |
| HU-042: Emitir, consultar y descargar certificados | — | UR-23 | RF-06-4 | RNF-16 | CU-G08 - Participar en capacitaciones (Detalle) (Diagram_ID 50) | Certificado.emitir() |
| HU-043: Consultar y descargar certificados | HU-042: Emitir, consultar y descargar certificados | UR-23 | RF-06-5 | RNF-10 | CU-G08 - Participar en capacitaciones (Detalle) (Diagram_ID 50) | Certificado.obtenerDocumento() |
| HU-044: Gestionar y supervisar capacitaciones | — | UR-24 | RF-06-6 | RNF-26 | CU-G19 - Gestionar capacitaciones y talleres (Detalle) (Diagram_ID 51) | Capacitacion.publicar() |
| HU-045: Verificar la autenticidad de un certificado | — | UR-23 | RF-06-7 | RNF-16, RNF-21 | CU-G19 - Gestionar capacitaciones y talleres (Detalle) (Diagram_ID 51) | Certificado.verificarAutenticidad() |
| HU-046: Gestionar talleres | — | UR-48 | RF-06-8 | — | CU-G19 - Gestionar capacitaciones y talleres (Detalle) (Diagram_ID 51) | Taller.programar() |
| HU-047: Inscribirse en talleres y registrar asistencia | — | UR-49 | RF-06-9 | RNF-12 | CU-G08 - Participar en capacitaciones (Detalle) (Diagram_ID 50) | InscripcionTaller.registrarAsistencia() |
| HU-048: Configurar sorteos | — | UR-25 | RF-07-1 | RNF-06 | CU-G20 - Gestionar sorteos (Detalle) (Diagram_ID 53) | Sorteo.configurar() |
| HU-049: Generar participaciones en sorteos | — | UR-26 | RF-07-2 | RNF-06 | CU-G09 - Participar en sorteos (Detalle) (Diagram_ID 52) | ParticipacionSorteo.validarOrigen() |
| HU-050: Ejecutar sorteos, notificar ganadores y auditar resultados | — | UR-27 | RF-07-3 | RNF-13, RNF-22 | CU-G20 - Gestionar sorteos (Detalle) (Diagram_ID 53) | Sorteo.ejecutar() |
| HU-051: Consultar resultados de sorteos | — | UR-28 | RF-07-4 | RNF-14 | CU-G09 - Participar en sorteos (Detalle) (Diagram_ID 52) | ResultadoSorteo.obtenerDatosPublicos() |
| HU-052: Notificar a los ganadores | HU-050: Ejecutar sorteos, notificar ganadores y auditar resultados | UR-28 | RF-07-5 | RNF-18 | CU-G20 - Gestionar sorteos (Detalle) (Diagram_ID 53) | EnvioNotificacion.programar() |
| HU-053: Consultar el historial de sorteos | HU-050: Ejecutar sorteos, notificar ganadores y auditar resultados | UR-27 | RF-07-6 | RNF-13 | CU-G20 - Gestionar sorteos (Detalle) (Diagram_ID 53) | EvidenciaSorteo.verificarIntegridad() |
| HU-054: Configurar beneficios | — | UR-31 | RF-08-1 | RNF-06 | CU-G21 - Administrar canjes y recompensas (Detalle) (Diagram_ID 55) | Beneficio.configurar() |
| HU-055: Solicitar canjes con reserva, descuento y liberación segura de puntos | — | UR-30 | RF-08-2 | RNF-12, RNF-17 | CU-G10 - Solicitar canje de recompensas (Detalle) (Diagram_ID 54) | Canje.solicitar() |
| HU-056: Gestionar y entregar canjes | — | UR-31 | RF-08-3 | RNF-06, RNF-13 | CU-G21 - Administrar canjes y recompensas (Detalle) (Diagram_ID 55) | Canje.aprobar() |
| HU-057: Consultar beneficios disponibles | — | UR-29 | RF-08-4 | RNF-03 | CU-G10 - Solicitar canje de recompensas (Detalle) (Diagram_ID 54) | Beneficio.estaDisponible() |
| HU-058: Consultar historial de canjes | — | UR-32 | RF-08-5 | RNF-13 | CU-G21 - Administrar canjes y recompensas (Detalle) (Diagram_ID 55) | Canje.consultarEstado() |
| HU-059: Reservar, descontar y liberar puntos de canjes | HU-055: Solicitar canjes con reserva, descuento y liberación segura de puntos | UR-30 | RF-08-6 | RNF-12 | CU-G21 - Administrar canjes y recompensas (Detalle) (Diagram_ID 55) | CuentaPuntos.confirmarDescuento() |
| HU-060: Gestionar, publicar y programar contenidos institucionales | — | UR-33 | RF-09-1 | RNF-20 | CU-G22 - Publicar noticias y materiales (Detalle) (Diagram_ID 28) | ContenidoInstitucional.retirar() |
| HU-061: Publicar noticias y comunicados | HU-060: Gestionar, publicar y programar contenidos institucionales | UR-33 | RF-09-2 | RNF-20 | CU-G22 - Publicar noticias y materiales (Detalle) (Diagram_ID 28) | ContenidoInstitucional.publicar() |
| HU-062: Gestionar materiales educativos | — | UR-34 | RF-09-3 | RNF-26 | CU-G22 - Publicar noticias y materiales (Detalle) (Diagram_ID 28) | MaterialEducativo.esAdmisible() |
| HU-063: Consultar contenido institucional | — | UR-35 | RF-09-4 | RNF-03 | CU-G11 - Consultar noticias y notificaciones (Detalle) (Diagram_ID 17) | ContenidoInstitucional.esVisible() |
| HU-064: Gestionar la vigencia de contenidos | HU-060: Gestionar, publicar y programar contenidos institucionales | UR-33 | RF-09-5 | — | CU-G22 - Publicar noticias y materiales (Detalle) (Diagram_ID 28) | ContenidoInstitucional.esVisible() |
| HU-065: Aprobar contenido antes de publicarlo | — | UR-33 | RF-09-6 | — | CU-G22 - Publicar noticias y materiales (Detalle) (Diagram_ID 28) | AprobacionContenido.aprobar() |
| HU-066: Gestionar plantillas de notificación | — | UR-36 | RF-10-1 | — | CU-G11 - Consultar noticias y notificaciones (Detalle) (Diagram_ID 17) | PlantillaNotificacion.definirContenido() |
| HU-067: Gestionar preferencias de notificación | — | UR-37 | RF-10-2 | — | CU-G11 - Consultar noticias y notificaciones (Detalle) (Diagram_ID 17) | PreferenciaNotificacion.permiteEnvio() |
| HU-068: Enviar notificaciones automáticas | — | UR-36 | RF-10-3 | RNF-18 | CU-G11 - Consultar noticias y notificaciones (Detalle) (Diagram_ID 17) | EnvioNotificacion.puedeReintentarse() |
| HU-069: Consultar la bandeja de notificaciones | — | UR-38 | RF-10-4 | RNF-10 | CU-G11 - Consultar noticias y notificaciones (Detalle) (Diagram_ID 17) | Notificacion.marcarLeida() |
| HU-070: Consultar el historial de envíos | — | UR-36 | RF-10-5 | RNF-18 | CU-G11 - Consultar noticias y notificaciones (Detalle) (Diagram_ID 17) | EnvioNotificacion.consultarHistorial() |
| HU-071: Registrar y administrar juegos educativos | — | UR-39 | RF-11-1 | — | CU-G23 - Gestionar juegos y retos (Detalle) (Diagram_ID 29) | Juego.activar() |
| HU-072: Registrar juegos de tipos predefinidos | HU-071: Registrar y administrar juegos educativos | UR-39 | RF-11-2 | — | CU-G23 - Gestionar juegos y retos (Detalle) (Diagram_ID 29) | Juego.definirContenido() |
| HU-073: Participar en juegos con resultados y límite de intentos | — | UR-40 | RF-11-3 | RNF-03 | CU-G12 - Participar en juegos y comunidad (Detalle) (Diagram_ID 56) | Juego.admitePartida() |
| HU-074: Finalizar partida y calcular resultado | HU-073: Participar en juegos con resultados y límite de intentos | UR-40 | RF-11-4 | RNF-20 | CU-G12 - Participar en juegos y comunidad (Detalle) (Diagram_ID 56) | Partida.calcularResultado() |
| HU-075: Registrar resultados de juegos | — | UR-41 | RF-11-5 | RNF-12 | CU-G23 - Gestionar juegos y retos (Detalle) (Diagram_ID 29) | Partida.habilitaReconocimiento() |
| HU-076: Validar el límite de intentos | HU-073: Participar en juegos con resultados y límite de intentos | UR-40 | RF-11-6 | — | CU-G12 - Participar en juegos y comunidad (Detalle) (Diagram_ID 56) | Juego.calcularIntentosRestantes() |
| HU-077: Gestionar retos | — | UR-50 | RF-11-7 | — | CU-G23 - Gestionar juegos y retos (Detalle) (Diagram_ID 29) | Reto.definirObjetivo() |
| HU-078: Participar en retos | — | UR-51 | RF-11-8 | RNF-12 | CU-G12 - Participar en juegos y comunidad (Detalle) (Diagram_ID 56) | ProgresoReto.reconocerCumplimiento() |
| HU-079: Publicar e interactuar en la comunidad | — | UR-52 | RF-12-1 | RNF-20, RNF-26 | CU-G12 - Participar en juegos y comunidad (Detalle) (Diagram_ID 56) | PublicacionComunidad.publicar() |
| HU-080: Interactuar con publicaciones | HU-079: Publicar e interactuar en la comunidad | UR-52 | RF-12-2 | RNF-20 | CU-G12 - Participar en juegos y comunidad (Detalle) (Diagram_ID 56) | PublicacionComunidad.admiteInteraccion() |
| HU-081: Reportar contenido inapropiado | HU-082: Gestionar reportes y moderar la comunidad | UR-52 | RF-12-3 | RNF-06 | CU-G24 - Moderar publicaciones (Detalle) (Diagram_ID 57) | ReporteComunidad.enviarAModeracion() |
| HU-082: Gestionar reportes y moderar la comunidad | — | UR-53 | RF-12-4 | RNF-06, RNF-14 | CU-G24 - Moderar publicaciones (Detalle) (Diagram_ID 57) | DecisionModeracion.aplicar() |
| HU-083: Configurar el perfil público | — | UR-52 | RF-12-5 | RNF-14 | CU-G12 - Participar en juegos y comunidad (Detalle) (Diagram_ID 56) | PerfilPublico.definirPrivacidad() |
| HU-084: Gestionar convenios de bienestar | — | UR-55 | RF-13-1 | RNF-24, RNF-26 | CU-G13 - Consultar beneficios de bienestar (Detalle) (Diagram_ID 19) | ConvenioBienestar.configurar() |
| HU-085: Consultar convenios y contenidos de bienestar | — | UR-54 | RF-13-2 | RNF-24 | CU-G13 - Consultar beneficios de bienestar (Detalle) (Diagram_ID 19) | RecursoBienestar.esVisible() |
| HU-086: Vincular convenios a recompensas | — | UR-55 | RF-13-3 | — | CU-G13 - Consultar beneficios de bienestar (Detalle) (Diagram_ID 19) | ConvenioBienestar.habilitaBeneficio() |
| HU-087: Visualizar el panel de supervisión | — | UR-56 | RF-14-1 | RNF-04 | CU-G25 - Consultar reportes y estadísticas (Detalle) (Diagram_ID 31) | ServicioReportes.generarSupervision() |
| HU-088: Generar reporte de referidos y campañas | — | UR-46 | RF-14-2 | RNF-14 | CU-G25 - Consultar reportes y estadísticas (Detalle) (Diagram_ID 31) | ServicioReportes.generarReferidosCampanas() |
| HU-089: Generar reporte de impacto social | — | UR-57 | RF-14-3 | RNF-14 | CU-G25 - Consultar reportes y estadísticas (Detalle) (Diagram_ID 31) | ServicioReportes.generarImpactoSocial() |
| HU-090: Generar reporte de gamificación y recompensas | — | UR-42 | RF-14-4 | RNF-14 | CU-G25 - Consultar reportes y estadísticas (Detalle) (Diagram_ID 31) | ServicioReportes.generarGamificacion() |
| HU-091: Exportar reportes en PDF y Excel/CSV | — | UR-42 | RF-14-5 | RNF-14, RNF-20 | CU-G25 - Consultar reportes y estadísticas (Detalle) (Diagram_ID 31) | ServicioReportes.exportar() |

## Elementos reales de casos de uso identificados en EA

Se verificó que cada elemento principal aparece en su diagrama de detalle mediante t_diagramobjects. Los GUID siguientes se leyeron del repositorio; no son vínculos nuevos. La relación de estas clases propuestas a esos elementos todavía debe crearse.

| Código del título | Diagram_ID | Object_ID principal | Nombre del UseCase | GUID del UseCase |
| --- | --- | --- | --- | --- |
| CU-G01 | 7 | 33 | Iniciar Sesión | `{6D91192E-C2B7-4651-AFEC-E5B27BC6CEEB}` |
| CU-G02 | 40 | 48 | Gestionar perfil | `{CAE9084E-0BFE-42fe-8BEE-6AA7910E90CD}` |
| CU-G03 | 42 | 49 | Generar código de referido | `{C4D17016-2041-4731-A119-424A73BE63D6}` |
| CU-G04 | 43 | 51 | Registrar persona referida | `{8C295FFF-5DD2-4327-A88A-D8EA0A13230A}` |
| CU-G05 | 44 | 52 | Consultar estado de referidos | `{23E3FCE3-0CE7-4fb4-AA5D-B9873F3FE1CF}` |
| CU-G06 | 48 | 53 | Participar en campañas | `{2170BCDE-0F71-445e-B36F-0DC65675DE1B}` |
| CU-G07 | 13 | 54 | Consultar puntos y logros | `{7AE62876-064E-40e4-B88F-0C238B279088}` |
| CU-G08 | 50 | 55 | Participar en capacitaciones | `{F9DAA354-B44D-4e17-BD48-FFDB3A742D53}` |
| CU-G09 | 52 | 56 | Participar en sorteos | `{A4300719-E0C4-4269-A4DB-6212B498977D}` |
| CU-G10 | 54 | 57 | Solicitar canje de recompensas | `{D90BF38E-9AAF-4771-9862-630D44DB47DA}` |
| CU-G11 | 17 | 58 | Consultar noticias y notificaciones | `{84B54BB4-E6B9-43dc-A927-CF8BF0A0ADC8}` |
| CU-G12 | 56 | 59 | Participar en juegos y comunidad | `{AA04FF08-39B3-409a-9572-3288B2217489}` |
| CU-G13 | 19 | 60 | Consultar beneficios de bienestar | `{2D0F76BF-BE97-46d2-894C-F27E822C1FB9}` |
| CU-G14 | 45 | 61 | Consultar prospectos referidos | `{3C85FC6F-7BC4-47d5-BD32-E953DAFF8DB7}` |
| CU-G15 | 46 | 62 | Validar registros de referidos | `{BE3CB42A-BD3C-4901-8B79-8D0BEF580D21}` |
| CU-G16 | 47 | 63 | Confirmar conversión a socio | `{783FB1F1-647F-4d04-A92A-54153E5FEFDF}` |
| CU-G17 | 41 | 64 | Administrar usuarios y permisos | `{1C0A5B1D-F94E-4426-8568-7096C6296A20}` |
| CU-G18 | 49 | 73 | Gestionar Campañas e incentivos | `{80041D5A-1A78-4ce2-9DA6-3A199D25D691}` |
| CU-G19 | 51 | 65 | Gestionar capacitaciones y talleres | `{EF335EC4-E148-4a15-B666-7EF7CFAFA6D2}` |
| CU-G20 | 53 | 66 | Gestionar sorteos | `{D2B6D6E6-3212-474d-A52D-599C77DC6A72}` |
| CU-G21 | 55 | 67 | Administrar canjes y recompensas | `{ED7DF65A-6252-430c-9380-911AD3781BAF}` |
| CU-G22 | 28 | 68 | Publicar noticias y materiales | `{2E7827E8-4CB4-4773-8E07-E81A11B6E5DB}` |
| CU-G23 | 29 | 70 | Gestionar juegos y retos | `{9D6B4F61-60DA-48c6-8563-A98CD6B6DB3A}` |
| CU-G24 | 57 | 71 | Moderar publicaciones | `{62394965-B392-4f06-9FB1-A15129BCCDE2}` |
| CU-G25 | 31 | 72 | Consultar reportes y estadísticas | `{116106F1-A85E-4fd6-913C-2EB3929C5FEA}` |

## Reglas de lectura y cobertura

La fuente de cada fila es `documentacion/product_con_subtareas.csv`, identificada por su HU y su Work item ID en el archivo. Cada operación figura con firma completa en CATALOGO-CLASES.md; sus atributos, asociaciones e invariantes completan el significado de la fila. Una operación representativa no cubre por sí sola todos los criterios de una historia.

| HU | Regla o soporte adicional para evaluar cobertura |
| --- | --- |
| HU-001 | Datos de Usuario y ConsentimientoCuenta; alta coordinada por registro_service.py, operación de registro a modelar como servicio si se requiere |
| HU-002 | Datos de Usuario y titularidad; consulta del perfil |
| HU-005 | Datos de Usuario, Rol y EventoAuditoria; alta/edición administrativa requiere coordinación adicional |
| HU-008 | Restricciones únicas de cedula/correo/nombreUsuario y alta atómica |
| HU-012 | Asociación Usuario–Rol; obtención de roles y unión de accesos |
| HU-013 | Asociaciones Usuario–Rol–Permiso; administración de asignaciones, no solamente consulta habilita |
| HU-016 | Generación única no secuencial y asociación a Socio; esValido solo representa validación del valor |
| HU-021 | Consulta por titularidad e historial enmascarado |
| HU-025 | Atributos de Campana y configuración previa a activar |
| HU-031 | Configuración/versionado de ReglaPuntos además de calcularPuntos |
| HU-033 | Insignia, InsigniaObtenida y notificación además de Nivel |
| HU-037 | Configuración de Nivel e Insignia además de evaluar criterio |
| HU-046 | Configuración de Taller además del cálculo de cupos |
| HU-048 | Configuración de Sorteo y PremioSorteo además de elegibilidad |
| HU-054 | Configuración de Beneficio además de disponibilidad |
| HU-058 | Consulta de canjes por titular y filtro de estado |
| HU-066 | Configuración de PlantillaNotificacion además de preparación de mensaje |
| HU-070 | Consulta autorizada de envíos y filtros, no solo registro de resultado |
| HU-072 | Configuración de Juego/Pregunta/OpcionPregunta además de evaluar respuesta |
| HU-077 | Configuración de Reto además de comprobar cumplimiento |
| HU-084 | Configuración de ConvenioBienestar y prohibición de datos clínicos además de vigencia |

## Estado y fuentes de evidencia

| Ámbito | Estado observado | Fuente y límite |
| --- | --- | --- |
| Registro, padrón, login, roles actuales y sesiones | Implementado en el alcance descrito por Sprint 1 | matriz-trazabilidad.md y servicios de usuarios; pruebas referenciadas, no ejecutadas en esta revisión |
| Recuperación de acceso | Implementación existente revisada | recuperacion_service.py y TokenRecuperacion; no equivale al módulo general de notificaciones |
| Administración completa de usuarios, estados y permisos | Parcial / planificada según operación | Crear personal existe como comando/servicio; no afirmar CRUD administrativo completo por las pantallas de ejemplo |
| Conversión administrativa temporal | Implementada, ampliación posterior | conversion-administrativa-temporal.md; no tiene HU original equivalente exacta y no sustituye HU-018 |
| Referidos, campañas, puntos, formación, sorteos, canjes, contenido, comunidad, juegos, bienestar, reportes y notificaciones generales | Planificados con diseño parcial y pantallas demostrativas | CSV, SQL 01–02, demo.js; clases y operaciones del catálogo son propuestas, no evidencia operativa |

## Trazabilidad pendiente de crear dentro de EA

Crear enlaces nativos hacia los elementos reales de CU y requisitos, registrar GUID, y verificar por criterio de aceptación. El inventario conserva datos de consulta pero no certifica enlaces nuevos. El proceso administrativo temporal debe usar una referencia local de decisión, sin inventarle un RF/HU del backlog. Los conceptos auxiliares propuestos justifican su existencia por las HU de sus clases relacionadas y deben anotarse así en EA.
