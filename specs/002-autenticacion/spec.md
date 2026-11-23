# Autenticación y control de acceso

## Objetivo y alcance

*Propósito:* Autenticar usuarios y autorizar cada acción en el servidor según los 5 roles base (COMP: Seguridad).
*Cobertura de historias antes de consolidar:* HU-009 a HU-015 (RF-02-1 a RF-02-7).
*Criterios de finalización:*
# Inicio, cierre y recuperación de sesión funcionan de forma segura.
# Toda ruta restringida deniega por defecto y verifica rol y pertenencia en el servidor.
# Bloqueo por intentos fallidos e inactividad de 15 min verificados.
*Sprints:* S1–S2.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-009, HU-011, HU-013.
# Historias incorporadas a otras: HU-010 → HU-009, HU-012 → HU-009, HU-015 → HU-009, HU-014 → HU-013.
# Se mantiene la cobertura de los 7 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-009: Iniciar y cerrar sesión con validación de credenciales y roles

Sprint: Sprint 1. Tipo: Story. Ítem original: 109. Padre: 2.

*Historia:* Como usuario, quiero iniciar sesión desde el celular o la computadora, para acceder a mis funciones.
*Descripción funcional:* Inicio de sesión con usuario o correo y contraseña.
*Criterios de aceptación:*
# El formulario acepta usuario o correo y contraseña, y oculta la contraseña.
# Con credenciales válidas se crea la sesión y se redirige al inicio según el rol.
# La vista funciona entre 320 y 1920 px y solo sobre HTTPS.
# Tras 5 intentos fallidos la cuenta se bloquea durante 15 minutos.
*Trazabilidad:* RF-02-1 · RF-02 Autenticación y control de acceso · UR-05 · RNF-03, RNF-09, RNF-21 · Dep.: RF-02-2

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-010: Validar credenciales de acceso* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 1 | Puntos originales: 3 | Requisito: RF-02-2
*Historia:* Como administrador de la plataforma, quiero que las credenciales se validen de forma segura, para impedir accesos indebidos.
*Descripción funcional:* Verificación de cuenta existente y activa con mensaje genérico ante fallos.
*Criterios de aceptación:*
# Se verifica que la cuenta exista y esté activa comparando el hash, nunca texto plano.
# Ante cualquier fallo se muestra el mismo mensaje genérico, sin revelar si el usuario existe.
# Cada intento, exitoso o fallido, queda en la bitácora con IP.
*Trazabilidad:* RF-02-2 · RF-02 Autenticación y control de acceso · UR-05 · RNF-01, RNF-06, RNF-21 · Dep.: —

*HU-012: Identificar los roles del usuario autenticado* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 1 | Puntos originales: 2 | Requisito: RF-02-4
*Historia:* Como usuario autenticado, quiero que el sistema reconozca mis roles, para ver solo las funciones que me corresponden.
*Descripción funcional:* Obtención de roles tras la autenticación para determinar las funcionalidades disponibles.
*Criterios de aceptación:*
# Tras autenticar, el servidor obtiene todos los roles del usuario.
# El menú muestra solo las funcionalidades de esos roles.
# Un usuario con varios roles ve la unión de sus funcionalidades.
*Trazabilidad:* RF-02-4 · RF-02 Autenticación y control de acceso · UR-07 · RNF-10 · Dep.: RF-02-1

*HU-015: Cerrar sesión e invalidarla en el servidor* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 1 | Puntos originales: 2 | Requisito: RF-02-7
*Historia:* Como usuario, quiero cerrar sesión, para que nadie reutilice mi sesión.
*Descripción funcional:* Invalidación de la sesión en el servidor al cerrar o por inactividad.
*Criterios de aceptación:*
# Al cerrar sesión, la sesión o el token se invalida en el servidor.
# Reutilizar un token invalidado responde no autorizado.
# La sesión se cierra automáticamente tras 15 minutos de inactividad.
*Trazabilidad:* RF-02-7 · RF-02 Autenticación y control de acceso · UR-05 · RNF-11 · Dep.: —

*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-010, HU-012, HU-015.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-011: Recuperar la contraseña por correo

Sprint: Sprint 2. Tipo: Story. Ítem original: 111. Padre: 2.

