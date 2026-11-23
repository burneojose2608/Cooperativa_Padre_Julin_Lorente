# Beneficios y recompensas

## Objetivo y alcance

*Propósito:* Canjear puntos por beneficios de la cooperativa y de sus convenios (SS: Recompensas).
*Cobertura de historias antes de consolidar:* HU-054 a HU-059 (RF-08-1 a RF-08-6).
*Criterios de finalización:*
# Un canje reserva, descuenta o libera puntos exactamente una vez.
# El flujo pendiente → aprobada/rechazada → entregada conserva historial.
# El socio consulta beneficios y su historial de canjes.
*Sprints:* S3–S4.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-054, HU-055, HU-056, HU-057, HU-058.
# Historias incorporadas a otras: HU-059 → HU-055.
# Se mantiene la cobertura de los 6 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-054: Configurar beneficios

Sprint: Sprint 3. Tipo: Story. Ítem original: 154. Padre: 8.

*Historia:* Como administrador o Responsable de Marketing, quiero registrar beneficios canjeables, para ofrecer recompensas a los socios.
*Descripción funcional:* Descripción, puntos requeridos, stock, condiciones y vigencia.
*Criterios de aceptación:*
# Se registran beneficios con todos sus datos.
# Los puntos requeridos y el stock no pueden ser negativos.
# Los beneficios se pueden editar y desactivar.
*Trazabilidad:* RF-08-1 · RF-08 Beneficios y recompensas · UR-31 · RNF-06 · Dep.: —

### HU-055: Solicitar canjes con reserva, descuento y liberación segura de puntos

Sprint: Sprint 4. Tipo: Story. Ítem original: 155. Padre: 8.

*Historia:* Como socio, quiero canjear mis puntos por beneficios, para aprovechar mi participación.
*Descripción funcional:* Verificación de condiciones, stock y saldo, con reserva de puntos.
*Criterios de aceptación:*
# Se verifican condiciones, stock y saldo antes de crear la solicitud.
# Al crearla, los puntos quedan reservados y la solicitud queda pendiente.
# Con saldo o stock insuficiente se rechaza con un mensaje claro.
*Trazabilidad:* RF-08-2 · RF-08 Beneficios y recompensas · UR-30 · RNF-12, RNF-17 · Dep.: RF-08-6

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-059: Reservar, descontar y liberar puntos de canjes* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 3 | Puntos originales: 5 | Requisito: RF-08-6
*Historia:* Como administrador, quiero que los puntos de cada canje se muevan exactamente una vez, para evitar saldos erróneos.
*Descripción funcional:* Movimientos del registro de puntos por canje.
*Criterios de aceptación:*
# La reserva, el descuento y la liberación se registran como movimientos.
# Cada operación ocurre una sola vez por canje (clave de idempotencia).
# Dos canjes simultáneos no pueden dejar el saldo negativo.
*Trazabilidad:* RF-08-6 · RF-08 Beneficios y recompensas · UR-30 · RNF-12 · Dep.: RF-05-6

*Coordinación:* Responsable principal de esta historia: vale0401g@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-059.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-056: Gestionar y entregar canjes

Sprint: Sprint 4. Tipo: Story. Ítem original: 156. Padre: 8.

*Historia:* Como administrador, quiero aprobar, rechazar y registrar entregas, para controlar los beneficios entregados.
*Descripción funcional:* Aprobación o rechazo con liberación de puntos y registro de entrega.
*Criterios de aceptación:*
# El personal autorizado aprueba o rechaza las solicitudes pendientes.
# Al rechazar se liberan los puntos reservados.
# Al aprobar, los puntos reservados se descuentan una sola vez; la entrega registra fecha y responsable.
# Cada cambio de estado queda en el historial.
*Trazabilidad:* RF-08-3 · RF-08 Beneficios y recompensas · UR-31 · RNF-06, RNF-13 · Dep.: RF-08-6

### HU-057: Consultar beneficios disponibles

Sprint: Sprint 3. Tipo: Story. Ítem original: 157. Padre: 8.

*Historia:* Como socio, quiero ver los beneficios disponibles, para decidir qué canjear.
*Descripción funcional:* Beneficios vigentes, incluidos los de convenios.
*Criterios de aceptación:*
# Se muestran descripción, puntos requeridos, condiciones y disponibilidad.
# Los beneficios sin stock o vencidos no aparecen como disponibles.
# Se identifican los beneficios que provienen de convenios.
*Trazabilidad:* RF-08-4 · RF-08 Beneficios y recompensas · UR-29 · RNF-03 · Dep.: RF-08-1

