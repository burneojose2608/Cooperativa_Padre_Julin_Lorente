# Sistema de referidos

## Objetivo y alcance

*Propósito:* Gestionar el ciclo completo del referido, desde el código hasta la conversión (SS: Referidos). Núcleo del objetivo de captación del Acta.
*Cobertura de historias antes de consolidar:* HU-016 a HU-024 (RF-03-1 a RF-03-9).
*Criterios de finalización:*
# Un prospecto se registra con código válido, confirma consentimiento y queda asociado al socio.
# El ciclo de estados se respeta y conserva historial.
# La conversión se registra una sola vez y dispara puntos.
*Sprints:* S2–S3.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-016, HU-017, HU-018, HU-021, HU-022.
# Historias incorporadas a otras: HU-019 → HU-016, HU-020 → HU-017, HU-023 → HU-017, HU-024 → HU-018.
# Se mantiene la cobertura de los 9 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

La consulta comercial aplica el permiso de gestión de Referidos. Los datos completos del prospecto se habilitan para el personal autorizado después de confirmar el consentimiento. El socio referente consulta los datos enmascarados. Ver [evidencia por criterio](aceptacion.md).

## Historias y escenarios de aceptación

### HU-016: Generar y compartir mi código de referido

Sprint: Sprint 2. Tipo: Story. Ítem original: 116. Padre: 3.

*Historia:* Como socio, quiero obtener un código de referido único, para recomendar la cooperativa.
*Descripción funcional:* Código único y no secuencial para cada socio validado, consultable desde el perfil.
*Criterios de aceptación:*
# Al validarse un socio se genera un código único y no secuencial.
# El código y su enlace son consultables desde el perfil.
# No existen dos socios con el mismo código (restricción única).
*Trazabilidad:* RF-03-1 · RF-03 Sistema de referidos · UR-08 · RNF-06 · Dep.: RF-01-6

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-019: Compartir código o enlace de referido* | Responsable originalmente asignado: lizriofrio557@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 2 | Requisito: RF-03-4
*Historia:* Como socio, quiero compartir mi código por medios digitales, para invitar a más personas fácilmente.
*Descripción funcional:* Copia y compartición mediante los medios del dispositivo.
*Criterios de aceptación:*
# Un botón copia el código o el enlace con confirmación visual.
# En móviles se abre el menú nativo de compartir.
# Si el navegador no soporta compartir, se ofrece copiar el enlace.
*Trazabilidad:* RF-03-4 · RF-03 Sistema de referidos · UR-08 · RNF-03 · Dep.: RF-03-1

*Coordinación:* Responsable principal de esta historia: vale0401g@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-019.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-017: Registrar prospectos referidos con validaciones y consentimiento

Sprint: Sprint 3. Tipo: Story. Ítem original: 117. Padre: 3.

*Historia:* Como socio o prospecto, quiero registrar una referencia con un código válido, para quedar asociado al socio que recomendó.
*Descripción funcional:* El registro lo hace el socio desde su cuenta o el prospecto desde el enlace. Se capturan nombres, teléfono o correo y producto de interés, y se asocia la campaña vigente.
*Criterios de aceptación:*
# Se puede registrar desde la cuenta del socio o desde el enlace público.
# Se capturan los datos requeridos y un código inválido se rechaza.
# El prospecto queda asociado al socio referente y a la campaña vigente cuando corresponda.
# El formulario público tiene límite de frecuencia de solicitudes.
*Trazabilidad:* RF-03-2 · RF-03 Sistema de referidos · UR-09 · RNF-02, RNF-20, RNF-21 · Dep.: RF-03-1, RF-03-5, RF-03-8

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-020: Prevenir referidos inválidos* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 3 | Requisito: RF-03-5
*Historia:* Como Responsable de Marketing, quiero que se rechacen los referidos inválidos, para que los incentivos sean justos.
*Descripción funcional:* Se comparan cédula, correo y teléfono contra el socio referente, el padrón y los referidos activos.
*Criterios de aceptación:*
# Se rechazan los autorreferidos.
# Se rechazan prospectos que ya son socios según el padrón de prueba.
# Se rechazan prospectos con un referido activo previo.
# El mensaje de rechazo no revela datos de terceros.
*Trazabilidad:* RF-03-5 · RF-03 Sistema de referidos · UR-44 · RNF-17 · Dep.: RF-01-6

*HU-023: Confirmar el consentimiento del prospecto* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 5 | Requisito: RF-03-8
*Historia:* Como prospecto, quiero aceptar el tratamiento de mis datos antes de ser contactado, para que se respete mi privacidad.
*Descripción funcional:* Solicitud de consentimiento con plazo configurable; sin confirmación, el referido expira.
*Criterios de aceptación:*
# Tras el registro, el prospecto recibe una solicitud de aceptación.
# La aceptación registra fecha, hora y versión de la política, y el referido pasa a Confirmado.
# Sin confirmación dentro del plazo configurado, el referido pasa a Expirado.
*Trazabilidad:* RF-03-8 · RF-03 Sistema de referidos · UR-43 · RNF-02, RNF-25 · Dep.: RF-10-3

