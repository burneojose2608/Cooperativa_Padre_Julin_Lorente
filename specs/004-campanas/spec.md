# Campañas e incentivos

## Objetivo y alcance

*Propósito:* Permitir a Marketing y Responsabilidad Social crear, segmentar y monitorear campañas (SS: Campañas).
*Cobertura de historias antes de consolidar:* HU-025 a HU-030 (RF-04-1 a RF-04-6).
*Criterios de finalización:*
# Una campaña se crea en Borrador, se activa y es visible solo para su segmento.
# Las modificaciones no alteran incentivos reconocidos.
# El monitoreo muestra la tasa de conversión y el avance frente a la meta.
*Sprints:* S3–S4.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-025, HU-027, HU-028, HU-030.
# Historias incorporadas a otras: HU-026 → HU-025, HU-029 → HU-028.
# Se mantiene la cobertura de los 6 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-025: Crear y activar campañas

Sprint: Sprint 3. Tipo: Story. Ítem original: 125. Padre: 4.

*Historia:* Como Responsable de Marketing o de Responsabilidad Social, quiero crear campañas con objetivos e incentivos, para impulsar la participación.
*Descripción funcional:* Nombre, tipo, objetivo, meta, vigencia, condiciones e incentivos (puntos o participaciones en sorteos), con estado inicial Borrador.
*Criterios de aceptación:*
# Se registran todos los campos de la campaña.
# Toda campaña nueva inicia en Borrador.
# La fecha de fin debe ser posterior a la de inicio.
# Solo Marketing y Responsabilidad Social pueden crear campañas.
*Trazabilidad:* RF-04-1 · RF-04 Campañas e incentivos · UR-12 · RNF-06, RNF-07 · Dep.: RF-05-1

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-026: Gestionar el estado de las campañas* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 3 | Puntos originales: 3 | Requisito: RF-04-2
*Historia:* Como Responsable de Marketing, quiero cambiar el estado de las campañas, para controlar cuándo se puede participar.
*Descripción funcional:* Estados Borrador, Activa, Suspendida y Finalizada.
*Criterios de aceptación:*
# Se puede cambiar entre los cuatro estados.
# No se aceptan participaciones en campañas suspendidas, finalizadas o fuera de vigencia.
# Cada cambio de estado queda registrado.
*Trazabilidad:* RF-04-2 · RF-04 Campañas e incentivos · UR-15 · RNF-06 · Dep.: RF-04-1

*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-026.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-027: Consultar campañas vigentes

Sprint: Sprint 3. Tipo: Story. Ítem original: 127. Padre: 4.

*Historia:* Como socio, quiero ver las campañas vigentes, para decidir en cuáles participar.
*Descripción funcional:* Solo campañas activas, vigentes y de su segmento.
*Criterios de aceptación:*
# El socio ve solo campañas activas y dentro de vigencia.
# Una campaña segmentada solo la ven los socios de ese segmento.
# Cada campaña muestra condiciones, incentivos y fechas.
*Trazabilidad:* RF-04-3 · RF-04 Campañas e incentivos · UR-14 · RNF-03 · Dep.: RF-04-2

### HU-028: Segmentar y modificar campañas con historial

Sprint: Sprint 4. Tipo: Story. Ítem original: 128. Padre: 4.

*Historia:* Como Responsable de Marketing, quiero dirigir campañas a grupos específicos, incluido el segmento joven, para mejorar la captación.
*Descripción funcional:* Criterios autorizados: rango de edad, tipo de socio, producto y agencia.
*Criterios de aceptación:*
# Se define el público por rango de edad, tipo de socio, producto y agencia.
# Antes de activar la campaña se muestra cuántos socios cumplen la segmentación.
# Solo se pueden usar los criterios autorizados.
*Trazabilidad:* RF-04-4 · RF-04 Campañas e incentivos · UR-13 · RNF-06 · Dep.: RF-04-1

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-029: Modificar campañas conservando el historial* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 4 | Puntos originales: 3 | Requisito: RF-04-5
*Historia:* Como Responsable de Marketing, quiero modificar campañas sin afectar incentivos ya reconocidos, para ajustar estrategias con seguridad.
*Descripción funcional:* La edición depende del estado e incluye historial de cambios.
*Criterios de aceptación:*
# Los campos editables dependen del estado de la campaña.
# Las modificaciones no alteran retroactivamente los incentivos reconocidos.
# Se conserva el historial de cambios con responsable y fecha.
*Trazabilidad:* RF-04-5 · RF-04 Campañas e incentivos · UR-15 · RNF-06 · Dep.: RF-04-2

