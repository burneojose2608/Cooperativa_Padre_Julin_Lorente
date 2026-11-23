# Salud y bienestar

## Objetivo y alcance

*Propósito:* Difundir convenios y contenidos de bienestar e integrarlos a recompensas, sin datos clínicos (COMP: Bienestar).
*Cobertura de historias antes de consolidar:* HU-084 a HU-086 (RF-13-1 a RF-13-3).
*Criterios de finalización:*
# Los convenios vigentes son consultables por el socio.
# Un convenio puede publicarse como recompensa canjeable.
# No existe ningún campo de datos clínicos.
*Sprints:* S3–S5.

*Backlog consolidado (07/11/2026):*
# Historias vigentes: HU-084, HU-085, HU-086.
# Historias incorporadas a otras: Ninguna.
# Se mantiene la cobertura de los 3 requisitos/historias originalmente previstos, con sus criterios dentro de las historias vigentes.

## Reglas vigentes

Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y `../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.

## Historias y escenarios de aceptación

### HU-084: Gestionar convenios de bienestar

Sprint: Sprint 3. Tipo: Story. Ítem original: 184. Padre: 13.

*Historia:* Como Gestor de contenidos, quiero registrar convenios de salud y bienestar, para difundirlos entre los socios.
*Descripción funcional:* Proveedor, descripción, beneficio, condiciones y vigencia.
*Criterios de aceptación:*
# Se registran convenios con todos sus datos.
# Ningún formulario solicita ni almacena datos clínicos o de salud de los socios.
# Los convenios se pueden editar y consultar.
*Trazabilidad:* RF-13-1 · RF-13 Salud y bienestar · UR-55 · RNF-24, RNF-26 · Dep.: —

### HU-085: Consultar convenios y contenidos de bienestar

Sprint: Sprint 3. Tipo: Story. Ítem original: 185. Padre: 13.

*Historia:* Como socio, quiero conocer los convenios de bienestar, para aprovecharlos.
*Descripción funcional:* Convenios vigentes y contenidos de bienestar.
*Criterios de aceptación:*
# El socio ve los convenios vigentes y los contenidos de bienestar.
# Los convenios vencidos no se muestran.
# La vista funciona en pantallas móviles.
*Trazabilidad:* RF-13-2 · RF-13 Salud y bienestar · UR-54 · RNF-24 · Dep.: RF-13-1

### HU-086: Vincular convenios a recompensas

Sprint: Sprint 5. Tipo: Story. Ítem original: 186. Padre: 13.

*Historia:* Como administrador, quiero publicar beneficios de convenios como recompensas, para ampliar el catálogo.
*Descripción funcional:* Beneficios canjeables con puntos vinculados a su convenio.
*Criterios de aceptación:*
# Un convenio puede publicarse como beneficio canjeable con puntos.
# El beneficio queda vinculado a su convenio de origen.
# Si el convenio vence, el beneficio deja de estar disponible.
*Trazabilidad:* RF-13-3 · RF-13 Salud y bienestar · UR-55 · — · Dep.: RF-13-1, RF-08-1

## Requisitos funcionales vigentes

### RF-13-1 Gestionar convenios

El sistema deberá registrar convenios con proveedor, descripción, beneficio, condiciones y vigencia.

UR: UR-55. HU: HU-084. CU: CU-G13.

### RF-13-2 Consultar convenios y contenidos

El sistema deberá permitir al socio consultar los convenios vigentes y los contenidos de bienestar.

UR: UR-54. HU: HU-085. CU: CU-G13.

### RF-13-3 Vincular convenios a recompensas

El sistema deberá publicar beneficios de convenios como recompensas canjeables con puntos.

UR: UR-55. HU: HU-086. CU: CU-G13.

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
- **RNF-24 Exclusión de datos clínicos:** El sistema no deberá solicitar ni almacenar datos clínicos o de salud de los socios. El módulo de bienestar gestionará únicamente información de convenios y contenidos.
- **RNF-26 Validación de archivos:** El sistema deberá validar el tipo, la extensión y el tamaño (máximo 10 MB) de los archivos cargados, renombrarlos y almacenarlos fuera del directorio público.

## Cierre

Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. Las capacidades externas o mediciones no ejecutadas se registran como pendientes.
