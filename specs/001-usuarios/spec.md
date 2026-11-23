# Gestión de usuarios y perfiles

Criterios vigentes conciliados con los cambios de línea base. Revisar la [matriz de aceptación técnica](acceptance.md) para conocer la evidencia y el alcance del cierre.

## Objetivo y alcance

*Propósito:* Registrar socios validando su condición en el padrón de prueba, mantener sus perfiles y administrar las cuentas del personal (COMP: Usuarios). Apoya el objetivo del Acta de una interfaz sencilla y segura.

*Cobertura de historias antes de consolidar:* HU-001 a HU-008 (RF-01-1 a RF-01-8).

*Criterios de finalización:*

# Un socio del padrón de prueba se registra, consulta y edita su perfil.

# El administrador gestiona cuentas y estados registrando motivo, fecha y responsable.

# No es posible crear cuentas duplicadas por cédula, correo o usuario.

*Sprints:* S1–S2.



*Backlog consolidado (07/11/2026):*

# Historias vigentes: HU-001, HU-002, HU-004, HU-005.

# Historias incorporadas a otras: HU-006 → HU-001, HU-008 → HU-001, HU-003 → HU-002, HU-007 → HU-005.

# Se mantiene la cobertura de los 8 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

El registro público requiere 18 años cumplidos en la fecha local de la cooperativa. El servidor valida la edad antes de consultar el padrón o crear una cuenta general o de socio.

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-001: Registrar socio con validación de cédula, padrón y duplicados

Sprint: Sprint 1. Tipo: Story. Ítem original: 101. Padre: 1.

*Historia:* Como socio de la cooperativa, quiero registrarme en la plataforma, para acceder a referidos, capacitaciones y recompensas.

*Descripción funcional:* Registro con cédula, nombres, apellidos, fecha de nacimiento, celular, correo, usuario y contraseña. Se validan los campos obligatorios y el formato de diez dígitos de la cédula.

*Criterios de aceptación:*

# El formulario solicita todos los campos y marca los obligatorios.

# Una cédula que no sea texto de diez dígitos ASCII se rechaza con un mensaje de validación. Se preservan ceros iniciales y el dígito verificador queda fuera de la regla vigente.

# El padrón activo habilita el rol Socio. Una cédula ausente permite crear una cuenta general sin dicho rol. El padrón inactivo, un fallo de consulta o un duplicado impiden el alta.

# La contraseña se almacena con Argon2id o bcrypt (costo ≥ 10) y el consentimiento se registra con fecha, hora y versión de la política.

*Trazabilidad:* RF-01-1 · RF-01 Gestión de usuarios y perfiles · UR-01 · RNF-01, RNF-02, RNF-07, RNF-20, RNF-23 · Dep.: RF-01-6, RF-01-8



*Consolidación de historias (07/11/2026):*

Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:



*HU-006: Validar la condición de socio activo* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 1 | Puntos originales: 3 | Requisito: RF-01-6

*Historia:* Como administrador de la plataforma, quiero que se verifique que la cédula pertenece a un socio activo, para que solo socios reales accedan a las funciones de socio.

*Descripción funcional:* Consulta contra el padrón de prueba del MVP antes de habilitar las funciones de socio.

*Criterios de aceptación:*

# La cédula se busca en el padrón de prueba y solo se habilitan funciones de socio si su estado es activo.

# Una cédula ausente permite el alta general. Una cédula inactiva o un fallo de consulta impiden el alta.

# La validación usa únicamente datos de prueba, sin conexión a sistemas de producción.

*Trazabilidad:* RF-01-6 · RF-01 Gestión de usuarios y perfiles · UR-01 · RNF-23 · Dep.: —



*HU-008: Prevenir cuentas duplicadas* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 1 | Puntos originales: 2 | Requisito: RF-01-8

*Historia:* Como administrador, quiero impedir cuentas duplicadas, para mantener un único registro por socio.

*Descripción funcional:* Unicidad por cédula, correo electrónico y nombre de usuario.

*Criterios de aceptación:*

# Se rechaza el registro si la cédula ya tiene una cuenta.

# Se rechaza si el correo o el usuario ya existen.

# La unicidad también está garantizada por restricciones en la base de datos.

*Trazabilidad:* RF-01-8 · RF-01 Gestión de usuarios y perfiles · UR-01 · RNF-20 · Dep.: —



*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.

*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-006, HU-008.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-002: Consultar y actualizar mi perfil

Sprint: Sprint 2. Tipo: Story. Ítem original: 102. Padre: 1.

*Historia:* Como socio, quiero consultar mi información personal, para verificar que sea correcta.

*Descripción funcional:* El socio autenticado consulta exclusivamente su propio perfil.

*Criterios de aceptación:*

# El socio autenticado accede a Mi perfil y ve sus datos registrados.

# El servidor devuelve solo el perfil de la sesión; pedir el ID de otro usuario responde acceso denegado.

# Sin sesión activa se redirige al inicio de sesión.

*Trazabilidad:* RF-01-2 · RF-01 Gestión de usuarios y perfiles · UR-02 · RNF-10 · Dep.: RF-02-1