*Historia:* Como usuario, quiero restablecer mi contraseña si la olvido, para recuperar el acceso a mi cuenta.
*Descripción funcional:* Enlace de un solo uso con expiración enviado al correo registrado.
**Aceptación vigente de Sprint 2.** Según [DEC-RECUPERACION-CONSOLA](../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md#recuperación-temporal-por-consola---sprint-2), el backend emite el código y el enlace por consola. La respuesta es genérica, el token se guarda como huella, vence a los 30 minutos, solo se usa una vez y el restablecimiento revoca las sesiones previas. Se aplica la política de contraseña y el límite de solicitudes.

**Aceptación definitiva pendiente.** El criterio original de entrega al correo registrado se conserva para la integración RF-10-3. Su cierre requiere comprobar SMTP, entrega y expiración en el entorno acordado.

*Criterios de aceptación:*
# La solicitud siempre muestra el mismo mensaje, exista o no la cuenta.
# Se envía al correo registrado un enlace de un solo uso con expiración.
# Un enlace ya usado o expirado es rechazado.
# La nueva contraseña cumple la política de seguridad.
*Trazabilidad:* RF-02-3 · RF-02 Autenticación y control de acceso · UR-06 · RNF-01, RNF-21 · Dep.: RF-10-3

### HU-013: Administrar roles, permisos y acceso seguro

Sprint: Sprint 2. Tipo: Story. Ítem original: 113. Padre: 2.

*Historia:* Como administrador, quiero asignar, modificar y revocar roles y permisos, para que cada usuario acceda solo a sus funciones.
*Descripción funcional:* Roles base: Socio, Administrador, Responsable de Marketing, Responsable de Responsabilidad Social y Gestor de contenidos.
*Criterios de aceptación:*
# Existen los cinco roles base.
# El administrador asigna, modifica y revoca roles y permisos.
# Los cambios se aplican en la siguiente solicitud del usuario afectado.
# Cada cambio queda registrado en la bitácora.
*Trazabilidad:* RF-02-5 · RF-02 Autenticación y control de acceso · UR-07 · RNF-06, RNF-10 · Dep.: —

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-014: Autorizar el acceso según rol en el servidor* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 5 | Requisito: RF-02-6
*Historia:* Como administrador de la plataforma, quiero que cada acción restringida se autorice en el servidor, para impedir accesos a datos ajenos.
*Descripción funcional:* Verificación de permisos en el servidor antes de ejecutar funcionalidades restringidas, denegando por defecto.
*Criterios de aceptación:*
# Toda ruta restringida verifica rol y pertenencia del recurso; por defecto se deniega.
# La API responde 403 a solicitudes no autorizadas aunque la interfaz oculte la opción.
# Una prueba confirma que un socio no accede a recursos de otro cambiando identificadores.
*Trazabilidad:* RF-02-6 · RF-02 Autenticación y control de acceso · UR-07 · RNF-10, RNF-20 · Dep.: RF-02-4

*Coordinación:* Responsable principal de esta historia: jgabriel2608@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-014.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-010: Validar credenciales de acceso

Sprint: Sprint 1. Tipo: Sub-task. Ítem original: 110. Padre: 109.

*Historia:* Como administrador de la plataforma, quiero que las credenciales se validen de forma segura, para impedir accesos indebidos.
*Descripción funcional:* Verificación de cuenta existente y activa con mensaje genérico ante fallos.
*Criterios de aceptación:*
# Se verifica que la cuenta exista y esté activa comparando el hash, nunca texto plano.
# Ante cualquier fallo se muestra el mismo mensaje genérico, sin revelar si el usuario existe.
# Cada intento, exitoso o fallido, queda en la bitácora con IP.
*Trazabilidad:* RF-02-2 · RF-02 Autenticación y control de acceso · UR-05 · RNF-01, RNF-06, RNF-21 · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-009.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 1.
*Responsable original:* jgabriel2608@gmail.com.

### HU-012: Identificar los roles del usuario autenticado

Sprint: Sprint 1. Tipo: Sub-task. Ítem original: 112. Padre: 109.

*Historia:* Como usuario autenticado, quiero que el sistema reconozca mis roles, para ver solo las funciones que me corresponden.
*Descripción funcional:* Obtención de roles tras la autenticación para determinar las funcionalidades disponibles.
*Criterios de aceptación:*
# Tras autenticar, el servidor obtiene todos los roles del usuario.
# El menú muestra solo las funcionalidades de esos roles.
# Un usuario con varios roles ve la unión de sus funcionalidades.
*Trazabilidad:* RF-02-4 · RF-02 Autenticación y control de acceso · UR-07 · RNF-10 · Dep.: RF-02-1

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-009.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 1.
*Responsable original:* jgabriel2608@gmail.com.

### HU-014: Autorizar el acceso según rol en el servidor

Sprint: Sprint 2. Tipo: Sub-task. Ítem original: 114. Padre: 113.

*Historia:* Como administrador de la plataforma, quiero que cada acción restringida se autorice en el servidor, para impedir accesos a datos ajenos.
*Descripción funcional:* Verificación de permisos en el servidor antes de ejecutar funcionalidades restringidas, denegando por defecto.
*Criterios de aceptación:*
# Toda ruta restringida verifica rol y pertenencia del recurso; por defecto se deniega.
# La API responde 403 a solicitudes no autorizadas aunque la interfaz oculte la opción.
# Una prueba confirma que un socio no accede a recursos de otro cambiando identificadores.
*Trazabilidad:* RF-02-6 · RF-02 Autenticación y control de acceso · UR-07 · RNF-10, RNF-20 · Dep.: RF-02-4

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-013.
*Puntos de origen:* 5 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* jgabriel2608@gmail.com.

### HU-015: Cerrar sesión e invalidarla en el servidor

Sprint: Sprint 1. Tipo: Sub-task. Ítem original: 115. Padre: 109.

*Historia:* Como usuario, quiero cerrar sesión, para que nadie reutilice mi sesión.
*Descripción funcional:* Invalidación de la sesión en el servidor al cerrar o por inactividad.
*Criterios de aceptación:*
# Al cerrar sesión, la sesión o el token se invalida en el servidor.
# Reutilizar un token invalidado responde no autorizado.
# La sesión se cierra automáticamente tras 15 minutos de inactividad.
*Trazabilidad:* RF-02-7 · RF-02 Autenticación y control de acceso · UR-05 · RNF-11 · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-009.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 1.
*Responsable original:* jgabriel2608@gmail.com.

## Requisitos funcionales vigentes

### RF-02-1 Iniciar sesión

El sistema deberá permitir iniciar sesión con usuario o correo y contraseña.

UR: UR-05. HU: HU-009. CU: CU-G01.

### RF-02-2 Validar credenciales

El sistema deberá verificar que las credenciales correspondan a una cuenta existente y activa, mostrando un mensaje genérico ante fallos, sin revelar si el usuario existe.

UR: UR-05. HU: HU-010. CU: CU-G01.

### RF-02-3 Recuperar contraseña

El sistema deberá permitir restablecer la contraseña mediante un enlace de un solo uso, con expiración, enviado al correo registrado.

El criterio de entrega vigente para Sprint 2 y la comprobación externa pendiente se detallan en [HU-011](#hu-011-recuperar-la-contraseña-por-correo).

UR: UR-06. HU: HU-011. CU: CU-G01.

### RF-02-4 Identificar rol

El sistema deberá identificar los roles del usuario autenticado para determinar las funcionalidades disponibles.

UR: UR-07. HU: HU-012. CU: CU-G01.

### RF-02-5 Gestionar roles y permisos

El sistema deberá permitir al administrador asignar, modificar y revocar roles y permisos. Los roles base son Socio, Administrador, Responsable de Marketing, Responsable de Responsabilidad Social y Gestor de contenidos.

UR: UR-07. HU: HU-013. CU: CU-G17.

### RF-02-6 Autorizar acceso según rol

El sistema deberá verificar en el servidor los permisos del usuario antes de ejecutar cualquier funcionalidad restringida.

UR: UR-07. HU: HU-014. CU: CU-G17.

### RF-02-7 Cerrar sesión

El sistema deberá permitir cerrar la sesión, invalidándola en el servidor para impedir su reutilización.

UR: UR-05. HU: HU-015. CU: CU-G01.

## Requisitos de calidad

- **RNF-01 Protección de contraseñas:** El sistema deberá almacenar las contraseñas con Argon2id o bcrypt (factor de costo ≥ 10) y sal individual, exigir un mínimo de 8 caracteres, rechazar contraseñas comunes y ocultar los caracteres al ingresarlas.
- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-06 Auditoría inmutable:** El sistema deberá registrar en una bitácora de solo inserción las operaciones críticas (usuario, fecha, hora, acción, recurso, resultado e IP), sin permitir su modificación ni eliminación desde la aplicación.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-11 Inactividad de sesión:** El sistema deberá cerrar las sesiones tras 15 minutos de inactividad, invalidándolas en el servidor.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-21 Bloqueo y límite de solicitudes:** El sistema deberá bloquear temporalmente una cuenta durante 15 min tras 5 intentos fallidos de inicio de sesión y limitar la frecuencia de solicitudes en los formularios públicos.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
