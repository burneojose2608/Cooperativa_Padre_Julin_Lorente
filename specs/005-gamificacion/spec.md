# Puntos, niveles, insignias y clasificaciones

## Objetivo y alcance

*Propósito:* Acreditar puntos por acciones validadas mediante un registro inmutable y gestionar niveles, insignias y clasificaciones (SS: Gamificación).
*Cobertura de historias antes de consolidar:* HU-031 a HU-038 (RF-05-1 a RF-05-8).
*Criterios de finalización:*
# El saldo se calcula desde movimientos inmutables y nunca es negativo ni duplicado.
# Niveles e insignias se otorgan según criterios configurados.
# Las clasificaciones usan alias y permiten exclusión.
*Sprints:* S2–S4.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-031, HU-032, HU-033, HU-034, HU-035, HU-037, HU-038.
# Historias incorporadas a otras: HU-036 → HU-032.
# Se mantiene la cobertura de los 8 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-031: Configurar reglas de puntuación

Sprint: Sprint 2. Tipo: Story. Ítem original: 131. Padre: 5.

*Historia:* Como administrador, quiero configurar los puntos por actividad, para alinear incentivos con las reglas de la cooperativa.
*Descripción funcional:* Puntos por tipo de actividad, límites por período y vigencia, sin efecto retroactivo.
*Criterios de aceptación:*
# Se configuran puntos por tipo de actividad, límite por período y vigencia.
# Los cambios no recalculan acreditaciones anteriores.
# Solo el administrador puede modificar las reglas.
*Trazabilidad:* RF-05-1 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-16 · RNF-06 · Dep.: —

### HU-032: Acreditar puntos y registrar movimientos inmutables

Sprint: Sprint 3. Tipo: Story. Ítem original: 132. Padre: 5.

*Historia:* Como socio, quiero recibir puntos al completar acciones validadas, para ser reconocido por mi participación.
*Descripción funcional:* Acreditación automática por conversión, capacitación aprobada, asistencia a taller, juego o reto, usando el ID de la acción de origen.
*Criterios de aceptación:*
# Una acción validada acredita puntos según la regla vigente.
# El ID de la acción de origen actúa como clave de idempotencia: repetir el evento no duplica puntos.
# Se respetan los límites por período.
# La acreditación es atómica; si falla, no queda un registro parcial.
*Trazabilidad:* RF-05-2 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-16 · RNF-12 · Dep.: RF-05-1, RF-05-6

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-036: Registrar movimientos inmutables de puntos* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 5 | Requisito: RF-05-6
*Historia:* Como administrador, quiero que cada movimiento de puntos sea inmutable, para auditar los saldos con confianza.
*Descripción funcional:* Acreditación, reserva, descuento y reverso como movimientos; el saldo se deriva de ellos.
*Criterios de aceptación:*
# Cada operación se guarda como un movimiento inmutable.
# El saldo se calcula desde los movimientos y nunca es negativo.
# La aplicación no permite editar ni eliminar movimientos.
# Las operaciones concurrentes sobre un socio no producen saldos inconsistentes.
*Trazabilidad:* RF-05-6 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-17 · RNF-06, RNF-12 · Dep.: —

*Coordinación:* Responsable principal de esta historia: jgabriel2608@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-036.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-033: Calcular nivel e insignias

Sprint: Sprint 4. Tipo: Story. Ítem original: 133. Padre: 5.

*Historia:* Como socio, quiero subir de nivel y obtener insignias, para ver reconocido mi progreso.
*Descripción funcional:* Actualización de nivel e insignias según los criterios configurados.
*Criterios de aceptación:*
# Al superar el umbral de un nivel, el socio sube automáticamente.
# Cada insignia se otorga una sola vez al cumplir su criterio.
# El socio recibe una notificación del nuevo nivel o insignia.
*Trazabilidad:* RF-05-3 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-18 · — · Dep.: RF-05-7

### HU-034: Consultar puntos y logros

Sprint: Sprint 3. Tipo: Story. Ítem original: 134. Padre: 5.

*Historia:* Como socio, quiero consultar mis puntos, nivel e insignias, para conocer mi progreso.
*Descripción funcional:* Saldo, nivel, insignias e historial de movimientos con su actividad de origen.
*Criterios de aceptación:*
# El socio ve saldo, nivel e insignias.
# El historial muestra cada movimiento con la actividad que lo originó.
# El saldo mostrado coincide con la suma de movimientos.
# Sin puntos se muestra un mensaje informativo.
*Trazabilidad:* RF-05-4 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-17 · RNF-10 · Dep.: RF-05-6

### HU-035: Consultar clasificaciones

Sprint: Sprint 4. Tipo: Story. Ítem original: 135. Padre: 5.

*Historia:* Como socio, quiero ver mi posición en una clasificación protegiendo mi privacidad, para motivarme sin exponerme.
*Descripción funcional:* Clasificaciones por período con alias y opción de exclusión pública.
*Criterios de aceptación:*
# Se muestran clasificaciones por período usando alias.
# El socio puede excluirse de la vista pública y seguir viendo su propia posición.
# No se muestran cédulas ni nombres completos.
*Trazabilidad:* RF-05-5 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-19 · RNF-14 · Dep.: RF-05-6

