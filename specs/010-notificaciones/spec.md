# Notificaciones

## Objetivo y alcance

*Propósito:* Informar eventos relevantes en la plataforma y por correo (WS: Notificaciones).
*Cobertura de historias antes de consolidar:* HU-066 a HU-070 (RF-10-1 a RF-10-5).
*Criterios de finalización:*
# Las notificaciones se envían de forma asíncrona con hasta 3 reintentos.
# El socio gestiona su bandeja y sus preferencias.
# El personal consulta el historial de envíos.
*Sprints:* S2–S5.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-066, HU-067, HU-068, HU-069, HU-070.
# Historias incorporadas a otras: Ninguna.
# Se mantiene la cobertura de los 5 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-066: Gestionar plantillas de notificación

Sprint: Sprint 3. Tipo: Story. Ítem original: 166. Padre: 10.

*Historia:* Como personal autorizado, quiero administrar plantillas, para estandarizar los mensajes.
*Descripción funcional:* Título, contenido, tipo de evento y canal.
*Criterios de aceptación:*
# Se crean y editan plantillas con todos sus datos.
# Solo el personal autorizado puede gestionarlas.
# Los envíos automáticos usan la plantilla del evento y canal correspondiente.
*Trazabilidad:* RF-10-1 · RF-10 Notificaciones · UR-36 · — · Dep.: —

### HU-067: Gestionar preferencias de notificación

Sprint: Sprint 5. Tipo: Story. Ítem original: 167. Padre: 10.

*Historia:* Como socio, quiero elegir qué notificaciones opcionales recibo y por qué canal, para no saturarme.
*Descripción funcional:* Preferencias que respetan las comunicaciones obligatorias.
*Criterios de aceptación:*
# El socio activa o desactiva las notificaciones opcionales por canal.
# Las obligatorias no pueden desactivarse.
# Los envíos respetan las preferencias guardadas.
*Trazabilidad:* RF-10-2 · RF-10 Notificaciones · UR-37 · — · Dep.: —

### HU-068: Enviar notificaciones automáticas

Sprint: Sprint 2. Tipo: Story. Ítem original: 168. Padre: 10.

*Historia:* Como socio, quiero recibir avisos automáticos, para enterarme de mis referidos, puntos, campañas, sorteos y canjes.
*Descripción funcional:* Servicio asíncrono de plataforma y correo. Los eventos de cada módulo se conectan en el sprint donde ese módulo se implementa.
*Criterios de aceptación:*
# Se generan avisos en plataforma y correo ante los eventos definidos.
# El envío es asíncrono y no bloquea la operación principal.
# Un envío fallido se reintenta hasta 3 veces y el error queda registrado.
# Se respetan las preferencias del socio.
*Trazabilidad:* RF-10-3 · RF-10 Notificaciones · UR-36 · RNF-18 · Dep.: RF-03-9, RF-05-2, RF-08-3

### HU-069: Consultar la bandeja de notificaciones

Sprint: Sprint 2. Tipo: Story. Ítem original: 169. Padre: 10.

*Historia:* Como socio, quiero ver mis notificaciones y marcarlas como leídas, para organizarme.
*Descripción funcional:* Bandeja con estado de lectura.
*Criterios de aceptación:*
# El socio ve sus notificaciones e identifica las no leídas.
# Puede marcarlas como leídas.
# Solo ve sus propias notificaciones.
*Trazabilidad:* RF-10-4 · RF-10 Notificaciones · UR-38 · RNF-10 · Dep.: —

### HU-070: Consultar el historial de envíos

Sprint: Sprint 5. Tipo: Story. Ítem original: 170. Padre: 10.

*Historia:* Como personal autorizado, quiero revisar los envíos realizados, para detectar fallos.
*Descripción funcional:* Fecha, destinatario, tipo, canal y estado.
*Criterios de aceptación:*
# Se listan los envíos con estado enviado o fallido.
# Se puede filtrar por estado y canal.
# Solo el personal autorizado accede.
*Trazabilidad:* RF-10-5 · RF-10 Notificaciones · UR-36 · RNF-18 · Dep.: RF-10-3

## Requisitos funcionales vigentes

### RF-10-1 Gestionar plantillas

El sistema deberá permitir crear y modificar plantillas con título, contenido, tipo de evento y canal.

UR: UR-36. HU: HU-066. CU: CU-G11.

### RF-10-2 Gestionar preferencias

El sistema deberá permitir al socio elegir las notificaciones opcionales y los canales, sin desactivar las obligatorias.

UR: UR-37. HU: HU-067. CU: CU-G11.

### RF-10-3 Enviar notificaciones automáticas

El sistema deberá enviar notificaciones ante cambios de estado de referidos, acreditación de puntos, campañas, sorteos y canjes, respetando las preferencias del socio.

UR: UR-36. HU: HU-068. CU: CU-G11.

### RF-10-4 Consultar bandeja

El sistema deberá permitir al socio ver sus notificaciones, identificar las no leídas y marcarlas como leídas.

UR: UR-38. HU: HU-069. CU: CU-G11.

### RF-10-5 Consultar historial de envíos

El sistema deberá permitir al personal autorizado consultar los envíos con fecha, destinatario, tipo, canal y estado (enviado o fallido).

UR: UR-36. HU: HU-070. CU: CU-G11.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-18 Notificaciones asíncronas:** El sistema deberá procesar las notificaciones de forma asíncrona, reintentando hasta 3 veces los envíos fallidos y registrando el error, sin bloquear las operaciones principales.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
