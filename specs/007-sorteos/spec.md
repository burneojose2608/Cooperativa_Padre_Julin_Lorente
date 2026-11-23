# Sorteos

## Objetivo y alcance

*Propósito:* Configurar y ejecutar sorteos verificables entre socios elegibles (SS: Sorteos).
*Cobertura de historias antes de consolidar:* HU-048 a HU-053 (RF-07-1 a RF-07-6).
*Criterios de finalización:*
# Las participaciones se generan sin duplicados.
# El sorteo usa CSPRNG y una lista congelada con hash.
# Los resultados se publican enmascarados y se notifica a los ganadores.
*Sprints:* S3–S5.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-048, HU-049, HU-050, HU-051.
# Historias incorporadas a otras: HU-052 → HU-050, HU-053 → HU-050.
# Se mantiene la cobertura de los 6 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-048: Configurar sorteos

Sprint: Sprint 3. Tipo: Story. Ítem original: 148. Padre: 7.

*Historia:* Como Responsable de Marketing, quiero configurar sorteos, para incentivar la participación.
*Descripción funcional:* Nombre, premios, ganadores, suplentes, fecha, condiciones y elegibilidad.
*Criterios de aceptación:*
# Se crea un sorteo con todos sus datos.
# El número de ganadores debe ser mayor que cero.
# Solo Marketing o el Administrador pueden configurarlo.
*Trazabilidad:* RF-07-1 · RF-07 Sorteos · UR-25 · RNF-06 · Dep.: —

### HU-049: Generar participaciones en sorteos

Sprint: Sprint 4. Tipo: Story. Ítem original: 149. Padre: 7.

*Historia:* Como socio, quiero obtener participaciones al cumplir condiciones, para optar a premios.
*Descripción funcional:* Generación automática sin duplicados no permitidos.
*Criterios de aceptación:*
# Las participaciones se generan automáticamente al cumplirse las condiciones.
# No se generan duplicados no permitidos.
# Cada participación registra socio, sorteo, origen y fecha.
*Trazabilidad:* RF-07-2 · RF-07 Sorteos · UR-26 · RNF-06 · Dep.: RF-07-1, RF-03-3, RF-06-3

### HU-050: Ejecutar sorteos, notificar ganadores y auditar resultados

Sprint: Sprint 5. Tipo: Story. Ítem original: 150. Padre: 7.

*Historia:* Como Responsable de Marketing, quiero ejecutar sorteos verificables, para garantizar transparencia.
*Descripción funcional:* Verificación de elegibilidad, selección aleatoria y registro de evidencia.
*Criterios de aceptación:*
# Antes de ejecutar, la lista elegible se congela y se registra su hash.
# La selección usa un generador aleatorio criptográficamente seguro.
# Se registran ganadores, suplentes y evidencia.
# Un sorteo ejecutado no puede volver a ejecutarse.
*Trazabilidad:* RF-07-3 · RF-07 Sorteos · UR-27 · RNF-13, RNF-22 · Dep.: RF-07-2

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-052: Notificar a los ganadores* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 5 | Puntos originales: 2 | Requisito: RF-07-5
*Historia:* Como socio ganador, quiero ser notificado, para reclamar mi premio.
*Descripción funcional:* Aviso con premio y condiciones de reclamo.
*Criterios de aceptación:*
# Al registrarse los ganadores se les notifica el premio y las condiciones.
# La notificación llega por plataforma y correo según las preferencias, respetando las obligatorias.
# Un envío fallido se reintenta sin bloquear el sorteo.
*Trazabilidad:* RF-07-5 · RF-07 Sorteos · UR-28 · RNF-18 · Dep.: RF-10-3

*HU-053: Consultar el historial de sorteos* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 5 | Puntos originales: 2 | Requisito: RF-07-6
*Historia:* Como administrador, quiero consultar sorteos pasados con su evidencia, para auditarlos.
*Descripción funcional:* Sorteos, participantes elegibles, ganadores y evidencias.
*Criterios de aceptación:*
# Se listan los sorteos con elegibles, ganadores y evidencias.
# Se puede verificar el hash de la lista congelada.
# Solo el personal autorizado accede.
*Trazabilidad:* RF-07-6 · RF-07 Sorteos · UR-27 · RNF-13 · Dep.: —

*Coordinación:* Responsable principal de esta historia: jgabriel2608@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-052, HU-053.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-051: Consultar resultados de sorteos

