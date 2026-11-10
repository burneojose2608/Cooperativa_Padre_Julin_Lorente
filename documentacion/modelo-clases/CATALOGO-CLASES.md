# Catálogo propuesto de clases de negocio

Modelo de análisis del alcance completo, revisado el 10 de noviembre de 2026. Las operaciones son responsabilidades propuestas; no constituyen un inventario literal de métodos del código. Los módulos posteriores a identidad/seguridad están planificados. Consultar DECISIONES-Y-REGLAS.md para evidencia, brechas y políticas pendientes.

Todos los atributos y operaciones no implementados explícitamente en la fuente citada son propuestas derivadas de requisitos. La misma clase puede combinar atributos existentes y planificados. No equivale a una especificación física completa de base de datos.

Convención: `- atributo: Tipo`, `+ operacion(parametro: Tipo): Retorno`; `/` marca un valor derivado; `[0..1]` indica dato opcional. Los registros inmutables pueden carecer de operaciones propias. `Identificador`, `Recurso`, `Referencia`, `Condiciones`, `DatosRegistro`, `DatosPerfil`, `DatosEvento`, `DatosSeguimiento`, `DatosPublicos`, `DatosEnmascarados`, `Indicador`, `Criterio` y `PosicionPublica` son tipos de análisis auxiliares, cuyo detalle debe concretarse si aporta comprensión; no son clases implementadas. `Secreto` es un dato transitorio de entrada. No se modela almacenamiento de contraseñas en claro.

No todas las relaciones son persistentes. CuentaPuntos, Clasificacion y ControlAcceso agrupan responsabilidades conceptuales. EntradaPadron se consulta por cédula; no se exige una FK permanente desde cada usuario. Los métodos de configuración describen cambios con sentido de negocio y permisos, sin operaciones de persistencia genéricas.


Inventario: **70 clases**, **94 asociaciones** y **31 dependencias** propuestas. Las enumeraciones se definen en DECISIONES-Y-REGLAS.md.


## Identidad


### Usuario

Estereotipo propuesto: `Entidad`. Titular de la cuenta. Campos principales implementados; foto y gestión completa de estado/contacto son planificados. HU-001–008; models/usuario.py. Secreto es un parámetro transitorio, nunca un atributo público ni texto almacenado.


```text
- id: Identificador
- cedula: Texto
- nombres: Texto
- apellidos: Texto
- correo: Texto
- nombreUsuario: Texto
- telefono: Texto
- fechaNacimiento: Fecha
- estado: EstadoCuenta
- foto: Recurso [0..1]

+ calcularEdad(fecha: Fecha): Entero
+ actualizarContacto(correo: Texto, telefono: Texto, foto: Recurso [0..1]): Booleano
+ cambiarContrasena(actual: Secreto, nueva: Secreto): Booleano
+ cambiarEstado(estado: EstadoCuenta, motivo: Texto, responsable: Usuario): Booleano
+ consultarPerfil(solicitante: Usuario): DatosPerfil
```


### Socio

Estereotipo propuesto: `Entidad`. Condición cooperativa asociada a una cuenta. Código y validación implementados; datos de segmentación propuestos y pendientes de fuente P05. models/socio.py; HU-028.


```text
- codigoSocio: Texto
- validadoEn: FechaHora
- tipoSocio: Texto [0..1]
- agencia: Texto [0..1]
- productosSegmentacion: Conjunto<Texto>

+ esElegibleParaParticipar(fecha: FechaHora): Booleano
```


### Rol

Estereotipo propuesto: `Entidad`. Conjunto de autorizaciones. Roles múltiples implementados; administración completa de permisos planificada. HU-012–014.


```text
- nombre: Texto

+ habilita(permiso: Permiso): Booleano
```


### Permiso

Estereotipo propuesto: `Entidad`. Capacidad autorizada; diseño SQL permiso/rol_permiso y HU-013. No presupone administración operativa completa.


```text
- codigo: Texto
- descripcion: Texto

+ permiteAccion(accion: Texto): Booleano
```


### ConsentimientoCuenta

Estereotipo propuesto: `Registro`. Evidencia de aceptación de la cuenta. Fecha y versión implementadas; finalidad explícita propuesta. HU-001.


```text
- versionPolitica: Texto
- finalidad: Texto
- aceptadoEn: FechaHora

+ acreditaAceptacion(version: Texto): Booleano
```


### EntradaPadron

Estereotipo propuesto: `Entidad`. Registro de prueba independiente de cuentas. No encontrado es resultado de consulta, no una fila ficticia. HU-006; models/padron.py.


```text
- cedula: Texto
- activo: Booleano

+ habilitaCondicionSocio(): Booleano
```


### ValidacionAdministrativaSocio

Estereotipo propuesto: `Entidad`. Concepto propuesto para explicar proceso manual temporal ya implementado por servicio y auditoría; no afirma tabla propia. No acredita puntos de referidos.


```text
- fecha: FechaHora
- confirmacionExpresa: Booleano
- resultado: Texto

+ validarYHabilitar(cuenta: Usuario, administrador: Usuario): Socio
```


## Seguridad


### Sesion

Estereotipo propuesto: `Entidad`. Sesión revocable implementada; iniciadaEn es atributo conceptual propuesto. No almacena JWT en claro. HU-009/HU-015; models/sesion.py.


```text
- iniciadaEn: FechaHora
- venceEn: FechaHora
- ultimoUso: FechaHora [0..1]
- revocadaEn: FechaHora [0..1]

+ estaVigente(ahora: FechaHora): Booleano
+ registrarActividad(ahora: FechaHora): Booleano
+ cerrar(ahora: FechaHora): Booleano
+ expirarPorInactividad(ahora: FechaHora): Booleano
```


### RecuperacionAcceso

Estereotipo propuesto: `Entidad`. Enlace de un uso, modelo TokenRecuperacion y servicio existentes. HU-011. Vigencia actual 30 minutos en servicio; no extender a todos los consentimientos.