*Coordinación:* Responsable principal de esta historia: jgabriel2608@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-020, HU-023.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-018: Gestionar seguimiento, estados y conversión de referidos

Sprint: Sprint 3. Tipo: Story. Ítem original: 118. Padre: 3.

*Historia:* Como Responsable de Marketing, quiero registrar cuándo un referido se convierte, para reconocer al socio que lo recomendó.
*Descripción funcional:* Registro de apertura de cuenta o aprobación de producto crediticio, una sola vez por prospecto, con datos de prueba.
*Criterios de aceptación:*
# El personal autorizado registra la conversión con datos de prueba.
# Solo se acepta una conversión por prospecto; un segundo intento se rechaza.
# La conversión dispara una única acreditación de puntos al socio referente.
# El cambio de estado queda en el historial con responsable y fecha.
*Trazabilidad:* RF-03-3 · RF-03 Sistema de referidos · UR-11 · RNF-06, RNF-12, RNF-13 · Dep.: RF-03-9, RF-05-2

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-024: Gestionar los estados del referido* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 5 | Requisito: RF-03-9
*Historia:* Como Responsable de Marketing, quiero un ciclo de estados controlado, para dar seguimiento trazable a cada referido.
*Descripción funcional:* Ciclo Registrado → Confirmado → En seguimiento → Convertido / Rechazado / Expirado.
*Criterios de aceptación:*
# Solo se permiten las transiciones definidas.
# El servidor rechaza cualquier transición no permitida.
# Cada cambio guarda estado anterior, estado nuevo, fecha, responsable y observación.
*Trazabilidad:* RF-03-9 · RF-03 Sistema de referidos · UR-10, UR-11 · RNF-06, RNF-13 · Dep.: —

*Coordinación:* Responsable principal de esta historia: vale0401g@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-024.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-021: Consultar mis referidos

Sprint: Sprint 3. Tipo: Story. Ítem original: 121. Padre: 3.

*Historia:* Como socio, quiero ver el estado de mis referidos, para saber si mis recomendaciones avanzan.
*Descripción funcional:* Listado con fecha de registro y estado, con datos personales enmascarados.
*Criterios de aceptación:*
# El socio ve solo sus referidos, con fecha y estado.
# Los datos personales del prospecto aparecen enmascarados.
# Sin referidos se muestra un mensaje informativo.
*Trazabilidad:* RF-03-6 · RF-03 Sistema de referidos · UR-10 · RNF-10, RNF-14 · Dep.: RF-03-9

### HU-022: Consultar resultados de referidos (Marketing)

Sprint: Sprint 3. Tipo: Story. Ítem original: 122. Padre: 3.

*Historia:* Como Responsable de Marketing, quiero consultar y filtrar todos los referidos, para evaluar la captación.
*Descripción funcional:* Consulta de referidos, estados y conversiones con filtros.
*Criterios de aceptación:*
# Marketing ve el listado de referidos, estados y conversiones.
# Puede filtrar por campaña, período, estado y socio referente.
# Los datos completos solo se muestran a roles autorizados.
*Trazabilidad:* RF-03-7 · RF-03 Sistema de referidos · UR-45 · RNF-14 · Dep.: RF-03-9

### HU-019: Compartir código o enlace de referido

Sprint: Sprint 2. Tipo: Sub-task. Ítem original: 119. Padre: 116.

*Historia:* Como socio, quiero compartir mi código por medios digitales, para invitar a más personas fácilmente.
*Descripción funcional:* Copia y compartición mediante los medios del dispositivo.
*Criterios de aceptación:*
# Un botón copia el código o el enlace con confirmación visual.
# En móviles se abre el menú nativo de compartir.
# Si el navegador no soporta compartir, se ofrece copiar el enlace.
*Trazabilidad:* RF-03-4 · RF-03 Sistema de referidos · UR-08 · RNF-03 · Dep.: RF-03-1

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-016.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* lizriofrio557@gmail.com.

### HU-020: Prevenir referidos inválidos

Sprint: Sprint 3. Tipo: Sub-task. Ítem original: 120. Padre: 117.

*Historia:* Como Responsable de Marketing, quiero que se rechacen los referidos inválidos, para que los incentivos sean justos.
*Descripción funcional:* Se comparan cédula, correo y teléfono contra el socio referente, el padrón y los referidos activos.
*Criterios de aceptación:*
# Se rechazan los autorreferidos.
# Se rechazan prospectos que ya son socios según el padrón de prueba.
# Se rechazan prospectos con un referido activo previo.
# El mensaje de rechazo no revela datos de terceros.
*Trazabilidad:* RF-03-5 · RF-03 Sistema de referidos · UR-44 · RNF-17 · Dep.: RF-01-6

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-017.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* vale0401g@gmail.com.

### HU-023: Confirmar el consentimiento del prospecto

Sprint: Sprint 3. Tipo: Sub-task. Ítem original: 123. Padre: 117.

