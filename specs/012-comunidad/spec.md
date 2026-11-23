# Comunidad e interacción social

## Objetivo y alcance

*Propósito:* Espacio comunitario moderado solo para socios autenticados (SS: Comunidad).
*Cobertura de historias antes de consolidar:* HU-079 a HU-083 (RF-12-1 a RF-12-5).
*Criterios de finalización:*
# Los socios publican, comentan, reaccionan y reportan.
# El gestor modera y deja registrado el motivo.
# La información personal está oculta por defecto.
*Sprints:* S5.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-079, HU-082, HU-083.
# Historias incorporadas a otras: HU-080 → HU-079, HU-081 → HU-082.
# Se mantiene la cobertura de los 5 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-079: Publicar e interactuar en la comunidad

Sprint: Sprint 5. Tipo: Story. Ítem original: 179. Padre: 12.

*Historia:* Como socio, quiero publicar texto e imágenes, para compartir con otros socios.
*Descripción funcional:* Publicaciones visibles solo para socios autenticados.
*Criterios de aceptación:*
# El socio publica texto e imágenes.
# Solo los socios autenticados ven las publicaciones.
# Las imágenes se validan por tipo, extensión y tamaño ≤ 10 MB.
*Trazabilidad:* RF-12-1 · RF-12 Comunidad e interacción social · UR-52 · RNF-20, RNF-26 · Dep.: RF-12-3, RF-12-4

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-080: Interactuar con publicaciones* | Responsable originalmente asignado: lizriofrio557@gmail.com | Sprint originalmente planificado: Sprint 5 | Puntos originales: 3 | Requisito: RF-12-2
*Historia:* Como socio, quiero reaccionar y comentar, para participar en la comunidad.
*Descripción funcional:* Reacciones y comentarios.
*Criterios de aceptación:*
# El socio puede reaccionar y comentar.
# Los comentarios se codifican al mostrarse.
# El contenido oculto por moderación no admite interacción.
*Trazabilidad:* RF-12-2 · RF-12 Comunidad e interacción social · UR-52 · RNF-20 · Dep.: RF-12-1

*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-080.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-082: Gestionar reportes y moderar la comunidad

Sprint: Sprint 5. Tipo: Story. Ítem original: 182. Padre: 12.

*Historia:* Como Gestor de contenidos, quiero moderar publicaciones reportadas, para proteger a la comunidad.
*Descripción funcional:* Revisión de reportes, ocultamiento o eliminación y suspensión temporal.
*Criterios de aceptación:*
# El gestor revisa los reportes.
# Puede ocultar o eliminar contenido y suspender temporalmente a un socio.
# Cada acción registra el motivo.
*Trazabilidad:* RF-12-4 · RF-12 Comunidad e interacción social · UR-53 · RNF-06, RNF-14 · Dep.: RF-12-3

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-081: Reportar contenido inapropiado* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 5 | Puntos originales: 2 | Requisito: RF-12-3
*Historia:* Como socio, quiero reportar contenido inapropiado, para mantener sano el espacio.
*Descripción funcional:* Reporte de publicaciones o comentarios con motivo.
*Criterios de aceptación:*
# Se reporta una publicación o comentario indicando el motivo.
# El reporte llega a la cola de moderación.
# Se registran quién reporta y la fecha.
*Trazabilidad:* RF-12-3 · RF-12 Comunidad e interacción social · UR-52 · RNF-06 · Dep.: —

*Coordinación:* Responsable principal de esta historia: jgabriel2608@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-081.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-083: Configurar el perfil público

Sprint: Sprint 5. Tipo: Story. Ítem original: 183. Padre: 12.

*Historia:* Como socio, quiero elegir mi alias y los datos visibles, para controlar mi privacidad.
En los comentarios del muro privado, mostrar el alias elegido o, si falta, el primer nombre del autor. Mantener privados los apellidos y los datos de cuenta.

*Descripción funcional:* Alias y datos visibles, con la información personal oculta por defecto.
*Criterios de aceptación:*
# El socio define un alias y los datos visibles.
# Por defecto la información personal está oculta.
# La comunidad solo muestra los datos elegidos.
*Trazabilidad:* RF-12-5 · RF-12 Comunidad e interacción social · UR-52 · RNF-14 · Dep.: —

### HU-080: Interactuar con publicaciones

Sprint: Sprint 5. Tipo: Sub-task. Ítem original: 180. Padre: 179.

*Historia:* Como socio, quiero reaccionar y comentar, para participar en la comunidad.
*Descripción funcional:* Reacciones y comentarios.
*Criterios de aceptación:*
# El socio puede reaccionar y comentar.
# Los comentarios se codifican al mostrarse.
# El contenido oculto por moderación no admite interacción.
*Trazabilidad:* RF-12-2 · RF-12 Comunidad e interacción social · UR-52 · RNF-20 · Dep.: RF-12-1

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-079.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 5.
*Responsable original:* lizriofrio557@gmail.com.

### HU-081: Reportar contenido inapropiado

Sprint: Sprint 5. Tipo: Sub-task. Ítem original: 181. Padre: 182.

*Historia:* Como socio, quiero reportar contenido inapropiado, para mantener sano el espacio.
*Descripción funcional:* Reporte de publicaciones o comentarios con motivo.
*Criterios de aceptación:*
# Se reporta una publicación o comentario indicando el motivo.
# El reporte llega a la cola de moderación.
# Se registran quién reporta y la fecha.
*Trazabilidad:* RF-12-3 · RF-12 Comunidad e interacción social · UR-52 · RNF-06 · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-082.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 5.
*Responsable original:* vale0401g@gmail.com.

## Requisitos funcionales vigentes

### RF-12-1 Publicar en la comunidad

El sistema deberá permitir a los socios publicar texto e imágenes visibles solo para socios autenticados.

UR: UR-52. HU: HU-079. CU: CU-G12.

### RF-12-2 Interactuar con publicaciones

El sistema deberá permitir reaccionar y comentar publicaciones.

UR: UR-52. HU: HU-080. CU: CU-G12.

### RF-12-3 Reportar contenido

El sistema deberá permitir reportar publicaciones o comentarios inapropiados indicando el motivo.

UR: UR-52. HU: HU-081. CU: CU-G12.

### RF-12-4 Moderar comunidad

El sistema deberá permitir al gestor de contenidos revisar reportes, ocultar o eliminar contenido y suspender temporalmente a un socio, registrando el motivo.

UR: UR-53. HU: HU-082. CU: CU-G24.

### RF-12-5 Configurar perfil público

El sistema deberá permitir definir un alias y los datos visibles en la comunidad, ocultando por defecto la información personal.

UR: UR-52. HU: HU-083. CU: CU-G12.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-06 Auditoría inmutable:** El sistema deberá registrar en una bitácora de solo inserción las operaciones críticas (usuario, fecha, hora, acción, recurso, resultado e IP), sin permitir su modificación ni eliminación desde la aplicación.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-14 Enmascaramiento y privacidad:** El sistema deberá enmascarar los datos personales (cédula parcial, alias) en listados, reportes, clasificaciones, resultados de sorteos y comunidad, mostrando el dato completo solo a los roles autorizados.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.
- **RNF-26 Validación de archivos:** El sistema deberá validar el tipo, la extensión y el tamaño (máximo 10 MB) de los archivos cargados, renombrarlos y almacenarlos fuera del directorio público.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