```text
- solicitadaEn: FechaHora
- venceEn: FechaHora
- usadaEn: FechaHora [0..1]
- huellaEnlace: Texto

+ esUtilizable(ahora: FechaHora): Booleano
+ restablecerContrasena(nueva: Secreto): Booleano
```


### ControlAcceso

Estereotipo propuesto: `Entidad`. Responsabilidad conceptual agrupada de servicios existentes; estado de fallos físicamente en Usuario. HU-009/HU-010/HU-014. Permisos dinámicos completos no se presuponen implementados.


```text
- intentosFallidos: Entero
- bloqueadoHasta: FechaHora [0..1]

+ validarCredenciales(identificador: Texto, clave: Secreto): Sesion
+ registrarIntentoFallido(ahora: FechaHora): Booleano
+ autorizar(usuario: Usuario, accion: Texto, recurso: Referencia): Booleano
+ registrarCuenta(datos: DatosRegistro, consentimiento: ConsentimientoCuenta): Usuario
+ validarUnicidad(datos: DatosRegistro): Booleano
+ registrarPersonal(datos: DatosRegistro, roles: Coleccion<Rol>, administrador: Usuario): Usuario
+ identificarRoles(usuario: Usuario): Coleccion<Rol>
+ asignarRol(usuario: Usuario, rol: Rol, administrador: Usuario): Booleano
+ revocarRol(usuario: Usuario, rol: Rol, administrador: Usuario): Booleano
```


## Auditoria


### EventoAuditoria

Estereotipo propuesto: `Registro`. Registro inmutable; actor opcional para acciones anónimas. Implementado para eventos concretos, no interfaz general completa. models/auditoria.py; RNF-06.


```text
- accion: Texto
- entidad: Texto
- referencia: Texto [0..1]
- fecha: FechaHora
- resultado: Texto
- origenConexion: Texto [0..1]
(Sin operaciones propias: registro u objeto de datos.)
```


### CambioEstado

Estereotipo propuesto: `Registro`. Historial inmutable compartido por referido, campaña y canje. Diseño SQL historial_estado; motivo/observación propuestos por HU-024/HU-056.


```text
- entidad: Texto
- referencia: Texto
- anterior: Texto [0..1]
- nuevo: Texto
- fecha: FechaHora
- motivo: Texto [0..1]
(Sin operaciones propias: registro u objeto de datos.)
```


## Referidos


### CodigoReferido

Estereotipo propuesto: `Entidad`. Identificador comercial no secuencial distinto de codigoSocio. SQL permite historial y un código activo por socio. HU-016/HU-019; módulo planificado.


```text
- valor: Texto
- activo: Booleano

+ esValido(): Booleano
+ generarEnlace(base: Texto): Texto
+ generarPara(socio: Socio): CodigoReferido
```


### Prospecto

Estereotipo propuesto: `Entidad`. Persona recomendada sin cuenta obligatoria. HU-017/HU-020. Al menos un contacto; datos mínimos de comparación pendientes de precisar.


```text
- id: Identificador
- nombres: Texto
- huellaIdentificacion: Texto [0..1]
- telefono: Texto [0..1]
- correo: Texto [0..1]
- productoInteres: Texto [0..1]

+ coincideCon(persona: Referencia): Booleano
+ tieneContactoUtilizable(): Booleano
```


### ConsentimientoProspecto

Estereotipo propuesto: `Registro`. Objeto propuesto de evidencia de consentimiento para un referido; SQL 02 solo cubre parte de las fechas. HU-023; no reutiliza ConsentimientoCuenta.


```text
- finalidad: Texto
- versionPolitica: Texto
- solicitadoEn: FechaHora
- limiteConfirmacion: FechaHora
- aceptadoEn: FechaHora [0..1]

+ confirmar(ahora: FechaHora): Booleano
+ estaConfirmado(): Booleano
+ plazoVencido(ahora: FechaHora): Booleano
```


### Referido

Estereotipo propuesto: `Entidad`. Vínculo de recomendación. Valida código, autorreferido, padrón, duplicados y transición; conserva historial. HU-017–024; módulo planificado.


```text
- id: Identificador
- creadoEn: FechaHora
- estado: EstadoReferido

+ validarRegistro(): Booleano
+ confirmarConsentimiento(ahora: FechaHora): Booleano
+ iniciarSeguimiento(responsable: Usuario): Booleano
+ rechazar(motivo: Texto, responsable: Usuario): Booleano
+ expirar(ahora: FechaHora): Booleano
+ confirmarConversion(tipo: TipoConversion, evidencia: Texto, responsable: Usuario): Conversion
+ consultarSeguimiento(solicitante: Usuario): DatosSeguimiento
```


### Conversion

Estereotipo propuesto: `Registro`. Hecho comercial validado una vez por prospecto; dispara reconocimiento único. SQL conversion y HU-018; evidencia detallada propuesta.


```text
- tipo: TipoConversion
- validadaEn: FechaHora
- evidenciaPrueba: Texto
- claveOrigen: Texto

+ esReconocible(): Booleano
```


## Campanas


### Campana

Estereotipo propuesto: `Entidad`. Organiza objetivos, vigencia e incentivos. HU-025–030; planificado. unidadMeta propuesta pendiente de definición.


```text
- nombre: Texto
- tipo: Texto
- objetivo: Texto
- meta: Entero
- unidadMeta: Texto
- inicio: Fecha
- fin: Fecha
- estado: EstadoCampana

+ activar(fecha: Fecha): Booleano
+ suspender(motivo: Texto): Booleano
+ finalizar(fecha: Fecha): Booleano
+ admiteParticipacion(socio: Socio, fecha: Fecha): Booleano
+ modificarCondiciones(cambios: Condiciones, responsable: Usuario): Booleano
+ calcularTasaConversion(): Decimal
+ calcularAvanceMeta(): Decimal
```