### HU-058: Consultar historial de canjes

Sprint: Sprint 4. Tipo: Story. Ítem original: 158. Padre: 8.

*Historia:* Como socio, quiero ver mis solicitudes de canje, para conocer su estado.
*Descripción funcional:* Beneficio, fecha, puntos y estado.
*Criterios de aceptación:*
# Se muestran las solicitudes con beneficio, fecha, puntos y estado.
# Se puede filtrar por pendiente, aprobada, rechazada o entregada.
# Solo se muestran las solicitudes propias.
*Trazabilidad:* RF-08-5 · RF-08 Beneficios y recompensas · UR-32 · RNF-13 · Dep.: —

### HU-059: Reservar, descontar y liberar puntos de canjes

Sprint: Sprint 4. Tipo: Sub-task. Ítem original: 159. Padre: 155.

*Historia:* Como administrador, quiero que los puntos de cada canje se muevan exactamente una vez, para evitar saldos erróneos.
*Descripción funcional:* Movimientos del registro de puntos por canje.
*Criterios de aceptación:*
# La reserva, el descuento y la liberación se registran como movimientos.
# Cada operación ocurre una sola vez por canje (clave de idempotencia).
# Dos canjes simultáneos no pueden dejar el saldo negativo.
*Trazabilidad:* RF-08-6 · RF-08 Beneficios y recompensas · UR-30 · RNF-12 · Dep.: RF-05-6

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-055.
*Puntos de origen:* 5 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 3.
*Responsable original:* jgabriel2608@gmail.com.

## Requisitos funcionales vigentes

### RF-08-1 Configurar beneficios

El sistema deberá registrar beneficios con descripción, puntos requeridos, stock, condiciones y vigencia.

UR: UR-31. HU: HU-054. CU: CU-G21.

### RF-08-2 Solicitar canje

El sistema deberá permitir al socio solicitar un beneficio, verificando condiciones, stock y saldo, y reservando los puntos mientras la solicitud esté pendiente.

UR: UR-30. HU: HU-055. CU: CU-G10.

### RF-08-3 Gestionar y entregar canjes

El sistema deberá permitir aprobar o rechazar solicitudes, liberando los puntos reservados al rechazar, y registrar la entrega con fecha y responsable.

UR: UR-31. HU: HU-056. CU: CU-G21.

### RF-08-4 Consultar beneficios disponibles

El sistema deberá mostrar al socio los beneficios vigentes con descripción, puntos requeridos, condiciones y disponibilidad.

UR: UR-29. HU: HU-057. CU: CU-G10.

### RF-08-5 Consultar historial de canjes

El sistema deberá mostrar las solicitudes del socio con beneficio, fecha, puntos y estado: pendiente, aprobada, rechazada o entregada.

UR: UR-32. HU: HU-058. CU: CU-G21.

### RF-08-6 Reservar y descontar puntos

El sistema deberá reservar, descontar o liberar los puntos de cada canje una sola vez, mediante movimientos del registro de puntos.

UR: UR-30. HU: HU-059. CU: CU-G10.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-06 Auditoría inmutable:** El sistema deberá registrar en una bitácora de solo inserción las operaciones críticas (usuario, fecha, hora, acción, recurso, resultado e IP), sin permitir su modificación ni eliminación desde la aplicación.
- **RNF-07 Validación y accesibilidad:** Los formularios deberán validar los datos en línea con mensajes que indiquen cómo corregir el error, cumpliendo el contraste y etiquetado de WCAG 2.1 nivel AA.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-12 Atomicidad e idempotencia de puntos:** El sistema deberá ejecutar las acreditaciones, reservas y descuentos de puntos en transacciones atómicas con clave de idempotencia por acción de origen, garantizando que el saldo nunca sea negativo ni se duplique ante operaciones concurrentes.
- **RNF-13 Historial de estados:** El sistema deberá conservar el historial completo de estados de referidos, sorteos y canjes (estado anterior, estado nuevo, responsable y fecha).
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-17 Mensajes de operación:** El sistema deberá mostrar mensajes claros de confirmación, advertencia o error tras cada operación, sin exponer detalles técnicos internos (trazas, consultas o rutas).
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