Sprint: Sprint 5. Tipo: Story. Ítem original: 151. Padre: 7.

*Historia:* Como socio, quiero ver los resultados publicados, para saber quién ganó.
*Descripción funcional:* Solo la información de ganadores autorizada.
*Criterios de aceptación:*
# El socio ve los resultados publicados.
# Los ganadores aparecen con alias o datos enmascarados.
# Los sorteos no ejecutados no muestran resultados.
*Trazabilidad:* RF-07-4 · RF-07 Sorteos · UR-28 · RNF-14 · Dep.: RF-07-3

### HU-052: Notificar a los ganadores

Sprint: Sprint 5. Tipo: Sub-task. Ítem original: 152. Padre: 150.

*Historia:* Como socio ganador, quiero ser notificado, para reclamar mi premio.
*Descripción funcional:* Aviso con premio y condiciones de reclamo.
*Criterios de aceptación:*
# Al registrarse los ganadores se les notifica el premio y las condiciones.
# La notificación llega por plataforma y correo según las preferencias, respetando las obligatorias.
# Un envío fallido se reintenta sin bloquear el sorteo.
*Trazabilidad:* RF-07-5 · RF-07 Sorteos · UR-28 · RNF-18 · Dep.: RF-10-3

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-050.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 5.
*Responsable original:* vale0401g@gmail.com.

### HU-053: Consultar el historial de sorteos

Sprint: Sprint 5. Tipo: Sub-task. Ítem original: 153. Padre: 150.

*Historia:* Como administrador, quiero consultar sorteos pasados con su evidencia, para auditarlos.
*Descripción funcional:* Sorteos, participantes elegibles, ganadores y evidencias.
*Criterios de aceptación:*
# Se listan los sorteos con elegibles, ganadores y evidencias.
# Se puede verificar el hash de la lista congelada.
# Solo el personal autorizado accede.
*Trazabilidad:* RF-07-6 · RF-07 Sorteos · UR-27 · RNF-13 · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-050.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 5.
*Responsable original:* jgabriel2608@gmail.com.

## Requisitos funcionales vigentes

### RF-07-1 Configurar sorteo

El sistema deberá crear sorteos con nombre, premios, número de ganadores y suplentes, fecha, condiciones y criterios de elegibilidad.

UR: UR-25. HU: HU-048. CU: CU-G20.

### RF-07-2 Generar participaciones

El sistema deberá generar participaciones automáticamente para los socios que cumplan las condiciones, sin duplicados no permitidos.

UR: UR-26. HU: HU-049. CU: CU-G09.

### RF-07-3 Ejecutar sorteo y registrar ganadores

El sistema deberá verificar la elegibilidad, ejecutar la selección aleatoria y registrar ganadores, suplentes y evidencia del proceso.

UR: UR-27. HU: HU-050. CU: CU-G20.

### RF-07-4 Consultar resultados

El sistema deberá permitir a los socios consultar los resultados publicados, mostrando solo la información autorizada de los ganadores.

UR: UR-28. HU: HU-051. CU: CU-G09.

### RF-07-5 Notificar ganadores

El sistema deberá notificar a los ganadores el premio obtenido y las condiciones para reclamarlo.

UR: UR-28. HU: HU-052. CU: CU-G20.

### RF-07-6 Consultar historial de sorteos

El sistema deberá permitir al personal autorizado consultar sorteos, participantes elegibles, ganadores y evidencias.

UR: UR-27. HU: HU-053. CU: CU-G20.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-06 Auditoría inmutable:** El sistema deberá registrar en una bitácora de solo inserción las operaciones críticas (usuario, fecha, hora, acción, recurso, resultado e IP), sin permitir su modificación ni eliminación desde la aplicación.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-13 Historial de estados:** El sistema deberá conservar el historial completo de estados de referidos, sorteos y canjes (estado anterior, estado nuevo, responsable y fecha).
- **RNF-14 Enmascaramiento y privacidad:** El sistema deberá enmascarar los datos personales (cédula parcial, alias) en listados, reportes, clasificaciones, resultados de sorteos y comunidad, mostrando el dato completo solo a los roles autorizados.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-22 Sorteos verificables:** Los sorteos deberán usar un generador aleatorio criptográficamente seguro, y la lista de participaciones elegibles deberá congelarse y registrarse con su hash antes de la ejecución.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