### Segmento

Estereotipo propuesto: `Entidad`. Selecciona por edad, tipo de socio, producto y agencia; combinación de criterios pendiente P05. HU-028.


```text
- nombre: Texto
- criteriosAutorizados: Conjunto<Criterio>

+ incluye(socio: Socio, fecha: Fecha): Booleano
+ contarElegibles(socios: Coleccion<Socio>): Entero
```


### IncentivoCampana

Estereotipo propuesto: `Entidad`. Descomposición conceptual propuesta de incentivos de campaña (SQL los guarda como texto). Puntos o participaciones, sin efecto retroactivo. HU-025/HU-029.


```text
- tipo: Texto
- cantidad: Entero
- condiciones: Texto
- version: Texto
- vigenteDesde: Fecha
- vigenteHasta: Fecha [0..1]

+ correspondeA(actividad: ActividadValidada): Booleano
```


### ParticipacionCampana

Estereotipo propuesto: `Entidad`. Registro propuesto de participación validada para monitoreo y CU-G06. No se exige inscripción manual universal ni se afirma tabla existente.


```text
- registradaEn: FechaHora
- validadaEn: FechaHora [0..1]
- versionCondiciones: Texto

+ validarElegibilidad(fecha: Fecha): Booleano
```


## Gamificacion


### ActividadValidada

Estereotipo propuesto: `ObjetoValor`. Objeto de valor propuesto de enlace entre hechos de negocio y reconocimiento; no duplica sus registros operativos. HU-032/HU-049/HU-075/HU-078.


```text
- tipo: Texto
- referenciaOrigen: Texto
- fecha: FechaHora
- validada: Booleano

+ esReconocible(): Booleano
```


### ReglaPuntos

Estereotipo propuesto: `Entidad`. Regla sin efecto retroactivo. HU-031/HU-032; límites y versión no completos en SQL.


```text
- tipoActividad: Texto
- puntos: Entero
- limitePeriodo: Entero [0..1]
- periodo: Texto [0..1]
- vigenteDesde: Fecha
- vigenteHasta: Fecha [0..1]
- version: Texto

+ calcularPuntos(actividad: ActividadValidada, acumuladoPeriodo: Entero): Entero
+ estaVigente(fecha: Fecha): Booleano
+ configurarVersion(condiciones: Condiciones, administrador: Usuario): ReglaPuntos
```


### CuentaPuntos

Estereotipo propuesto: `Entidad`. Agregado conceptual propuesto, derivado del libro; no tabla de saldo. HU-032/HU-034/HU-036/HU-038/HU-059. Semántica de reserva según propuesta R6.


```text
- /saldoContable: Entero
- /saldoReservado: Entero
- /saldoDisponible: Entero

+ calcularSaldoContable(): Entero
+ calcularSaldoReservado(): Entero
+ calcularSaldoDisponible(): Entero
+ acreditar(actividad: ActividadValidada, regla: ReglaPuntos): MovimientoPuntos
+ reservar(canje: Canje, cantidad: Entero): MovimientoPuntos
+ confirmarDescuento(canje: Canje): MovimientoPuntos
+ liberarReserva(canje: Canje): MovimientoPuntos
+ revertir(original: MovimientoPuntos, motivo: Texto): MovimientoPuntos
```


### MovimientoPuntos

Estereotipo propuesto: `Registro`. Registro inmutable con cantidad positiva y signo semántico según tipo. Origen, beneficiario y reverso trazables; HU-036/HU-038/HU-059.


```text
- id: Identificador
- tipo: TipoMovimiento
- cantidad: Entero
- fecha: FechaHora
- claveIdempotencia: Texto
- motivo: Texto [0..1]
(Sin operaciones propias: registro u objeto de datos.)
```


### Nivel

Estereotipo propuesto: `Entidad`. Umbrales únicos. Base de puntos y descensos pendientes P06. HU-033/HU-037.


```text
- nombre: Texto
- umbralPuntos: Entero

+ seAlcanzaCon(puntosBase: Entero): Booleano
+ definirUmbral(puntos: Entero, administrador: Usuario): Booleano
```


### Insignia

Estereotipo propuesto: `Entidad`. Define logro; icono requerido por HU-037 aunque no completo en SQL. HU-033/HU-037.


```text
- nombre: Texto
- icono: Recurso
- criterio: Texto

+ seCumplePara(socio: Socio, actividades: Coleccion<ActividadValidada>): Booleano
+ definirCriterio(criterio: Texto, administrador: Usuario): Booleano
```


### InsigniaObtenida

Estereotipo propuesto: `Registro`. Registro único socio–insignia; no borrar al cambiar criterios. HU-033; SQL socio_insignia.


```text
- obtenidaEn: FechaHora
(Sin operaciones propias: registro u objeto de datos.)
```


### Clasificacion

Estereotipo propuesto: `Entidad`. Consulta derivada con alias y exclusión pública. No necesita tabla propia. Criterio y empates pendientes P06. HU-035.


```text
- desde: Fecha
- hasta: Fecha
- criterioOrden: Texto

+ calcularPosicion(socio: Socio): Entero
+ generarVistaPublica(): Coleccion<PosicionPublica>
```


## Formacion


### Capacitacion

Estereotipo propuesto: `Entidad`. Oferta de educación financiera. Varias propiedades derivadas de HU aún sin persistencia completa. HU-039/HU-044.


```text
- titulo: Texto
- descripcion: Texto
- duracionHoras: Decimal
- requisitos: Texto
- estado: Texto

+ puedeInscribirse(socio: Socio): Booleano
+ publicar(responsable: Usuario): Booleano
+ calcularTasaAprobacion(): Decimal
```


### ModuloCapacitacion

Estereotipo propuesto: `Entidad`. Corresponde a unidad del SQL; obligatoriedad propuesta para explicar avance. HU-040/HU-044.