*Historia:* Como prospecto, quiero aceptar el tratamiento de mis datos antes de ser contactado, para que se respete mi privacidad.
*Descripción funcional:* Solicitud de consentimiento con plazo configurable; sin confirmación, el referido expira.
*Criterios de aceptación:*
# Tras el registro, el prospecto recibe una solicitud de aceptación.
# La aceptación registra fecha, hora y versión de la política, y el referido pasa a Confirmado.
# Sin confirmación dentro del plazo configurado, el referido pasa a Expirado.
*Trazabilidad:* RF-03-8 · RF-03 Sistema de referidos · UR-43 · RNF-02, RNF-25 · Dep.: RF-10-3

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-017.
*Puntos de origen:* 5 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* jgabriel2608@gmail.com.

### HU-024: Gestionar los estados del referido

Sprint: Sprint 3. Tipo: Sub-task. Ítem original: 124. Padre: 118.

*Historia:* Como Responsable de Marketing, quiero un ciclo de estados controlado, para dar seguimiento trazable a cada referido.
*Descripción funcional:* Ciclo Registrado → Confirmado → En seguimiento → Convertido / Rechazado / Expirado.
*Criterios de aceptación:*
# Solo se permiten las transiciones definidas.
# El servidor rechaza cualquier transición no permitida.
# Cada cambio guarda estado anterior, estado nuevo, fecha, responsable y observación.
*Trazabilidad:* RF-03-9 · RF-03 Sistema de referidos · UR-10, UR-11 · RNF-06, RNF-13 · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-018.
*Puntos de origen:* 5 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* vale0401g@gmail.com.

## Requisitos funcionales vigentes

### RF-03-1 Generar código de referido

El sistema deberá generar un código único y no secuencial para cada socio validado, consultable desde su perfil.

UR: UR-08. HU: HU-016. CU: CU-G03.

### RF-03-2 Registrar prospecto

El sistema deberá registrar un prospecto con un código válido, ingresado por el socio desde su cuenta o por el prospecto desde el enlace de referido, capturando nombres, teléfono o correo y producto de interés, y asociándolo a la campaña vigente cuando corresponda.

UR: UR-09. HU: HU-017. CU: CU-G04.

### RF-03-3 Validar conversión

El sistema deberá permitir al personal autorizado registrar la conversión de un referido (apertura de cuenta o aprobación de producto crediticio) una sola vez por prospecto, disparando la acreditación de puntos.

UR: UR-11. HU: HU-018. CU: CU-G16.

### RF-03-4 Compartir código

El sistema deberá permitir copiar y compartir el código o enlace de referido mediante los medios digitales del dispositivo.

UR: UR-08. HU: HU-019. CU: CU-G03.

### RF-03-5 Prevenir referidos inválidos

El sistema deberá rechazar autorreferidos, prospectos que ya son socios y prospectos con un referido activo previo, comparando cédula, correo y teléfono.

UR: UR-44. HU: HU-020. CU: CU-G15.

### RF-03-6 Consultar mis referidos

El sistema deberá permitir al socio consultar sus referidos con fecha de registro y estado, mostrando los datos personales enmascarados.

UR: UR-10. HU: HU-021. CU: CU-G05.

### RF-03-7 Consultar resultados de referidos

El sistema deberá permitir a Marketing consultar referidos, estados y conversiones, con filtros por campaña, período, estado y socio referente.

UR: UR-45. HU: HU-022. CU: CU-G14.

### RF-03-8 Confirmar consentimiento del prospecto

El sistema deberá solicitar al prospecto que acepte el tratamiento de sus datos antes de habilitar su seguimiento. Si no confirma dentro del plazo configurado, el referido expira.

UR: UR-43. HU: HU-023. CU: CU-G04.

### RF-03-9 Gestionar estados del referido

El sistema deberá administrar el ciclo Registrado → Confirmado → En seguimiento → Convertido / Rechazado / Expirado, registrando fecha, responsable y observación de cada cambio.

UR: UR-10, UR-11. HU: HU-024. CU: CU-G15.

## Requisitos de calidad

- **RNF-02 Consentimiento de datos:** El sistema deberá registrar el consentimiento expreso de socios y prospectos para el tratamiento de datos personales, con fecha, hora y versión de la política aceptada.
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
- **RNF-14 Enmascaramiento y privacidad:** El sistema deberá enmascarar los datos personales (cédula parcial, alias) en listados, reportes, clasificaciones, resultados de sorteos y comunidad, mostrando el dato completo solo a los roles autorizados.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-17 Mensajes de operación:** El sistema deberá mostrar mensajes claros de confirmación, advertencia o error tras cada operación, sin exponer detalles técnicos internos (trazas, consultas o rutas).
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-21 Bloqueo y límite de solicitudes:** El sistema deberá bloquear temporalmente una cuenta durante 15 min tras 5 intentos fallidos de inicio de sesión y limitar la frecuencia de solicitudes en los formularios públicos.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.
- **RNF-25 Retención de prospectos:** El sistema deberá anonimizar o eliminar los datos de prospectos no convertidos tras un plazo configurable (12 meses por defecto) o cuando el titular lo solicite.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
