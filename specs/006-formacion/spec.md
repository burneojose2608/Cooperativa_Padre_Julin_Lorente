# Capacitaciones, talleres y certificaciones

## Objetivo y alcance

*Propósito:* Gestionar capacitaciones virtuales y talleres de educación financiera, registrar la participación y emitir certificados (SS: Formación).
*Cobertura de historias antes de consolidar:* HU-039 a HU-047 (RF-06-1 a RF-06-9).
*Criterios de finalización:*
# Un socio completa módulos, aprueba la evaluación y descarga su certificado.
# Los certificados son verificables mediante un código no secuencial.
# Responsabilidad Social consulta inscritos, avance y resultados.
*Sprints:* S3–S5.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-039, HU-041, HU-042, HU-044, HU-045, HU-046, HU-047.
# Historias incorporadas a otras: HU-040 → HU-039, HU-043 → HU-042.
# Se mantiene la cobertura de los 9 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-039: Inscribirme y avanzar en capacitaciones

Sprint: Sprint 3. Tipo: Story. Ítem original: 139. Padre: 6.

*Historia:* Como socio, quiero ver capacitaciones de educación financiera e inscribirme, para fortalecer mis conocimientos.
*Descripción funcional:* Capacitaciones publicadas con descripción, contenido, duración y requisitos.
*Criterios de aceptación:*
# El socio ve las capacitaciones publicadas con su información.
# Solo puede inscribirse si cumple las condiciones.
# No se permite una inscripción duplicada.
*Trazabilidad:* RF-06-1 · RF-06 Capacitaciones, talleres y certificaciones · UR-20 · RNF-17 · Dep.: RF-06-6

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-040: Realizar módulos y registrar avance* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 3 | Puntos originales: 5 | Requisito: RF-06-2
*Historia:* Como socio, quiero avanzar por los módulos de una capacitación, para completarla a mi ritmo.
*Descripción funcional:* Acceso a módulos de capacitaciones inscritas y porcentaje de avance.
*Criterios de aceptación:*
# Solo se accede a módulos de capacitaciones inscritas.
# Completar un módulo actualiza el porcentaje de avance.
# El avance se conserva entre sesiones.
*Trazabilidad:* RF-06-2 · RF-06 Capacitaciones, talleres y certificaciones · UR-21 · RNF-17 · Dep.: RF-06-1

*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-040.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-041: Rendir la evaluación de una capacitación

Sprint: Sprint 4. Tipo: Story. Ítem original: 141. Padre: 6.

*Historia:* Como socio, quiero rendir la evaluación y conocer mi resultado, para aprobar la capacitación.
*Descripción funcional:* Calificación en servidor, puntaje mínimo e intentos máximos.
*Criterios de aceptación:*
# Las respuestas se registran y la calificación se calcula en el servidor.
# Se aprueba al alcanzar el puntaje mínimo configurado.
# Al llegar al máximo de intentos no se permite uno nuevo.
# La aprobación dispara la acreditación de puntos una sola vez.
*Trazabilidad:* RF-06-3 · RF-06 Capacitaciones, talleres y certificaciones · UR-22 · RNF-17 · Dep.: RF-06-2, RF-05-2

### HU-042: Emitir, consultar y descargar certificados

Sprint: Sprint 4. Tipo: Story. Ítem original: 142. Padre: 6.

*Historia:* Como socio, quiero recibir un certificado al aprobar, para acreditar mi formación.
*Descripción funcional:* PDF con código único de verificación.
*Criterios de aceptación:*
# Al aprobar se genera un PDF con datos del socio, la capacitación y la fecha.
# Cada certificado tiene un código de verificación único y no secuencial.
# No se emite certificado sin aprobación.
*Trazabilidad:* RF-06-4 · RF-06 Capacitaciones, talleres y certificaciones · UR-23 · RNF-16 · Dep.: RF-06-3

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-043: Consultar y descargar certificados* | Responsable originalmente asignado: lizriofrio557@gmail.com | Sprint originalmente planificado: Sprint 4 | Puntos originales: 2 | Requisito: RF-06-5
*Historia:* Como socio, quiero ver y descargar mis certificados, para presentarlos cuando los necesite.
*Descripción funcional:* Historial de certificados con descarga.
*Criterios de aceptación:*
# El socio ve el historial de sus certificados.
# Puede descargar cada PDF.
# No puede descargar certificados de otros socios.
*Trazabilidad:* RF-06-5 · RF-06 Capacitaciones, talleres y certificaciones · UR-23 · RNF-10 · Dep.: RF-06-4