```text
- titulo: Texto
- orden: Entero
- obligatorio: Booleano

+ estaCompletado(progreso: ProgresoModulo): Booleano
```


### InscripcionCapacitacion

Estereotipo propuesto: `Entidad`. Vínculo único socio–capacitación. Fórmula y acceso a evaluación por definir P06. HU-039–041.


```text
- fecha: FechaHora
- estado: Texto
- /porcentajeAvance: Decimal

+ completarModulo(modulo: ModuloCapacitacion): ProgresoModulo
+ calcularAvance(): Decimal
+ puedeRendir(evaluacion: Evaluacion): Booleano
```


### ProgresoModulo

Estereotipo propuesto: `Entidad`. Seguimiento por inscripción y módulo; entre 0 y 100. HU-040; SQL progreso.


```text
- porcentaje: Decimal
- completadoEn: FechaHora [0..1]

+ registrarFinalizacion(ahora: FechaHora): Booleano
```


### Evaluacion

Estereotipo propuesto: `Entidad`. Calificación en servidor y límite. HU-041/HU-044; reglas y máximo no completos en SQL.


```text
- notaMinima: Decimal
- maximoIntentos: Entero
- reglasCalificacion: Texto

+ permiteNuevoIntento(inscripcion: InscripcionCapacitacion): Booleano
+ calcularNota(respuestas: Coleccion<RespuestaActividad>): Decimal
```


### IntentoEvaluacion

Estereotipo propuesto: `Entidad`. Intento asociado a inscripción y evaluación; aprobación válida genera actividad única. HU-041.


```text
- numero: Entero
- iniciadoEn: FechaHora
- finalizadoEn: FechaHora [0..1]
- nota: Decimal [0..1]
- aprobado: Booleano [0..1]

+ calificar(): Decimal
+ alcanzaAprobacion(): Booleano
```


### Certificado

Estereotipo propuesto: `Entidad`. Solo tras aprobar, código único no secuencial y acceso al documento autorizado. HU-042/HU-043/HU-045.


```text
- codigoVerificacion: Texto
- emitidoEn: FechaHora
- documento: Recurso

+ emitir(inscripcion: InscripcionCapacitacion): Booleano
+ verificarAutenticidad(codigo: Texto): Booleano
+ obtenerDocumento(solicitante: Usuario): Recurso
```


### Taller

Estereotipo propuesto: `Entidad`. Actividad con aforo; sin integración de videoconferencia inventada. HU-046/HU-047.


```text
- titulo: Texto
- modalidad: Texto
- lugarOEnlace: Texto
- fecha: FechaHora
- cupo: Entero
- estado: Texto

+ calcularCuposDisponibles(): Entero
+ admiteInscripcion(socio: Socio): Booleano
+ programar(condiciones: Condiciones, responsable: Usuario): Booleano
```


### InscripcionTaller

Estereotipo propuesto: `Entidad`. Representa inscripción y asistencia (tabla asistencia_taller). Una por socio–taller, premio una vez. HU-047.


```text
- inscritaEn: FechaHora
- asistio: Booleano
- asistenciaRegistradaEn: FechaHora [0..1]

+ registrarAsistencia(responsable: Usuario): Booleano
+ habilitaReconocimiento(): Booleano
```


## Preguntas


### Pregunta

Estereotipo propuesto: `Entidad`. Propietario exclusivo evaluación XOR juego según SQL 02. Parejas para emparejar pendientes P08. HU-041/HU-072.


```text
- enunciado: Texto
- tipo: Texto
- criterioCorreccion: Texto

+ evaluar(respuesta: RespuestaActividad): Decimal
```


### OpcionPregunta

Estereotipo propuesto: `Entidad`. Alternativa de pregunta. SQL solo permite una correcta; no extrapolar a todos los juegos. HU-041/HU-072.


```text
- texto: Texto
- correcta: Booleano
(Sin operaciones propias: registro u objeto de datos.)
```


### RespuestaActividad

Estereotipo propuesto: `ObjetoValor`. Objeto de valor propuesto, propiedad exclusiva de un intento de evaluación o una partida; referencia la pregunta respondida. HU-041/HU-074.


```text
- contenido: Texto
- respondidaEn: FechaHora
(Sin operaciones propias: registro u objeto de datos.)
```


## Sorteos


### Sorteo

Estereotipo propuesto: `Entidad`. Ejecución única con lista congelada y selección segura. HU-048–053; campos de evidencia son propuesta, no funcionalidad existente.


```text
- nombre: Texto
- fecha: FechaHora
- condiciones: Texto
- numeroGanadores: Entero
- numeroSuplentes: Entero
- estado: Texto

+ verificarElegibilidad(socio: Socio): Booleano
+ congelarElegibles(): EvidenciaSorteo
+ ejecutar(responsable: Usuario): Coleccion<ResultadoSorteo>
+ publicarResultados(): Booleano
+ configurar(condiciones: Condiciones, responsable: Usuario): Booleano
```


### ParticipacionSorteo

Estereotipo propuesto: `Entidad`. Participación por socio, sorteo y actividad; sin duplicados no permitidos. HU-049.


```text
- registradaEn: FechaHora
- claveOrigen: Texto
- elegibleAlCierre: Booleano

+ validarOrigen(): Booleano
```


### PremioSorteo

Estereotipo propuesto: `Entidad`. Premio configurado; SQL 02 premio_sorteo. HU-048/HU-052.


```text
- descripcion: Texto
- posicion: Entero
- condicionesReclamo: Texto
(Sin operaciones propias: registro u objeto de datos.)
```


### EvidenciaSorteo

Estereotipo propuesto: `Registro`. Registro propuesto para lista congelada, proceso y resultado; conservar inmutable tras ejecución. HU-050/HU-053.


```text
- listaCongelada: Coleccion<Texto>
- hashLista: Texto
- congeladaEn: FechaHora
- ejecutadoEn: FechaHora [0..1]
- referenciaMetodoSeleccion: Texto

+ verificarIntegridad(): Booleano
```


