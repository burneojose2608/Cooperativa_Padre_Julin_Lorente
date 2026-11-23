# Contenido institucional y gestión de contenidos

## Objetivo y alcance

*Propósito:* Publicar y mantener noticias, comunicados, multimedia y materiales educativos (SS: Contenidos).
*Cobertura de historias antes de consolidar:* HU-060 a HU-065 (RF-09-1 a RF-09-6).
*Criterios de finalización:*
# El gestor publica y retira contenidos con vigencia automática.
# Los archivos se validan y almacenan fuera del directorio público.
# El socio consulta contenidos vigentes por categoría y búsqueda.
*Sprints:* S2–S5.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-060, HU-062, HU-063, HU-065.
# Historias incorporadas a otras: HU-061 → HU-060, HU-064 → HU-060.
# Se mantiene la cobertura de los 6 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-060: Gestionar, publicar y programar contenidos institucionales

Sprint: Sprint 2. Tipo: Story. Ítem original: 160. Padre: 9.

*Historia:* Como Gestor de contenidos, quiero crear, modificar y retirar publicaciones, para mantener informada a la comunidad.
*Descripción funcional:* Título, contenido, categoría, estado y responsable.
*Criterios de aceptación:*
# Se crean, modifican y retiran publicaciones con sus datos.
# El contenido se codifica al mostrarse para prevenir XSS.
# Solo el Gestor de contenidos accede a esta función.
*Trazabilidad:* RF-09-1 · RF-09 Contenido institucional y gestión de contenidos · UR-33 · RNF-20 · Dep.: —

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-061: Publicar noticias y comunicados* | Responsable originalmente asignado: lizriofrio557@gmail.com | Sprint originalmente planificado: Sprint 2 | Puntos originales: 2 | Requisito: RF-09-2
*Historia:* Como Gestor de contenidos, quiero publicar noticias, comunicados y multimedia, para difundir información institucional.
*Descripción funcional:* Publicación de contenido previamente registrado.
*Criterios de aceptación:*
# Una publicación registrada puede pasar a publicada.
# Se admiten noticias, comunicados y multimedia.
# Solo se publica si contiene la información obligatoria.
*Trazabilidad:* RF-09-2 · RF-09 Contenido institucional y gestión de contenidos · UR-33 · RNF-20 · Dep.: RF-09-1

*HU-064: Gestionar la vigencia de contenidos* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 3 | Puntos originales: 2 | Requisito: RF-09-5
*Historia:* Como Gestor de contenidos, quiero programar la vigencia, para que lo vencido se oculte solo.
*Descripción funcional:* Fechas de inicio y fin con ocultamiento automático.
*Criterios de aceptación:*
# Se programan fechas de inicio y fin.
# Al vencer, el contenido se oculta automáticamente.
# Un contenido con inicio futuro no se muestra antes de tiempo.
*Trazabilidad:* RF-09-5 · RF-09 Contenido institucional y gestión de contenidos · UR-33 · — · Dep.: RF-09-1

*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-061, HU-064.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-062: Gestionar materiales educativos

Sprint: Sprint 2. Tipo: Story. Ítem original: 162. Padre: 9.

*Historia:* Como Gestor de contenidos o Responsable de Responsabilidad Social, quiero organizar materiales educativos, para reutilizarlos en capacitaciones.
*Descripción funcional:* Organización por categoría y formato.
*Criterios de aceptación:*
# Los materiales se organizan por categoría y formato.
# Los archivos se validan por tipo, extensión y tamaño ≤ 10 MB, se renombran y se guardan fuera del directorio público.
# Los materiales pueden reutilizarse en capacitaciones.
# Se pueden editar y eliminar.
*Trazabilidad:* RF-09-3 · RF-09 Contenido institucional y gestión de contenidos · UR-34 · RNF-26 · Dep.: —

### HU-063: Consultar contenido institucional

Sprint: Sprint 3. Tipo: Story. Ítem original: 163. Padre: 9.

