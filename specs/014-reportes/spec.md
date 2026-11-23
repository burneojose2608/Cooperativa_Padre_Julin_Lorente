# Reportes y estadísticas

## Objetivo y alcance

*Propósito:* Indicadores e informes para decisiones y balance social (SS: Reportes).
*Cobertura de historias antes de consolidar:* HU-087 a HU-091 (RF-14-1 a RF-14-5).
*Criterios de finalización:*
# Panel de supervisión y reportes de Marketing, impacto social y gamificación disponibles.
# Las cifras coinciden con los datos de prueba.
# Exportación a PDF y Excel/CSV con fecha y filtros.
*Sprints:* S4–S5.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-087, HU-088, HU-089, HU-090, HU-091.
# Historias incorporadas a otras: Ninguna.
# Se mantiene la cobertura de los 5 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-087: Visualizar el panel de supervisión

Sprint: Sprint 4. Tipo: Story. Ítem original: 187. Padre: 14.

*Historia:* Como administrador, quiero un panel centralizado, para supervisar la actividad de la plataforma.
*Descripción funcional:* Usuarios activos, referidos, conversiones, puntos emitidos y canjeados, y actividad reciente.
*Criterios de aceptación:*
# El panel muestra todos los indicadores definidos.
# Solo el administrador accede.
# Las cifras coinciden con consultas directas sobre los datos de prueba.
*Trazabilidad:* RF-14-1 · RF-14 Reportes y estadísticas · UR-56 · RNF-04 · Dep.: RF-03-9, RF-05-6, RF-08-5

### HU-088: Generar reporte de referidos y campañas

Sprint: Sprint 4. Tipo: Story. Ítem original: 188. Padre: 14.

*Historia:* Como Responsable de Marketing, quiero un reporte de conversiones por campaña, para evaluar estrategias.
*Descripción funcional:* Conversiones, tasa de conversión y resultados por campaña, período y segmento.
*Criterios de aceptación:*
# El reporte se puede filtrar por campaña, período y segmento.
# El reporte indica los filtros aplicados.
# Los datos personales aparecen enmascarados.
*Trazabilidad:* RF-14-2 · RF-14 Reportes y estadísticas · UR-46 · RNF-14 · Dep.: RF-04-6

### HU-089: Generar reporte de impacto social

Sprint: Sprint 5. Tipo: Story. Ítem original: 189. Padre: 14.

*Historia:* Como Responsable de Responsabilidad Social, quiero indicadores de formación, para el balance social.
*Descripción funcional:* Inscritos, aprobados, certificados emitidos, horas de formación y participación por rango de edad.
*Criterios de aceptación:*
# El reporte muestra todos los indicadores definidos.
# Se puede filtrar por período.
# Solo Responsabilidad Social y el Administrador acceden.
*Trazabilidad:* RF-14-3 · RF-14 Reportes y estadísticas · UR-57 · RNF-14 · Dep.: RF-06-6

### HU-090: Generar reporte de gamificación y recompensas

Sprint: Sprint 5. Tipo: Story. Ítem original: 190. Padre: 14.

*Historia:* Como administrador, quiero comparar puntos emitidos y canjeados, para controlar el programa de incentivos.
*Descripción funcional:* Puntos emitidos frente a canjeados, canjes por beneficio y resultados de sorteos.
*Criterios de aceptación:*
# Se muestran los puntos emitidos frente a los canjeados.
# Se muestran los canjes por beneficio.
# Se muestran los resultados de sorteos con datos enmascarados.
*Trazabilidad:* RF-14-4 · RF-14 Reportes y estadísticas · UR-42 · RNF-14 · Dep.: RF-05-6, RF-08-5

### HU-091: Exportar reportes en PDF y Excel/CSV

Sprint: Sprint 5. Tipo: Story. Ítem original: 191. Padre: 14.

*Historia:* Como personal autorizado, quiero exportar reportes, para compartirlos y archivarlos.
*Descripción funcional:* Exportación con fecha de generación y filtros aplicados.
*Criterios de aceptación:*
# Se exporta en PDF y en Excel/CSV.
# El archivo incluye la fecha de generación y los filtros aplicados.
# Se respeta el enmascaramiento según el rol.
# En CSV se neutralizan las celdas que inician con =, +, - o @ (inyección de fórmulas).
*Trazabilidad:* RF-14-5 · RF-14 Reportes y estadísticas · UR-42 · RNF-14, RNF-20 · Dep.: RF-14-1 a RF-14-4

## Requisitos funcionales vigentes

### RF-14-1 Panel de supervisión

El sistema deberá mostrar al administrador los usuarios activos, referidos, conversiones, puntos emitidos y canjeados, y la actividad reciente.

UR: UR-56. HU: HU-087. CU: CU-G25.

### RF-14-2 Reporte de referidos y campañas

El sistema deberá entregar a Marketing las conversiones, la tasa de conversión y los resultados por campaña, período y segmento.

UR: UR-46. HU: HU-088. CU: CU-G25.

### RF-14-3 Reporte de impacto social

El sistema deberá entregar a Responsabilidad Social los inscritos, aprobados, certificados emitidos, horas de formación y la participación por rango de edad.

UR: UR-57. HU: HU-089. CU: CU-G25.

### RF-14-4 Reporte de gamificación y recompensas

El sistema deberá mostrar los puntos emitidos frente a los canjeados, los canjes por beneficio y los resultados de sorteos.

UR: UR-42. HU: HU-090. CU: CU-G25.

### RF-14-5 Exportar reportes

El sistema deberá exportar los reportes en PDF y Excel/CSV, indicando la fecha de generación y los filtros aplicados.

UR: UR-42. HU: HU-091. CU: CU-G25.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-14 Enmascaramiento y privacidad:** El sistema deberá enmascarar los datos personales (cédula parcial, alias) en listados, reportes, clasificaciones, resultados de sorteos y comunidad, mostrando el dato completo solo a los roles autorizados.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