### ResultadoSorteo

Estereotipo propuesto: `Registro`. Vincula participación de ese mismo sorteo; premio opcional para suplente. HU-050/HU-051; SQL ganador.


```text
- posicion: Entero
- esSuplente: Booleano
- registradoEn: FechaHora

+ obtenerDatosPublicos(): DatosEnmascarados
```


## Recompensas


### Beneficio

Estereotipo propuesto: `Entidad`. Stock nulo puede representar ilimitado según SQL; política de costo cero pendiente P02. Convenio vencido bloquea disponibilidad. HU-054/HU-057/HU-086.


```text
- nombre: Texto
- descripcion: Texto
- costoPuntos: Entero
- stock: Entero [0..1]
- condiciones: Texto
- inicio: Fecha [0..1]
- fin: Fecha [0..1]
- activo: Booleano

+ estaDisponible(fecha: Fecha): Booleano
+ cumpleCondiciones(socio: Socio): Booleano
+ calcularStockDisponible(): Entero
+ configurar(condiciones: Condiciones, responsable: Usuario): Booleano
```


### Canje

Estereotipo propuesto: `Entidad`. Coordina reserva, descuento/liberación y stock con CuentaPuntos; evidencia de condiciones propuesta. HU-055/HU-056/HU-058/HU-059.


```text
- solicitadoEn: FechaHora
- puntosComprometidos: Entero
- condicionesReconocidas: Texto
- estado: EstadoCanje
- entregadoEn: FechaHora [0..1]

+ solicitar(): Booleano
+ aprobar(responsable: Usuario): Booleano
+ rechazar(motivo: Texto, responsable: Usuario): Booleano
+ registrarEntrega(responsable: Usuario): Booleano
+ consultarEstado(solicitante: Usuario): EstadoCanje
```


## Contenidos


### ContenidoInstitucional

Estereotipo propuesto: `Entidad`. Noticias, comunicados y multimedia; distinta de publicación comunitaria. HU-060/HU-061/HU-063/HU-064/HU-065.


```text
- titulo: Texto
- cuerpo: Texto
- categoria: Texto
- tipo: Texto
- estado: Texto
- desde: Fecha [0..1]
- hasta: Fecha [0..1]
- requiereAprobacion: Booleano

+ solicitarAprobacion(): Booleano
+ publicar(responsable: Usuario): Booleano
+ retirar(motivo: Texto): Booleano
+ esVisible(fecha: Fecha): Booleano
```


### AprobacionContenido

Estereotipo propuesto: `Registro`. Evidencia propuesta de aprobación opcional por responsable designado; no tabla existente confirmada. HU-065.


```text
- decididaEn: FechaHora
- decision: Texto
- observacion: Texto [0..1]

+ aprobar(responsable: Usuario): Booleano
```


### MaterialEducativo

Estereotipo propuesto: `Entidad`. Repositorio reutilizable; archivo máximo 10 MB y tipos autorizados. SQL material/contenido; HU-062/HU-044.


```text
- titulo: Texto
- categoria: Texto
- formato: Texto
- tamanoBytes: Entero
- recurso: Recurso

+ esAdmisible(): Booleano
+ puedeReutilizarse(): Booleano
```


## Notificaciones


### PlantillaNotificacion

Estereotipo propuesto: `Entidad`. Plantilla por evento y canal; naturaleza obligatoria propuesta pendiente P14. HU-066.


```text
- titulo: Texto
- cuerpo: Texto
- evento: Texto
- canal: Canal
- obligatoria: Booleano

+ prepararMensaje(datos: DatosEvento): Texto
+ definirContenido(titulo: Texto, cuerpo: Texto, responsable: Usuario): Booleano
```


### PreferenciaNotificacion

Estereotipo propuesto: `Entidad`. No puede desactivar comunicación obligatoria. HU-067; SQL preferencia_notificacion.


```text
- evento: Texto
- canal: Canal
- habilitada: Booleano

+ permiteEnvio(obligatoria: Booleano): Booleano
```


### Notificacion

Estereotipo propuesto: `Entidad`. Aviso de bandeja y sus envíos; separación conceptual propuesta respecto de fila SQL por canal. HU-068/HU-069.


```text
- evento: Texto
- creadaEn: FechaHora
- leidaEn: FechaHora [0..1]
- titulo: Texto
- mensaje: Texto

+ marcarLeida(destinatario: Usuario): Booleano
```


### EnvioNotificacion

Estereotipo propuesto: `Entidad`. Historial de entrega por canal sin bloquear operación principal; hasta tres reintentos, número total de intentos requiere convención explícita. HU-068/HU-070.


```text
- canal: Canal
- estado: Texto
- intentos: Entero
- enviadaEn: FechaHora [0..1]
- ultimoError: Texto [0..1]

+ programar(): Booleano
+ puedeReintentarse(): Booleano
+ registrarResultado(exito: Booleano, fecha: FechaHora): Booleano
+ consultarHistorial(filtro: FiltroReporte, solicitante: Usuario): Coleccion<EnvioNotificacion>
```


## JuegosRetos


### Juego

Estereotipo propuesto: `Entidad`. Juego educativo configurable; criterios derivados de HU pendientes de persistencia completa. HU-071/HU-072/HU-073/HU-076.


```text
- nombre: Texto
- instrucciones: Texto
- tipo: TipoJuego
- activo: Booleano
- maximoIntentos: Entero
- criteriosPuntuacion: Texto
- criteriosFinalizacion: Texto

+ admitePartida(socio: Socio): Booleano
+ calcularIntentosRestantes(socio: Socio): Entero
+ activar(): Booleano
+ desactivar(): Booleano
+ definirContenido(instrucciones: Texto, preguntas: Coleccion<Pregunta>, responsable: Usuario): Booleano
```


### Partida

