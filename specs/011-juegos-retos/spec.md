# Juegos y retos

## Objetivo y alcance

*Propósito:* Ofrecer juegos de educación financiera y retos que otorgan puntos (SS: Juegos).
*Cobertura de historias antes de consolidar:* HU-071 a HU-078 (RF-11-1 a RF-11-8).
*Criterios de finalización:*
# Juegos de tipos predefinidos con resultado calculado en el servidor.
# Límite de intentos respetado.
# Los retos otorgan la recompensa una sola vez.
*Sprints:* S4–S5.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-071, HU-073, HU-075, HU-077, HU-078.
# Historias incorporadas a otras: HU-072 → HU-071, HU-074 → HU-073, HU-076 → HU-073.
# Se mantiene la cobertura de los 8 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-071: Registrar y administrar juegos educativos

Sprint: Sprint 4. Tipo: Story. Ítem original: 171. Padre: 11.

*Historia:* Como Gestor de contenidos, quiero administrar la configuración de los juegos, para controlar su disponibilidad.
*Descripción funcional:* Información, condiciones, límite de intentos y disponibilidad.
*Criterios de aceptación:*
# Se modifican la información, las condiciones y el límite de intentos.
# Un juego se puede activar o desactivar.
# Solo el Gestor o el Administrador pueden hacerlo.
*Trazabilidad:* RF-11-1 · RF-11 Juegos y retos · UR-39 · — · Dep.: RF-11-2

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-072: Registrar juegos de tipos predefinidos* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 4 | Puntos originales: 5 | Requisito: RF-11-2
*Historia:* Como Gestor de contenidos, quiero registrar juegos educativos, para ofrecer actividades interactivas.
*Descripción funcional:* Tipos trivia, verdadero/falso y emparejar conceptos.
*Criterios de aceptación:*
# Se registran juegos de los tres tipos predefinidos.
# Cada juego exige nombre, instrucciones, banco de preguntas y criterios de puntuación y finalización.
# No se registra un juego sin instrucciones.
*Trazabilidad:* RF-11-2 · RF-11 Juegos y retos · UR-39 · — · Dep.: —

*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-072.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-073: Participar en juegos con resultados y límite de intentos

Sprint: Sprint 4. Tipo: Story. Ítem original: 173. Padre: 11.

*Historia:* Como socio, quiero jugar juegos de educación financiera, para aprender y ganar puntos.
*Descripción funcional:* Consulta de juegos disponibles e inicio de partida.
*Criterios de aceptación:*
# El socio ve los juegos activos.
# Puede iniciar una partida si cumple las condiciones.
# La interfaz funciona en pantallas móviles.
*Trazabilidad:* RF-11-3 · RF-11 Juegos y retos · UR-40 · RNF-03 · Dep.: RF-11-1

*Consolidación de historias (07/11/2026):*
Esta historia integra las funcionalidades siguientes, que ya no se gestionan como historias independientes. Se conservan los requisitos, criterios de aceptación y trazabilidad originales:

*HU-074: Finalizar partida y calcular resultado* | Responsable originalmente asignado: jgabriel2608@gmail.com | Sprint originalmente planificado: Sprint 4 | Puntos originales: 3 | Requisito: RF-11-4
*Historia:* Como administrador, quiero que el resultado se calcule en el servidor, para evitar manipulación de puntajes.
*Descripción funcional:* Cálculo según los criterios configurados.
*Criterios de aceptación:*
# El resultado se calcula en el servidor; el cliente no envía la puntuación final.
# La partida finaliza al cumplirse los criterios configurados.
# Se muestra la puntuación al socio.
*Trazabilidad:* RF-11-4 · RF-11 Juegos y retos · UR-40 · RNF-20 · Dep.: RF-11-3

*HU-076: Validar el límite de intentos* | Responsable originalmente asignado: vale0401g@gmail.com | Sprint originalmente planificado: Sprint 4 | Puntos originales: 2 | Requisito: RF-11-6
*Historia:* Como Gestor de contenidos, quiero limitar los intentos por juego, para mantener la equidad.
*Descripción funcional:* Bloqueo al alcanzar el límite configurado.
*Criterios de aceptación:*
# Se cuentan los intentos por socio y juego.
# Al alcanzar el límite, el servidor impide iniciar una nueva partida.
# Se informa al socio cuántos intentos le quedan.
*Trazabilidad:* RF-11-6 · RF-11 Juegos y retos · UR-40 · — · Dep.: RF-11-1

*Coordinación:* Responsable principal de esta historia: lizriofrio557@gmail.com. Los responsables originales de los requisitos integrados se mantienen identificados para la distribución del trabajo técnico.
*Estimación consolidada:* Suma de los puntos originales de las historias integradas; pendiente de reestimación del equipo.