*Consolidación de historias (07/11/2026):*

Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:



*HU-003: Editar los datos de contacto del perfil* | Responsable originalmente asignado: lizriofrio557@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 3 | Requisito: RF-01-3

*Historia:* Como socio, quiero actualizar mi teléfono, correo y foto, para mantener mis datos de contacto al día.

*Descripción funcional:* Solo se modifican los datos autorizados; la cédula y los datos institucionales son inmutables.

*Criterios de aceptación:*

# El socio puede modificar teléfono, correo y foto.

# La cédula y los datos institucionales aparecen en solo lectura y el servidor rechaza cualquier intento de cambiarlos.

# La foto se valida por tipo, extensión y tamaño máximo de 10 MB.

# Al guardar se muestra una confirmación con los datos actualizados.

*Trazabilidad:* RF-01-3 · RF-01 Gestión de usuarios y perfiles · UR-03 · RNF-07, RNF-20, RNF-26 · Dep.: RF-01-2



*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.

*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-003.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-004: Cambiar la contraseña

Sprint: Sprint 2. Tipo: Story. Ítem original: 104. Padre: 1.

*Historia:* Como usuario autenticado, quiero cambiar mi contraseña, para proteger mi cuenta.

*Descripción funcional:* Se verifica la contraseña actual y la política de seguridad vigente.

*Criterios de aceptación:*

# Se exige la contraseña actual; si es incorrecta, no se aplica el cambio.

# La nueva contraseña tiene mínimo 8 caracteres y no figura en la lista de contraseñas comunes.

# La nueva contraseña se almacena con hash y el cambio queda en la bitácora.

# Los caracteres se ocultan al ingresarlos.

*Trazabilidad:* RF-01-4 · RF-01 Gestión de usuarios y perfiles · UR-06 · RNF-01, RNF-06 · Dep.: RF-02-1

### HU-005: Administrar cuentas de usuarios y sus estados

Sprint: Sprint 2. Tipo: Story. Ítem original: 105. Padre: 1.

*Historia:* Como administrador, quiero registrar cuentas del personal y gestionar usuarios, para que cada área opere en la plataforma.

*Descripción funcional:* Alta de personal, consulta de usuarios y edición de datos permitidos según permisos.

*Criterios de aceptación:*

# El administrador registra cuentas del personal asignándoles un rol.

# Puede consultar y filtrar usuarios y editar solo los campos permitidos.

# Un usuario sin rol de administrador recibe acceso denegado, verificado en el servidor.

# Cada alta o edición queda registrada en la bitácora.

*Trazabilidad:* RF-01-5 · RF-01 Gestión de usuarios y perfiles · UR-04 · RNF-06, RNF-10 · Dep.: RF-02-5



*Consolidación de historias (07/11/2026):*

Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:



*HU-007: Gestionar el estado de las cuentas* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 3 | Requisito: RF-01-7

*Historia:* Como administrador, quiero activar, suspender o desactivar cuentas, para controlar quién accede a la plataforma.

*Descripción funcional:* Cambio de estado con motivo, fecha y responsable.

*Criterios de aceptación:*

# El administrador puede activar, suspender o desactivar una cuenta.

# El cambio exige motivo y registra fecha y responsable.

# Una cuenta suspendida o desactivada no puede iniciar sesión y sus sesiones activas se invalidan.

*Trazabilidad:* RF-01-7 · RF-01 Gestión de usuarios y perfiles · UR-04 · RNF-06, RNF-11 · Dep.: RF-01-5



*Coordinación:* Responsable principal de esta historia: vale0401g@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.

*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-007.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-003: Editar los datos de contacto del perfil

Sprint: Sprint 2. Tipo: Sub-task. Ítem original: 103. Padre: 102.

*Historia:* Como socio, quiero actualizar mi teléfono, correo y foto, para mantener mis datos de contacto al día.

*Descripción funcional:* Solo se modifican los datos autorizados; la cédula y los datos institucionales son inmutables.

*Criterios de aceptación:*

# El socio puede modificar teléfono, correo y foto.

# La cédula y los datos institucionales aparecen en solo lectura y el servidor rechaza cualquier intento de cambiarlos.

# La foto se valida por tipo, extensión y tamaño máximo de 10 MB.

# Al guardar se muestra una confirmación con los datos actualizados.

*Trazabilidad:* RF-01-3 · RF-01 Gestión de usuarios y perfiles · UR-03 · RNF-07, RNF-20, RNF-26 · Dep.: RF-01-2

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-002.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* lizriofrio557@gmail.com.

### HU-006: Validar la condición de socio activo

Sprint: Sprint 1. Tipo: Sub-task. Ítem original: 106. Padre: 101.

*Historia:* Como administrador de la plataforma, quiero que se verifique que la cédula pertenece a un socio activo, para que solo socios reales accedan a las funciones de socio.

*Descripción funcional:* Consulta contra el padrón de prueba del MVP antes de habilitar las funciones de socio.

*Criterios de aceptación:*

# La cédula se busca en el padrón de prueba y solo se habilitan funciones de socio si su estado es activo.

# Una cédula ausente permite el alta general. Una cédula inactiva o un fallo de consulta impiden el alta.