Estereotipo propuesto: `Entidad`. Resultado calculado en servidor; no aceptar puntaje final del cliente. HU-074/HU-075.


```text
- iniciadaEn: FechaHora
- finalizadaEn: FechaHora [0..1]
- puntuacion: Decimal [0..1]
- resultadoValido: Booleano

+ calcularResultado(): Decimal
+ finalizar(): Booleano
+ habilitaReconocimiento(): Booleano
```


### Reto

Estereotipo propuesto: `Entidad`. Tipo de actividad y cantidad medible; recompensa por regla vigente. HU-077.


```text
- objetivo: Texto
- tipoActividad: Texto
- meta: Entero
- inicio: Fecha
- fin: Fecha
- recompensa: Entero

+ estaVigente(fecha: Fecha): Booleano
+ cumpleObjetivo(progreso: ProgresoReto): Booleano
+ definirObjetivo(tipoActividad: Texto, cantidad: Entero, responsable: Usuario): Booleano
```


### ProgresoReto

Estereotipo propuesto: `Entidad`. Una recompensa por socio–reto; excluir duplicación de actividad. HU-078.


```text
- avance: Entero
- completadoEn: FechaHora [0..1]
- recompensaReconocida: Booleano

+ incorporarActividad(actividad: ActividadValidada): Booleano
+ calcularPorcentaje(): Decimal
+ reconocerCumplimiento(fecha: Fecha): Booleano
```


## Comunidad


### PerfilPublico

Estereotipo propuesto: `Entidad`. Información personal oculta por defecto; vista propia de clasificación incluso excluido de pública. HU-083/HU-035.


```text
- alias: Texto
- camposVisibles: Conjunto<Texto>
- participaClasificacionPublica: Booleano

+ definirPrivacidad(campos: Conjunto<Texto>): Booleano
+ obtenerDatosPublicos(): DatosPublicos
```


### PublicacionComunidad

Estereotipo propuesto: `Entidad`. Solo socios autenticados; imágenes autorizadas hasta 10 MB. HU-079/HU-080.


```text
- texto: Texto
- imagenes: Coleccion<Recurso>
- creadaEn: FechaHora
- estadoModeracion: Texto

+ admiteInteraccion(): Booleano
+ publicar(autor: Socio): Booleano
```


### Comentario

Estereotipo propuesto: `Entidad`. Asociado a publicación y socio; contenido oculto no admite interacción. HU-080.


```text
- texto: Texto
- creadoEn: FechaHora
- estadoModeracion: Texto

+ puedeMostrarse(): Booleano
```


### Reaccion

Estereotipo propuesto: `Entidad`. Una reacción por socio–publicación según SQL; regla de cambio pendiente si se amplía. HU-080.


```text
- tipo: Texto
- fecha: FechaHora
(Sin operaciones propias: registro u objeto de datos.)
```


### ReporteComunidad

Estereotipo propuesto: `Entidad`. Reporte de publicación o comentario, exclusivamente uno. HU-081; clase propuesta sin tabla equivalente confirmada.


```text
- motivo: Texto
- fecha: FechaHora
- estado: Texto

+ enviarAModeracion(): Booleano
```


### DecisionModeracion

Estereotipo propuesto: `Registro`. Oculta/elimina contenido o suspende temporalmente con motivo; alcance y plazo pendientes P14. HU-082.


```text
- accion: Texto
- motivo: Texto
- fecha: FechaHora
- suspensionHasta: FechaHora [0..1]

+ aplicar(responsable: Usuario): Booleano
```


## Bienestar


### ConvenioBienestar

Estereotipo propuesto: `Entidad`. Convenio informativo, sin datos clínicos de socios. HU-084/HU-085/HU-086.


```text
- proveedor: Texto
- descripcion: Texto
- beneficioDescriptivo: Texto
- condiciones: Texto
- inicio: Fecha [0..1]
- fin: Fecha [0..1]

+ estaVigente(fecha: Fecha): Booleano
+ habilitaBeneficio(fecha: Fecha): Booleano
+ configurar(condiciones: Condiciones, responsable: Usuario): Booleano
```


### RecursoBienestar

Estereotipo propuesto: `Entidad`. Vincula contenido institucional y opcionalmente convenio. HU-085; SQL recurso_bienestar.


```text
- titulo: Texto
- categoria: Texto

+ esVisible(fecha: Fecha): Booleano
```


## Reportes


### ServicioReportes

Estereotipo propuesto: `ServicioDominio`. Servicio de dominio propuesto para consultas y exportaciones según rol; sin atributos artificiales. HU-087–091.


```text
+ generarSupervision(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte
+ generarReferidosCampanas(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte
+ generarImpactoSocial(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte
+ generarGamificacion(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte
+ exportar(resultado: ResultadoReporte, formato: Texto, solicitante: Usuario): Recurso
```


### FiltroReporte

Estereotipo propuesto: `ObjetoValor`. Objeto de valor propuesto, registra filtros aplicados sin datos técnicos del framework. HU-088–091.


```text
- desde: Fecha [0..1]
- hasta: Fecha [0..1]
- campana: Referencia [0..1]
- segmento: Referencia [0..1]
- estado: Texto [0..1]

+ esValido(): Booleano
```


### ResultadoReporte

Estereotipo propuesto: `ObjetoValor`. Objeto de valor propuesto de salida; conserva fecha y filtros. HU-087–091. No obliga a persistir cada consulta.


```text
- tipo: Texto
- generadoEn: FechaHora
- indicadores: Coleccion<Indicador>
- datosEnmascarados: Booleano
(Sin operaciones propias: registro u objeto de datos.)
```


## Asociaciones y multiplicidades

Cada fila se lee: un A tiene la cantidad de B indicada en «B por A»; un B tiene la cantidad de A indicada en «A por B». Los nombres de roles se precisan mediante el significado. Restricciones condicionales prevalecen sobre el máximo general.