*Coordinación:* Responsable principal de esta historia: jgabriel2608@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-043.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-044: Gestionar y supervisar capacitaciones

Sprint: Sprint 3. Tipo: Story. Ítem original: 144. Padre: 6.

*Historia:* Como Responsable de Responsabilidad Social, quiero crear capacitaciones y ver su avance, para gestionar la formación de los socios.
*Descripción funcional:* Módulos, materiales, evaluación y puntaje mínimo, más consulta de inscritos, avance y resultados.
*Criterios de aceptación:*
# Se crean y publican capacitaciones con módulos, materiales, evaluación y puntaje mínimo.
# Los materiales se seleccionan del repositorio de materiales educativos.
# Se consultan inscritos, avance y resultados por capacitación.
*Trazabilidad:* RF-06-6 · RF-06 Capacitaciones, talleres y certificaciones · UR-24 · RNF-26 · Dep.: RF-09-3

### HU-045: Verificar la autenticidad de un certificado

Sprint: Sprint 5. Tipo: Story. Ítem original: 145. Padre: 6.

*Historia:* Como tercero interesado, quiero verificar un certificado con su código, para confirmar que es auténtico.
*Descripción funcional:* Verificación por código sin exponer datos personales adicionales.
*Criterios de aceptación:*
# Al ingresar el código se informa si el certificado es válido.
# Solo se muestran los datos del certificado, sin datos personales adicionales.
# La consulta tiene límite de frecuencia para impedir la enumeración de códigos.
*Trazabilidad:* RF-06-7 · RF-06 Capacitaciones, talleres y certificaciones · UR-23 · RNF-16, RNF-21 · Dep.: RF-06-4

### HU-046: Gestionar talleres

Sprint: Sprint 3. Tipo: Story. Ítem original: 146. Padre: 6.

*Historia:* Como Responsable de Responsabilidad Social, quiero registrar talleres, para organizar actividades presenciales o virtuales.
*Descripción funcional:* Fecha, cupo, lugar o enlace y puntos por asistencia.
*Criterios de aceptación:*
# Se registran talleres presenciales o virtuales con todos sus datos.
# El cupo debe ser mayor que cero.
# Los talleres registrados se pueden consultar y editar.
*Trazabilidad:* RF-06-8 · RF-06 Capacitaciones, talleres y certificaciones · UR-48 · — · Dep.: —

### HU-047: Inscribirse en talleres y registrar asistencia

Sprint: Sprint 4. Tipo: Story. Ítem original: 147. Padre: 6.

*Historia:* Como socio, quiero inscribirme en talleres y que se registre mi asistencia, para obtener los puntos correspondientes.
*Descripción funcional:* Inscripción respetando el cupo; el personal registra la asistencia.
*Criterios de aceptación:*
# La inscripción se bloquea al llenarse el cupo.
# El personal autorizado registra la asistencia.
# La asistencia habilita una única acreditación de puntos.
*Trazabilidad:* RF-06-9 · RF-06 Capacitaciones, talleres y certificaciones · UR-49 · RNF-12 · Dep.: RF-06-8, RF-05-2

### HU-040: Realizar módulos y registrar avance

Sprint: Sprint 3. Tipo: Sub-task. Ítem original: 140. Padre: 139.

*Historia:* Como socio, quiero avanzar por los módulos de una capacitación, para completarla a mi ritmo.
*Descripción funcional:* Acceso a módulos de capacitaciones inscritas y porcentaje de avance.
*Criterios de aceptación:*
# Solo se accede a módulos de capacitaciones inscritas.
# Completar un módulo actualiza el porcentaje de avance.
# El avance se conserva entre sesiones.
*Trazabilidad:* RF-06-2 · RF-06 Capacitaciones, talleres y certificaciones · UR-21 · RNF-17 · Dep.: RF-06-1

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-039.
*Puntos de origen:* 5 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 3.
*Responsable original:* vale0401g@gmail.com.