*Subtareas vinculadas:* HU-074, HU-076.
*Responsables y criterios específicos:* Se conservan en cada subtarea.
*Estimación de la historia:* Incluye el esfuerzo original de las subtareas; no sumar nuevamente sus estimaciones históricas.

### HU-075: Registrar resultados de juegos

Sprint: Sprint 5. Tipo: Story. Ítem original: 175. Padre: 11.

*Historia:* Como socio, quiero que mis resultados queden registrados, para consultar mis reconocimientos.
*Descripción funcional:* Participante, juego, fecha y puntuación, con envío a gamificación.
*Criterios de aceptación:*
# Se registran participante, juego, fecha y puntuación.
# Solo los resultados válidos se envían a gamificación.
# El socio consulta sus resultados y reconocimientos.
*Trazabilidad:* RF-11-5 · RF-11 Juegos y retos · UR-41 · RNF-12 · Dep.: RF-11-4, RF-05-2

### HU-077: Gestionar retos

Sprint: Sprint 4. Tipo: Story. Ítem original: 177. Padre: 11.

*Historia:* Como Gestor de contenidos o Responsable de Marketing, quiero crear retos medibles, para motivar la participación constante.
*Descripción funcional:* Objetivo medible, vigencia y recompensa.
*Criterios de aceptación:*
# Se crean retos con objetivo, vigencia y recompensa.
# El objetivo se define como tipo de actividad y cantidad (p. ej., 2 capacitaciones en el mes).
# Los retos se pueden consultar y editar.
*Trazabilidad:* RF-11-7 · RF-11 Juegos y retos · UR-50 · — · Dep.: RF-05-1

### HU-078: Participar en retos

Sprint: Sprint 5. Tipo: Story. Ítem original: 178. Padre: 11.

*Historia:* Como socio, quiero ver mi progreso en los retos, para cumplirlos y recibir la recompensa.
*Descripción funcional:* Retos vigentes, progreso y recompensa única.
*Criterios de aceptación:*
# El socio ve los retos vigentes y su progreso.
# Al cumplir el objetivo recibe la recompensa una sola vez.
# Los retos vencidos no otorgan recompensa.
*Trazabilidad:* RF-11-8 · RF-11 Juegos y retos · UR-51 · RNF-12 · Dep.: RF-11-7, RF-05-2

### HU-072: Registrar juegos de tipos predefinidos

Sprint: Sprint 4. Tipo: Sub-task. Ítem original: 172. Padre: 171.

*Historia:* Como Gestor de contenidos, quiero registrar juegos educativos, para ofrecer actividades interactivas.
*Descripción funcional:* Tipos trivia, verdadero/falso y emparejar conceptos.
*Criterios de aceptación:*
# Se registran juegos de los tres tipos predefinidos.
# Cada juego exige nombre, instrucciones, banco de preguntas y criterios de puntuación y finalización.
# No se registra un juego sin instrucciones.
*Trazabilidad:* RF-11-2 · RF-11 Juegos y retos · UR-39 · — · Dep.: —

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-071.
*Puntos de origen:* 5 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 4.
*Responsable original:* vale0401g@gmail.com.

### HU-074: Finalizar partida y calcular resultado

Sprint: Sprint 4. Tipo: Sub-task. Ítem original: 174. Padre: 173.

*Historia:* Como administrador, quiero que el resultado se calcule en el servidor, para evitar manipulación de puntajes.
*Descripción funcional:* Cálculo según los criterios configurados.
*Criterios de aceptación:*
# El resultado se calcula en el servidor; el cliente no envía la puntuación final.
# La partida finaliza al cumplirse los criterios configurados.
# Se muestra la puntuación al socio.
*Trazabilidad:* RF-11-4 · RF-11 Juegos y retos · UR-40 · RNF-20 · Dep.: RF-11-3

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-073.
*Puntos de origen:* 3 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 4.
*Responsable original:* jgabriel2608@gmail.com.

### HU-076: Validar el límite de intentos

Sprint: Sprint 4. Tipo: Sub-task. Ítem original: 176. Padre: 173.

*Historia:* Como Gestor de contenidos, quiero limitar los intentos por juego, para mantener la equidad.
*Descripción funcional:* Bloqueo al alcanzar el límite configurado.
*Criterios de aceptación:*
# Se cuentan los intentos por socio y juego.
# Al alcanzar el límite, el servidor impide iniciar una nueva partida.
# Se informa al socio cuántos intentos le quedan.
*Trazabilidad:* RF-11-6 · RF-11 Juegos y retos · UR-40 · — · Dep.: RF-11-1