*Coordinación:* Responsable principal de esta historia: vale0401g@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-029.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-030: Monitorear los resultados de una campaña

Sprint: Sprint 4. Tipo: Story. Ítem original: 130. Padre: 4.

*Historia:* Como Responsable de Marketing, quiero ver indicadores por campaña, para evaluar su efectividad.
*Descripción funcional:* Participantes, referidos, conversiones, tasa de conversión, puntos otorgados y avance frente a la meta.
*Criterios de aceptación:*
# Se muestran todos los indicadores por campaña.
# Solo se usan participaciones y conversiones validadas.
# Tasa de conversión = conversiones / referidos; si no hay referidos se muestra 0 %.
*Trazabilidad:* RF-04-6 · RF-04 Campañas e incentivos · UR-46 · RNF-04 · Dep.: RF-03-9, RF-05-6

### HU-026: Gestionar el estado de las campañas

Sprint: Sprint 3. Tipo: Sub-task. Ítem original: 126. Padre: 125.

*Historia:* Como Responsable de Marketing, quiero cambiar el estado de las campañas, para controlar cuándo se puede participar.
*Descripción funcional:* Estados Borrador, Activa, Suspendida y Finalizada.
*Criterios de aceptación:*
# Se puede cambiar entre los cuatro estados.
# No se aceptan participaciones en campañas suspendidas, finalizadas o fuera de vigencia.
# Cada cambio de estado queda registrado.
*Trazabilidad:* RF-04-2 · RF-04 Campañas e incentivos · UR-15 · RNF-06 · Dep.: RF-04-1

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-025.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 3.
*Responsable original:* vale0401g@gmail.com.

### HU-029: Modificar campañas conservando el historial

Sprint: Sprint 4. Tipo: Sub-task. Ítem original: 129. Padre: 128.

*Historia:* Como Responsable de Marketing, quiero modificar campañas sin afectar incentivos ya reconocidos, para ajustar estrategias con seguridad.
*Descripción funcional:* La edición depende del estado e incluye historial de cambios.
*Criterios de aceptación:*
# Los campos editables dependen del estado de la campaña.
# Las modificaciones no alteran retroactivamente los incentivos reconocidos.
# Se conserva el historial de cambios con responsable y fecha.
*Trazabilidad:* RF-04-5 · RF-04 Campañas e incentivos · UR-15 · RNF-06 · Dep.: RF-04-2

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-028.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 4.
*Responsable original:* vale0401g@gmail.com.

## Requisitos funcionales vigentes

### RF-04-1 Crear y configurar campañas

El sistema deberá crear campañas con nombre, tipo, objetivo, meta, vigencia, condiciones, incentivos (puntos o participaciones en sorteos) y estado inicial Borrador.

UR: UR-12. HU: HU-025. CU: CU-G18.

### RF-04-2 Gestionar estado de campañas

El sistema deberá permitir cambiar el estado entre Borrador, Activa, Suspendida y Finalizada, impidiendo nuevas participaciones en campañas suspendidas, finalizadas o fuera de vigencia.

UR: UR-15. HU: HU-026. CU: CU-G18.

### RF-04-3 Consultar campañas vigentes

El sistema deberá mostrar al socio solo las campañas activas y vigentes (y, si existe segmentación, las de su segmento), con condiciones, incentivos y fechas.

UR: UR-14. HU: HU-027. CU: CU-G06.

### RF-04-4 Segmentar campañas

El sistema deberá definir el público objetivo con criterios autorizados: rango de edad (incluido el segmento joven), tipo de socio, producto y agencia.

UR: UR-13. HU: HU-028. CU: CU-G18.

### RF-04-5 Modificar campañas

El sistema deberá permitir modificar campañas según su estado, sin alterar retroactivamente los incentivos reconocidos y conservando el historial de cambios.

UR: UR-15. HU: HU-029. CU: CU-G18.

### RF-04-6 Monitorear campaña

El sistema deberá mostrar por campaña los participantes, referidos, conversiones, la tasa de conversión, los puntos otorgados y el avance frente a la meta.

UR: UR-46. HU: HU-030. CU: CU-G18.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-06 Auditoría inmutable:** El sistema deberá registrar en una bitácora de solo inserción las operaciones críticas (usuario, fecha, hora, acción, recurso, resultado e IP), sin permitir su modificación ni eliminación desde la aplicación.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