| A | A por B | B | B por A | Significado y restricción |
| --- | --- | --- | --- | --- |
| Usuario | 1 | Socio | 0..1 | cuenta de la condición de socio |
| Usuario | 0..* | Rol | 0..* | roles asignados, sin herencia |
| Rol | 0..* | Permiso | 0..* | capacidades concedidas |
| Usuario | 1 | ConsentimientoCuenta | 1..* | aceptaciones versionadas de la cuenta |
| Usuario | 1 | Sesion | 0..* | sesiones de la cuenta |
| Usuario | 1 | RecuperacionAcceso | 0..* | solicitudes de recuperación |
| Usuario | 1 | ControlAcceso | 1 | política conceptual y estado de intentos asociado |
| Usuario | 0..1 | EventoAuditoria | 0..* | actor de evento; anónimo permitido |
| Usuario | 0..1 | CambioEstado | 0..* | responsable del cambio; sistema permitido |
| Usuario | 1 | ValidacionAdministrativaSocio | 0..1 | cuenta destinataria validada exitosamente |
| Usuario | 1 | ValidacionAdministrativaSocio | 0..* | administrador que confirma la validación |
| Socio | 1 | CodigoReferido | 0..* | códigos históricos; como máximo uno activo |
| CodigoReferido | 1 | Referido | 0..* | código utilizado al registrar |
| Prospecto | 1 | Referido | 0..* | historial; a lo sumo un referido activo |
| Referido | 1 | ConsentimientoProspecto | 0..* | solicitudes y evidencia versionada; a lo sumo una confirmación vigente |
| Referido | 1 | Conversion | 0..1 | hecho de conversión; también único por prospecto |
| Usuario | 1 | Conversion | 0..* | responsable que valida evidencia comercial |
| Campana | 0..1 | Referido | 0..* | campaña cuando corresponde |
| Usuario | 1 | Campana | 0..* | creador autorizado |
| Campana | 0..* | Segmento | 0..* | público objetivo |
| Campana | 1 | IncentivoCampana | 0..* | condiciones de reconocimiento por versión |
| Campana | 1 | ParticipacionCampana | 0..* | participaciones para monitoreo |
| Socio | 1 | ParticipacionCampana | 0..* | participante validado |
| Socio | 1 | CuentaPuntos | 1 | cuenta conceptual de puntos |
| CuentaPuntos | 1 | MovimientoPuntos | 0..* | libro inmutable del socio |
| ReglaPuntos | 0..1 | MovimientoPuntos | 0..* | regla aplicada cuando hay acreditación |
| ActividadValidada | 0..1 | MovimientoPuntos | 0..* | origen de reconocimiento; canjes/reversos usan sus enlaces específicos |
| Socio | 1 | ActividadValidada | 0..* | beneficiario del hecho reconocido |
| MovimientoPuntos | 0..1 | MovimientoPuntos | 0..* | original del reverso; validar no exceder importe reversible |
| CuentaPuntos | 0..* | Nivel | 0..1 | nivel calculado, base pendiente de política |
| Socio | 1 | InsigniaObtenida | 0..* | logros propios |
| Insignia | 1 | InsigniaObtenida | 0..* | tipo de logro obtenido una vez por socio |
| Socio | 1 | PerfilPublico | 0..1 | privacidad y alias; valores seguros por defecto al faltar |
| Capacitacion | 1 | ModuloCapacitacion | 1..* | pertenencia exclusiva; composición conceptual |
| ModuloCapacitacion | 0..* | MaterialEducativo | 0..* | material reutilizable |
| Socio | 1 | InscripcionCapacitacion | 0..* | inscrito, único por capacitación |
| Capacitacion | 1 | InscripcionCapacitacion | 0..* | oferta elegida |
| InscripcionCapacitacion | 1 | ProgresoModulo | 0..* | avance de la persona |
| ModuloCapacitacion | 1 | ProgresoModulo | 0..* | unidad completada; pertenece a la misma capacitación |
| Capacitacion | 1 | Evaluacion | 0..1 | evaluación final propuesta; cardinalidad por validar con política formativa |
| InscripcionCapacitacion | 1 | IntentoEvaluacion | 0..* | intentos del inscrito |
| Evaluacion | 1 | IntentoEvaluacion | 0..* | evaluación rendida |
| InscripcionCapacitacion | 1 | Certificado | 0..1 | certificado tras aprobación |
| Evaluacion | 0..1 | Pregunta | 0..* | propietario exclusivo XOR Juego |
| Juego | 0..1 | Pregunta | 0..* | propietario exclusivo XOR Evaluacion |
| Pregunta | 1 | OpcionPregunta | 0..* | alternativas exclusivas; composición conceptual |
| Pregunta | 1 | RespuestaActividad | 0..* | pregunta respondida |
| IntentoEvaluacion | 0..1 | RespuestaActividad | 0..* | propietario de respuesta XOR Partida |
| Partida | 0..1 | RespuestaActividad | 0..* | propietario de respuesta XOR IntentoEvaluacion |
| Socio | 1 | InscripcionTaller | 0..* | inscripción/asistencia única por taller |
| Taller | 1 | InscripcionTaller | 0..* | asistencia con cupo controlado |
| Usuario | 0..1 | InscripcionTaller | 0..* | responsable que confirma asistencia |
| Campana | 1 | Sorteo | 0..* | campaña de sorteo según SQL; obligatoriedad pendiente P04 |
| Sorteo | 1 | ParticipacionSorteo | 0..* | participaciones registradas |
| Socio | 1 | ParticipacionSorteo | 0..* | socio participante |
| ActividadValidada | 1 | ParticipacionSorteo | 0..* | origen validado de participación |
| Sorteo | 1 | PremioSorteo | 1..* | premios del sorteo |
| Sorteo | 1 | EvidenciaSorteo | 0..1 | lista y evidencia tras congelación |
| Sorteo | 1 | ResultadoSorteo | 0..* | ganadores y suplentes, antes de ejecución vacío |
| ParticipacionSorteo | 1 | ResultadoSorteo | 0..1 | participación seleccionada del mismo sorteo |
| PremioSorteo | 0..1 | ResultadoSorteo | 0..* | asignación; suplente puede no tener premio todavía |
| Socio | 1 | Canje | 0..* | solicitudes propias |
| Beneficio | 1 | Canje | 0..* | beneficio solicitado |
| Canje | 0..1 | MovimientoPuntos | 0..* | reserva, descuento o liberación del canje |
| Usuario | 0..1 | Canje | 0..* | responsable de decisión |
| Usuario | 0..1 | Canje | 0..* | responsable de entrega, rol separado de aprobación |
| ConvenioBienestar | 0..1 | Beneficio | 0..* | origen del beneficio, opcional |
| Usuario | 1 | ContenidoInstitucional | 0..* | autor o gestor |
| ContenidoInstitucional | 1 | AprobacionContenido | 0..* | decisiones versionadas de aprobación opcional |
| Usuario | 1 | AprobacionContenido | 0..* | responsable designado |
| ContenidoInstitucional | 1 | MaterialEducativo | 0..* | organización de material según diseño SQL; revisar con repositorio reutilizable |
| ContenidoInstitucional | 1 | RecursoBienestar | 0..* | contenido informativo de bienestar |
| ConvenioBienestar | 0..1 | RecursoBienestar | 0..* | convenio asociado cuando corresponde |
| Usuario | 1 | PreferenciaNotificacion | 0..* | preferencias por evento y canal |
| Usuario | 1 | Notificacion | 0..* | destinatario |
| Notificacion | 1 | EnvioNotificacion | 0..* | entregas por canal |
| PlantillaNotificacion | 1 | EnvioNotificacion | 0..* | plantilla usada para evento/canal |
| Socio | 1 | Partida | 0..* | jugador |
| Juego | 1 | Partida | 0..* | configuración del juego |
| Socio | 1 | ProgresoReto | 0..* | progreso propio |
| Reto | 1 | ProgresoReto | 0..* | reto medible |
| ReglaPuntos | 0..1 | Reto | 0..* | regla de recompensa; referencia histórica a preservar |
| Socio | 1 | PublicacionComunidad | 0..* | autor socio |
| PublicacionComunidad | 1 | Comentario | 0..* | comentarios recibidos |
| Socio | 1 | Comentario | 0..* | autor del comentario |
| PublicacionComunidad | 1 | Reaccion | 0..* | reacciones recibidas |
| Socio | 1 | Reaccion | 0..* | una por publicación según SQL |
| Socio | 1 | ReporteComunidad | 0..* | persona que reporta |
| PublicacionComunidad | 0..1 | ReporteComunidad | 0..* | objeto reportado XOR Comentario |
| Comentario | 0..1 | ReporteComunidad | 0..* | objeto reportado XOR PublicacionComunidad |
| ReporteComunidad | 1 | DecisionModeracion | 0..* | decisiones con motivo |
| Usuario | 1 | DecisionModeracion | 0..* | gestor autorizado |
| Socio | 0..1 | DecisionModeracion | 0..* | socio afectado si hay suspensión temporal |
| FiltroReporte | 1 | ResultadoReporte | 0..* | filtros aplicados al resultado |