# La validación usa únicamente datos de prueba, sin conexión a sistemas de producción.

*Trazabilidad:* RF-01-6 · RF-01 Gestión de usuarios y perfiles · UR-01 · RNF-23 · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-001.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 1.
*Responsable original:* vale0401g@gmail.com.

### HU-007: Gestionar el estado de las cuentas

Sprint: Sprint 2. Tipo: Sub-task. Ítem original: 107. Padre: 105.

*Historia:* Como administrador, quiero activar, suspender o desactivar cuentas, para controlar quién accede a la plataforma.

*Descripción funcional:* Cambio de estado con motivo, fecha y responsable.

*Criterios de aceptación:*

# El administrador puede activar, suspender o desactivar una cuenta.

# El cambio exige motivo y registra fecha y responsable.

# Una cuenta suspendida o desactivada no puede iniciar sesión y sus sesiones activas se invalidan.

*Trazabilidad:* RF-01-7 · RF-01 Gestión de usuarios y perfiles · UR-04 · RNF-06, RNF-11 · Dep.: RF-01-5

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-005.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* vale0401g@gmail.com.

### HU-008: Prevenir cuentas duplicadas

Sprint: Sprint 1. Tipo: Sub-task. Ítem original: 108. Padre: 101.

*Historia:* Como administrador, quiero impedir cuentas duplicadas, para mantener un único registro por socio.

*Descripción funcional:* Unicidad por cédula, correo electrónico y nombre de usuario.

*Criterios de aceptación:*

# Se rechaza el registro si la cédula ya tiene una cuenta.

# Se rechaza si el correo o el usuario ya existen.

# La unicidad también está garantizada por restricciones en la base de datos.

*Trazabilidad:* RF-01-8 · RF-01 Gestión de usuarios y perfiles · UR-01 · RNF-20 · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-001.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 1.
*Responsable original:* vale0401g@gmail.com.

## Requisitos funcionales vigentes

### RF-01-1 Registrar socio

El sistema deberá registrar cuentas con cédula, nombres, apellidos, fecha de nacimiento, celular, correo, usuario y contraseña, validando obligatorios, cédula como texto de diez dígitos ASCII, unicidad y consentimiento. Con padrón activo crea socio; con cédula ausente crea cuenta general; con padrón inactivo rechaza; si el padrón falla no crea una cuenta.

UR: UR-01. HU: HU-001. CU: CU-G02.

### RF-01-2 Consultar perfil

El sistema deberá permitir al socio autenticado consultar exclusivamente la información de su propio perfil.

UR: UR-02. HU: HU-002. CU: CU-G02.

### RF-01-3 Editar perfil

El sistema deberá permitir al socio actualizar su teléfono, correo y foto, impidiendo modificar la cédula y los datos institucionales.

UR: UR-03. HU: HU-003. CU: CU-G02.

### RF-01-4 Cambiar contraseña

El sistema deberá permitir al usuario autenticado cambiar su contraseña verificando la actual y la política de seguridad vigente.

UR: UR-06. HU: HU-004. CU: CU-G02.

### RF-01-5 Administrar usuarios

El sistema deberá permitir al administrador registrar cuentas del personal, consultar usuarios y modificar los datos permitidos según sus permisos.

UR: UR-04. HU: HU-005. CU: CU-G17.

### RF-01-6 Validar condición de socio

El sistema deberá consultar el padrón de prueba antes de habilitar la condición de socio. Activo permite habilitarla, ausente permite crear cuenta general sin privilegios de socio, inactivo impide el registro e indisponibilidad del padrón impide completar el alta.

UR: UR-01. HU: HU-006. CU: CU-G02.

### RF-01-7 Gestionar estado de cuentas

El sistema deberá permitir al administrador activar, suspender o desactivar cuentas, registrando motivo, fecha y responsable.

UR: UR-04. HU: HU-007. CU: CU-G17.

### RF-01-8 Prevenir cuentas duplicadas

El sistema deberá impedir más de una cuenta asociada a la misma cédula, correo electrónico o nombre de usuario.

UR: UR-01. HU: HU-008. CU: CU-G02.

## Requisitos de calidad

- **RNF-01 Protección de contraseñas:** El sistema deberá almacenar las contraseñas con Argon2id o bcrypt (factor de costo ≥ 10) y sal individual, exigir un mínimo de 8 caracteres, rechazar contraseñas comunes y ocultar los caracteres al ingresarlas.
- **RNF-02 Consentimiento de datos:** El sistema deberá registrar el consentimiento expreso de socios y prospectos para el tratamiento de datos personales, con fecha, hora y versión de la política aceptada.
- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-06 Auditoría inmutable:** El sistema deberá registrar en una bitácora de solo inserción las operaciones críticas (usuario, fecha, hora, acción, recurso, resultado e IP), sin permitir su modificación ni eliminación desde la aplicación.
- **RNF-07 Validación y accesibilidad:** Los formularios deberán validar los datos en línea con mensajes que indiquen cómo corregir el error, cumpliendo el contraste y etiquetado de WCAG 2.1 nivel AA.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