*Historia:* Como socio, quiero leer noticias y materiales publicados, para estar informado.
*Descripción funcional:* Contenidos vigentes por categoría y búsqueda.
*Criterios de aceptación:*
# El socio ve los contenidos vigentes por categoría.
# Puede buscar por texto.
# No se muestran contenidos retirados ni vencidos.
*Trazabilidad:* RF-09-4 · RF-09 Contenido institucional y gestión de contenidos · UR-35 · RNF-03 · Dep.: RF-09-2

### HU-065: Aprobar contenido antes de publicarlo

Sprint: Sprint 5. Tipo: Story. Ítem original: 165. Padre: 9.

*Historia:* Como responsable designado, quiero aprobar contenidos, para controlar lo que se publica.
*Descripción funcional:* Flujo de aprobación opcional.
*Criterios de aceptación:*
# Con el flujo activo, el contenido queda pendiente de aprobación.
# Solo el responsable designado puede aprobar.
# Se registran el aprobador y la fecha.
*Trazabilidad:* RF-09-6 · RF-09 Contenido institucional y gestión de contenidos · UR-33 · — · Dep.: RF-09-1

### HU-061: Publicar noticias y comunicados

Sprint: Sprint 2. Tipo: Sub-task. Ítem original: 161. Padre: 160.

*Historia:* Como Gestor de contenidos, quiero publicar noticias, comunicados y multimedia, para difundir información institucional.
*Descripción funcional:* Publicación de contenido previamente registrado.
*Criterios de aceptación:*
# Una publicación registrada puede pasar a publicada.
# Se admiten noticias, comunicados y multimedia.
# Solo se publica si contiene la información obligatoria.
*Trazabilidad:* RF-09-2 · RF-09 Contenido institucional y gestión de contenidos · UR-33 · RNF-20 · Dep.: RF-09-1

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-060.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 2.
*Responsable original:* lizriofrio557@gmail.com.

### HU-064: Gestionar la vigencia de contenidos

Sprint: Sprint 2. Tipo: Sub-task. Ítem original: 164. Padre: 160.

*Historia:* Como Gestor de contenidos, quiero programar la vigencia, para que lo vencido se oculte solo.
*Descripción funcional:* Fechas de inicio y fin con ocultamiento automático.
*Criterios de aceptación:*
# Se programan fechas de inicio y fin.
# Al vencer, el contenido se oculta automáticamente.
# Un contenido con inicio futuro no se muestra antes de tiempo.
*Trazabilidad:* RF-09-5 · RF-09 Contenido institucional y gestión de contenidos · UR-33 · — · Dep.: RF-09-1

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-060.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 3.
*Responsable original:* vale0401g@gmail.com.

## Requisitos funcionales vigentes

### RF-09-1 Gestionar contenido institucional

El sistema deberá permitir crear, modificar y retirar publicaciones con título, contenido, categoría, estado y responsable.

UR: UR-33. HU: HU-060. CU: CU-G22.

### RF-09-2 Publicar noticias y comunicados

El sistema deberá publicar noticias, comunicados y contenido multimedia previamente registrado.

UR: UR-33. HU: HU-061. CU: CU-G22.

### RF-09-3 Gestionar materiales educativos

El sistema deberá organizar los materiales de educación financiera por categoría y formato, reutilizables en las capacitaciones.

UR: UR-34. HU: HU-062. CU: CU-G22.

### RF-09-4 Consultar contenido

El sistema deberá permitir al socio visualizar los contenidos vigentes por categoría y búsqueda.

UR: UR-35. HU: HU-063. CU: CU-G11.

### RF-09-5 Gestionar vigencia

El sistema deberá programar fechas de inicio y fin, ocultando automáticamente los contenidos vencidos.

UR: UR-33. HU: HU-064. CU: CU-G22.

### RF-09-6 Aprobar contenido

Cuando el flujo de aprobación esté activo, el sistema deberá publicar solo los contenidos autorizados por el responsable designado.

UR: UR-33. HU: HU-065. CU: CU-G22.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.
- **RNF-26 Validación de archivos:** El sistema deberá validar el tipo, la extensión y el tamaño (máximo 10 MB) de los archivos cargados, renombrarlos y almacenarlos fuera del directorio público.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