## Dependencias de responsabilidad

| Origen | Destino | Motivo |
| --- | --- | --- |
| ControlAcceso | EntradaPadron | consulta condición para registrar |
| ControlAcceso | Rol | identifica/asigna roles |
| ControlAcceso | Sesion | abre y autoriza sesiones |
| ControlAcceso | EventoAuditoria | deja evidencia |
| ValidacionAdministrativaSocio | EntradaPadron | consulta/añade confirmación temporal autorizada |
| ValidacionAdministrativaSocio | Socio | habilita condición, no conversión comercial |
| RecuperacionAcceso | Sesion | revoca sesiones al restablecer |
| Referido | EntradaPadron | descarta prospecto ya socio |
| Referido | ActividadValidada | conversión validada produce actividad |
| IntentoEvaluacion | ActividadValidada | aprobación produce actividad |
| InscripcionTaller | ActividadValidada | asistencia produce actividad |
| Partida | ActividadValidada | resultado válido produce actividad |
| ProgresoReto | ActividadValidada | cumplimiento produce actividad |
| Canje | CuentaPuntos | coordina reserva/descuento/liberación |
| Clasificacion | CuentaPuntos | consulta puntos con política pendiente |
| Clasificacion | PerfilPublico | respeta alias y exclusión |
| ServicioReportes | Referido | consulta captación |
| ServicioReportes | Campana | consulta resultados |
| ServicioReportes | InscripcionCapacitacion | consulta formación |
| ServicioReportes | Certificado | consulta certificados |
| ServicioReportes | MovimientoPuntos | consulta puntos |
| ServicioReportes | Canje | consulta recompensas |
| ServicioReportes | ResultadoSorteo | consulta resultados enmascarados |
| ServicioReportes | Usuario | autoriza según roles vigentes |
| ServicioReportes | ResultadoReporte | genera salida y aplica privacidad |
| Referido | CambioEstado | conserva seguimiento |
| Campana | CambioEstado | conserva cambios |
| Canje | CambioEstado | conserva decisiones y entrega |
| CuentaPuntos | Notificacion | comunica reconocimientos |
| Sorteo | Notificacion | comunica ganadores |
| DecisionModeracion | Usuario | aplica suspensión autorizada cuando corresponde |

La actividad comercial o formativa origina una ActividadValidada; los movimientos de canje enlazan directamente con Canje. Las dependencias a CambioEstado explican su uso, y su entidad/referencia identifica el objeto seguido sin crear una FK universal inexistente. Validar política de retención; ninguna composición autoriza borrar evidencia histórica.