### HU-037: Configurar niveles e insignias

Sprint: Sprint 3. Tipo: Story. Ítem original: 137. Padre: 5.

*Historia:* Como administrador, quiero definir niveles e insignias, para estructurar la progresión de los socios.
*Descripción funcional:* Niveles con umbral de puntos; insignias con criterio de logro, nombre e ícono.
*Criterios de aceptación:*
# El administrador define niveles con umbral de puntos.
# Define insignias con criterio, nombre e ícono.
# No se permiten umbrales de nivel duplicados.
*Trazabilidad:* RF-05-7 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-18 · — · Dep.: —

### HU-038: Revertir puntos de acciones invalidadas

Sprint: Sprint 4. Tipo: Story. Ítem original: 138. Padre: 5.

*Historia:* Como administrador, quiero revertir puntos de acciones invalidadas, para corregir acreditaciones indebidas.
*Descripción funcional:* Movimiento compensatorio con justificación obligatoria.
*Criterios de aceptación:*
# El reverso es un movimiento compensatorio; el original no se borra.
# La justificación es obligatoria.
# Si el reverso dejaría el saldo negativo, se rechaza y se informa el motivo.
*Trazabilidad:* RF-05-8 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-47 · RNF-06, RNF-12 · Dep.: RF-05-6

### HU-036: Registrar movimientos inmutables de puntos

Sprint: Sprint 3. Tipo: Sub-task. Ítem original: 136. Padre: 132.

*Historia:* Como administrador, quiero que cada movimiento de puntos sea inmutable, para auditar los saldos con confianza.
*Descripción funcional:* Acreditación, reserva, descuento y reverso como movimientos; el saldo se deriva de ellos.
*Criterios de aceptación:*
# Cada operación se guarda como un movimiento inmutable.
# El saldo se calcula desde los movimientos y nunca es negativo.
# La aplicación no permite editar ni eliminar movimientos.
# Las operaciones concurrentes sobre un socio no producen saldos inconsistentes.
*Trazabilidad:* RF-05-6 · RF-05 Puntos, niveles, insignias y clasificaciones · UR-17 · RNF-06, RNF-12 · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-032.
*Puntos de origen:* 5 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* jgabriel2608@gmail.com.

## Requisitos funcionales vigentes

### RF-05-1 Configurar reglas de puntuación

El sistema deberá permitir al administrador configurar los puntos por tipo de actividad, los límites por período y la vigencia. Los cambios no afectan acreditaciones anteriores.

UR: UR-16. HU: HU-031. CU: CU-G18.

### RF-05-2 Acreditar puntos por acciones validadas

El sistema deberá acreditar puntos automáticamente al confirmarse una acción validada (conversión, capacitación aprobada, asistencia a taller, juego o reto), usando el identificador de la acción de origen para impedir duplicados.

UR: UR-16. HU: HU-032. CU: CU-G07.

### RF-05-3 Calcular nivel e insignias

El sistema deberá actualizar el nivel y otorgar insignias cuando el socio cumpla los criterios configurados.

UR: UR-18. HU: HU-033. CU: CU-G07.

### RF-05-4 Consultar puntos y logros

El sistema deberá permitir al socio consultar su saldo, nivel, insignias e historial de movimientos, con la actividad que originó cada uno.

UR: UR-17. HU: HU-034. CU: CU-G07.

### RF-05-5 Consultar clasificaciones

El sistema deberá mostrar clasificaciones por período usando alias y permitir al socio excluirse de la vista pública.

UR: UR-19. HU: HU-035. CU: CU-G07.

### RF-05-6 Registrar movimientos de puntos

El sistema deberá registrar cada acreditación, reserva, descuento o reverso como un movimiento inmutable, calculando el saldo a partir de los movimientos.

UR: UR-17. HU: HU-036. CU: CU-G07.

### RF-05-7 Configurar niveles e insignias

El sistema deberá permitir al administrador definir niveles (umbral de puntos) e insignias (criterio de logro, nombre e ícono).

UR: UR-18. HU: HU-037. CU: CU-G07.

### RF-05-8 Revertir puntos

El sistema deberá permitir al personal autorizado revertir puntos de acciones invalidadas mediante un movimiento compensatorio con justificación obligatoria.

UR: UR-47. HU: HU-038. CU: CU-G07.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-06 Auditoría inmutable:** El sistema deberá registrar en una bitácora de solo inserción las operaciones críticas (usuario, fecha, hora, acción, recurso, resultado e IP), sin permitir su modificación ni eliminación desde la aplicación.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-12 Atomicidad e idempotencia de puntos:** El sistema deberá ejecutar las acreditaciones, reservas y descuentos de puntos en transacciones atómicas con clave de idempotencia por acción de origen, garantizando que el saldo nunca sea negativo ni se duplique ante operaciones concurrentes.
- **RNF-14 Enmascaramiento y privacidad:** El sistema deberá enmascarar los datos personales (cédula parcial, alias) en listados, reportes, clasificaciones, resultados de sorteos y comunidad, mostrando el dato completo solo a los roles autorizados.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-17 Mensajes de operación:** El sistema deberá mostrar mensajes claros de confirmación, advertencia o error tras cada operación, sin exponer detalles técnicos internos (trazas, consultas o rutas).
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