### HU-043: Consultar y descargar certificados

Sprint: Sprint 4. Tipo: Sub-task. Ítem original: 143. Padre: 142.

*Historia:* Como socio, quiero ver y descargar mis certificados, para presentarlos cuando los necesite.
*Descripción funcional:* Historial de certificados con descarga.
*Criterios de aceptación:*
# El socio ve el historial de sus certificados.
# Puede descargar cada PDF.
# No puede descargar certificados de otros socios.
*Trazabilidad:* RF-06-5 · RF-06 Capacitaciones, talleres y certificaciones · UR-23 · RNF-10 · Dep.: RF-06-4

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-042.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 4.
*Responsable original:* lizriofrio557@gmail.com.

## Requisitos funcionales vigentes

### RF-06-1 Consultar e inscribirse

El sistema deberá permitir al socio consultar las capacitaciones publicadas (descripción, contenido, duración y requisitos) e inscribirse si cumple las condiciones.

UR: UR-20. HU: HU-039. CU: CU-G08.

### RF-06-2 Realizar módulos y registrar avance

El sistema deberá permitir acceder a los módulos de las capacitaciones inscritas, registrar los completados y consultar el porcentaje de avance. El aula calcula el porcentaje entero a partir de los módulos completados de la capacitación. La descarga de material privado de aula exige inscripción en una capacitación publicada, rol de Socio, validación y permiso vigente de participación en Formación.

UR: UR-21. HU: HU-040. CU: CU-G08.

### RF-06-3 Rendir evaluación

El sistema deberá registrar las respuestas, calcular la calificación, determinar la aprobación según el puntaje mínimo y controlar el número máximo de intentos. El aula habilita la evaluación cuando todos los módulos estén completos y queden intentos. La aprobación registra la inscripción en la bitácora.

UR: UR-22. HU: HU-041. CU: CU-G08.

### RF-06-4 Emitir certificado digital

El sistema deberá generar un certificado en PDF con código único de verificación al aprobar una capacitación.

UR: UR-23. HU: HU-042. CU: CU-G08.

### RF-06-5 Consultar y descargar certificados

El sistema deberá permitir al socio consultar el historial de sus certificados y descargarlos.

UR: UR-23. HU: HU-043. CU: CU-G08.

### RF-06-6 Gestionar y supervisar capacitaciones

El sistema deberá permitir a Responsabilidad Social crear y publicar capacitaciones (módulos, materiales, evaluación, puntaje mínimo) y consultar inscritos, avance y resultados.

UR: UR-24. HU: HU-044. CU: CU-G19.

### RF-06-7 Verificar certificado

El sistema deberá permitir comprobar la autenticidad de un certificado ingresando su código, sin exponer datos personales adicionales.

UR: UR-23. HU: HU-045. CU: CU-G19.

### RF-06-8 Gestionar talleres

El sistema deberá permitir a Responsabilidad Social registrar talleres presenciales o virtuales con fecha, cupo, lugar o enlace, y puntos por asistencia.

UR: UR-48. HU: HU-046. CU: CU-G19.

### RF-06-9 Inscripción y asistencia a talleres

El sistema deberá permitir al socio inscribirse respetando el cupo, y al personal autorizado registrar la asistencia, que habilita la acreditación de puntos.

UR: UR-49. HU: HU-047. CU: CU-G08.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-07 Validación y accesibilidad:** Los formularios deberán validar los datos en línea con mensajes que indiquen cómo corregir el error, cumpliendo el contraste y etiquetado de WCAG 2.1 nivel AA.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-16 Verificación de certificados:** Los certificados deberán incluir un código de verificación único y no secuencial, que impida adivinar o alterar certificados válidos.
- **RNF-17 Mensajes de operación:** El sistema deberá mostrar mensajes claros de confirmación, advertencia o error tras cada operación, sin exponer detalles técnicos internos (trazas, consultas o rutas).
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-21 Bloqueo y límite de solicitudes:** El sistema deberá bloquear temporalmente una cuenta durante 15 min tras 5 intentos fallidos de inicio de sesión y limitar la frecuencia de solicitudes en los formularios públicos.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