*Registro de conversión:* Antes HU independiente; ahora subtarea de HU-073.
*Puntos de origen:* 2 (incluidos en la estimación de la historia principal; no duplicar).
*Sprint original:* Sprint 4.
*Responsable original:* vale0401g@gmail.com.

## Requisitos funcionales vigentes

### RF-11-1 Gestionar juegos

El sistema deberá permitir modificar la información, las condiciones, el límite de intentos y la disponibilidad de los juegos.

UR: UR-39. HU: HU-071. CU: CU-G23.

### RF-11-2 Registrar juegos

El sistema deberá registrar juegos a partir de tipos predefinidos (trivia, verdadero/falso, emparejar conceptos), con nombre, instrucciones, banco de preguntas y criterios de puntuación y finalización.

UR: UR-39. HU: HU-072. CU: CU-G23.

### RF-11-3 Participar en juegos

El sistema deberá permitir al socio consultar los juegos disponibles e iniciar una partida según las condiciones.

UR: UR-40. HU: HU-073. CU: CU-G12.

### RF-11-4 Finalizar juego

El sistema deberá calcular el resultado en el servidor según los criterios configurados y mostrar la puntuación.

UR: UR-40. HU: HU-074. CU: CU-G12.

### RF-11-5 Registrar resultados

El sistema deberá registrar participante, juego, fecha y puntuación, y enviar los resultados válidos a gamificación.

UR: UR-41. HU: HU-075. CU: CU-G12.

### RF-11-6 Validar intentos

El sistema deberá impedir partidas adicionales al alcanzar el límite de intentos configurado.

UR: UR-40. HU: HU-076. CU: CU-G12.

### RF-11-7 Gestionar retos

El sistema deberá crear retos con objetivo medible (por ejemplo, completar 2 capacitaciones en el mes), vigencia y recompensa.

UR: UR-50. HU: HU-077. CU: CU-G23.

### RF-11-8 Participar en retos

El sistema deberá mostrar al socio los retos vigentes y su progreso, y otorgar la recompensa una sola vez al cumplir el objetivo.

UR: UR-51. HU: HU-078. CU: CU-G12.

## Requisitos de calidad

- **RNF-03 Compatibilidad y adaptación de interfaz:** La interfaz deberá tener un diseño mobile-first que funcione entre 320 y 1920 px de ancho en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari.
- **RNF-04 Tiempo de respuesta:** El sistema deberá responder el 95 % de las consultas habituales en un máximo de 2 s con 200 usuarios concurrentes en el entorno de pruebas.
- **RNF-05 Concurrencia y errores:** El sistema deberá soportar 500 usuarios concurrentes con una tasa de errores HTTP 5xx inferior al 1 % durante las pruebas de carga.
- **RNF-08 Disponibilidad:** El sistema deberá mantener una disponibilidad mensual mínima del 99 % durante los 6 meses de mantenimiento, excluyendo los mantenimientos programados y comunicados.
- **RNF-09 HTTPS y HSTS:** El sistema deberá cifrar toda comunicación con HTTPS (TLS 1.2 o superior), redirigir el tráfico HTTP y habilitar HSTS.
- **RNF-10 Autorización y titularidad:** El sistema deberá denegar el acceso por defecto y verificar en el servidor, en cada solicitud, el rol del usuario y la pertenencia del recurso, impidiendo acceder a datos de otros usuarios.
- **RNF-12 Atomicidad e idempotencia de puntos:** El sistema deberá ejecutar las acreditaciones, reservas y descuentos de puntos en transacciones atómicas con clave de idempotencia por acción de origen, garantizando que el saldo nunca sea negativo ni se duplique ante operaciones concurrentes.
- **RNF-15 Copias de seguridad y restauración:** El sistema deberá generar copias de seguridad automáticas cada 24 h, conservarlas al menos 7 días y contar con un procedimiento de restauración documentado y probado antes de la entrega.
- **RNF-19 Arquitectura y cobertura de pruebas:** El sistema deberá separar presentación, lógica de negocio y acceso a datos en módulos desacoplados, con pruebas unitarias que cubran al menos el 70 % de la lógica de referidos, gamificación y canjes.
- **RNF-20 Validación y prevención de inyección:** El sistema deberá validar en el servidor todas las entradas, usar consultas parametrizadas y codificar las salidas para prevenir inyección SQL, XSS y manipulación de parámetros.
- **RNF-23 Datos del MVP:** Durante el MVP, el sistema deberá operar exclusivamente con datos de prueba o anonimizados, sin conexión a los sistemas de producción de la cooperativa.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
