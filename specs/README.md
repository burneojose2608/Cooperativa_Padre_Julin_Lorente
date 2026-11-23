# Alcance y sprints del proyecto

Línea base documental del 20/11/2026. Los criterios se conservan desde las historias y subtareas consolidadas. Las casillas abiertas requieren implementación o comprobación actual; ningún estado se infiere del CSV de Jira.

## Funcionalidades

| Especificación | Historias | Subtareas | Sprints |
| --- | --- | --- | --- |
| [Gestión de usuarios y perfiles](001-usuarios/spec.md) | 4 | 4 | Sprint 1, Sprint 2 |
| [Autenticación y control de acceso](002-autenticacion/spec.md) | 3 | 4 | Sprint 1, Sprint 2 |
| [Sistema de referidos](003-referidos/spec.md) | 5 | 4 | Sprint 2, Sprint 3 |
| [Campañas e incentivos](004-campanas/spec.md) | 4 | 2 | Sprint 3, Sprint 4 |
| [Puntos, niveles, insignias y clasificaciones](005-gamificacion/spec.md) | 7 | 1 | Sprint 2, Sprint 3, Sprint 4 |
| [Capacitaciones, talleres y certificaciones](006-formacion/spec.md) | 7 | 2 | Sprint 3, Sprint 4, Sprint 5 |
| [Sorteos](007-sorteos/spec.md) | 4 | 2 | Sprint 3, Sprint 4, Sprint 5 |
| [Beneficios y recompensas](008-recompensas/spec.md) | 5 | 1 | Sprint 3, Sprint 4 |
| [Contenido institucional y gestión de contenidos](009-contenidos/spec.md) | 4 | 2 | Sprint 2, Sprint 3, Sprint 5 |
| [Notificaciones](010-notificaciones/spec.md) | 5 | 0 | Sprint 2, Sprint 3, Sprint 5 |
| [Juegos y retos](011-juegos-retos/spec.md) | 5 | 3 | Sprint 4, Sprint 5 |
| [Comunidad e interacción social](012-comunidad/spec.md) | 3 | 2 | Sprint 5 |
| [Salud y bienestar](013-bienestar/spec.md) | 3 | 0 | Sprint 3, Sprint 5 |
| [Reportes y estadísticas](014-reportes/spec.md) | 5 | 0 | Sprint 4, Sprint 5 |

## Plan por sprint

### Sprint 0

- T-001: Consolidar requisitos y matriz de trazabilidad (Task, ítem 301, padre sin padre).
- T-002: Definir arquitectura modular por capas (Task, ítem 302, padre sin padre).
- T-003: Elaborar diagramas de casos de uso y actividades (Task, ítem 303, padre sin padre).
- T-004: Elaborar diagramas de clases y secuencia (Task, ítem 304, padre sin padre).
- T-005: Configurar repositorio, CI y entornos (Task, ítem 305, padre sin padre).
- T-006: Diseñar prototipos mobile-first en Figma (Task, ítem 306, padre sin padre).
- T-007: Configurar base del backend con validación y manejo de errores (Task, ítem 307, padre sin padre).
- T-008: Configurar base del frontend responsive (Task, ítem 308, padre sin padre).
- T-009: Implementar hash de contraseñas y política (Task, ítem 309, padre 2).
- T-010: BD: elaborar modelo entidad-relación y diccionario de datos (Task, ítem 310, padre sin padre).
- T-011: BD: migraciones de usuarios, roles, sesiones, consentimientos y padrón (Task, ítem 311, padre 1).
- T-012: BD: scripts de datos de prueba anonimizados (Task, ítem 312, padre sin padre).
- T-013: Implementar interceptor de bitácora de auditoría (Task, ítem 313, padre sin padre).
- T-014: Implementar bloqueo de cuenta y limitación de solicitudes (Task, ítem 314, padre 2).
- T-015: Implementar enmascaramiento de datos personales (Task, ítem 315, padre sin padre).
- T-016: Implementar servicio seguro de carga de archivos (Task, ítem 316, padre 9).
- T-017: BD: crear bitácora de solo inserción (Task, ítem 317, padre sin padre).
- T-018: BD: referidos, prospectos e historial de estados (Task, ítem 318, padre 3).
- T-019: BD: registro inmutable de movimientos de puntos (Task, ítem 319, padre 5).
- T-020: BD: contenidos y materiales educativos (Task, ítem 320, padre 9).
- T-021: BD: notificaciones, plantillas y envíos (Task, ítem 321, padre 10).
- T-022: BD: campañas, segmentación e historial de cambios (Task, ítem 322, padre 4).
- T-023: BD: capacitaciones, evaluaciones, certificados y talleres (Task, ítem 323, padre 6).
- T-024: BD: beneficios, canjes e historial (Task, ítem 324, padre 8).
- T-025: BD: sorteos, participaciones y evidencia (Task, ítem 325, padre 7).
- T-026: BD: convenios de bienestar (Task, ítem 326, padre 13).
- T-027: Ejecutar pruebas de concurrencia e idempotencia de puntos (Task, ítem 327, padre 5).
- T-028: Desplegar en servidor con HTTPS (Task, ítem 328, padre sin padre).
- T-029: Configurar monitoreo de disponibilidad (Task, ítem 329, padre sin padre).
- T-030: BD: juegos, partidas, intentos y retos (Task, ítem 330, padre 11).
- T-031: BD: comunidad (Task, ítem 331, padre 12).
- T-032: BD: consultas e índices para reportes (Task, ítem 332, padre 14).
- T-033: BD: copias de seguridad automáticas (Task, ítem 333, padre sin padre).
- T-034: BD: anonimización de prospectos no convertidos (Task, ítem 334, padre 3).
- T-035: Ejecutar pruebas de carga y rendimiento (Task, ítem 335, padre sin padre).
- T-036: Ejecutar pruebas de control de acceso y sesiones (Task, ítem 336, padre sin padre).
- T-037: Ejecutar pruebas de seguridad OWASP (Task, ítem 337, padre sin padre).
- T-038: Preparar la entrega y la documentación final (Task, ítem 338, padre sin padre).
- T-039: Ejecutar pruebas unitarias con cobertura ≥ 70 % (Task, ítem 339, padre sin padre).
- T-040: Ejecutar pruebas de integración referidos → puntos → canjes (Task, ítem 340, padre sin padre).
- T-041: Ejecutar pruebas de compatibilidad (Task, ítem 341, padre sin padre).
- T-042: Auditar accesibilidad WCAG y mensajes del sistema (Task, ítem 342, padre sin padre).
- T-043: Ejecutar pruebas funcionales E2E y corregir defectos (Task, ítem 343, padre sin padre).
- T-044: BD: pruebas de persistencia y optimización de consultas (Task, ítem 344, padre sin padre).
- T-045: BD: prueba de restauración de copia de seguridad (Task, ítem 345, padre sin padre).

### Sprint 1

- HU-001: Registrar socio con validación de cédula, padrón y duplicados (Story, ítem 101, padre 1).
- HU-009: Iniciar y cerrar sesión con validación de credenciales y roles (Story, ítem 109, padre 2).
- HU-006: Validar la condición de socio activo (Sub-task, ítem 106, padre 101).
- HU-008: Prevenir cuentas duplicadas (Sub-task, ítem 108, padre 101).
- HU-010: Validar credenciales de acceso (Sub-task, ítem 110, padre 109).
- HU-012: Identificar los roles del usuario autenticado (Sub-task, ítem 112, padre 109).
- HU-015: Cerrar sesión e invalidarla en el servidor (Sub-task, ítem 115, padre 109).

### Sprint 2

- HU-002: Consultar y actualizar mi perfil (Story, ítem 102, padre 1).
- HU-004: Cambiar la contraseña (Story, ítem 104, padre 1).
- HU-005: Administrar cuentas de usuarios y sus estados (Story, ítem 105, padre 1).
- HU-011: Recuperar la contraseña por correo (Story, ítem 111, padre 2).
- HU-013: Administrar roles, permisos y acceso seguro (Story, ítem 113, padre 2).
- HU-016: Generar y compartir mi código de referido (Story, ítem 116, padre 3).
- HU-031: Configurar reglas de puntuación (Story, ítem 131, padre 5).
- HU-060: Gestionar, publicar y programar contenidos institucionales (Story, ítem 160, padre 9).
- HU-062: Gestionar materiales educativos (Story, ítem 162, padre 9).
- HU-068: Enviar notificaciones automáticas (Story, ítem 168, padre 10).
- HU-069: Consultar la bandeja de notificaciones (Story, ítem 169, padre 10).
- HU-003: Editar los datos de contacto del perfil (Sub-task, ítem 103, padre 102).
- HU-007: Gestionar el estado de las cuentas (Sub-task, ítem 107, padre 105).
- HU-014: Autorizar el acceso según rol en el servidor (Sub-task, ítem 114, padre 113).
- HU-019: Compartir código o enlace de referido (Sub-task, ítem 119, padre 116).
- HU-061: Publicar noticias y comunicados (Sub-task, ítem 161, padre 160).
- HU-064: Gestionar la vigencia de contenidos (Sub-task, ítem 164, padre 160).

### Sprint 3

- HU-017: Registrar prospectos referidos con validaciones y consentimiento (Story, ítem 117, padre 3).
- HU-018: Gestionar seguimiento, estados y conversión de referidos (Story, ítem 118, padre 3).
- HU-021: Consultar mis referidos (Story, ítem 121, padre 3).
- HU-022: Consultar resultados de referidos (Marketing) (Story, ítem 122, padre 3).
- HU-025: Crear y activar campañas (Story, ítem 125, padre 4).
- HU-027: Consultar campañas vigentes (Story, ítem 127, padre 4).
- HU-032: Acreditar puntos y registrar movimientos inmutables (Story, ítem 132, padre 5).
- HU-034: Consultar puntos y logros (Story, ítem 134, padre 5).
- HU-037: Configurar niveles e insignias (Story, ítem 137, padre 5).
- HU-039: Inscribirme y avanzar en capacitaciones (Story, ítem 139, padre 6).
- HU-044: Gestionar y supervisar capacitaciones (Story, ítem 144, padre 6).
- HU-046: Gestionar talleres (Story, ítem 146, padre 6).
- HU-048: Configurar sorteos (Story, ítem 148, padre 7).
- HU-054: Configurar beneficios (Story, ítem 154, padre 8).
- HU-057: Consultar beneficios disponibles (Story, ítem 157, padre 8).
- HU-063: Consultar contenido institucional (Story, ítem 163, padre 9).
- HU-066: Gestionar plantillas de notificación (Story, ítem 166, padre 10).
- HU-084: Gestionar convenios de bienestar (Story, ítem 184, padre 13).
- HU-085: Consultar convenios y contenidos de bienestar (Story, ítem 185, padre 13).
- HU-020: Prevenir referidos inválidos (Sub-task, ítem 120, padre 117).
- HU-023: Confirmar el consentimiento del prospecto (Sub-task, ítem 123, padre 117).
- HU-024: Gestionar los estados del referido (Sub-task, ítem 124, padre 118).
- HU-026: Gestionar el estado de las campañas (Sub-task, ítem 126, padre 125).
- HU-036: Registrar movimientos inmutables de puntos (Sub-task, ítem 136, padre 132).
- HU-040: Realizar módulos y registrar avance (Sub-task, ítem 140, padre 139).

### Sprint 4

- HU-028: Segmentar y modificar campañas con historial (Story, ítem 128, padre 4).
- HU-030: Monitorear los resultados de una campaña (Story, ítem 130, padre 4).
- HU-033: Calcular nivel e insignias (Story, ítem 133, padre 5).
- HU-035: Consultar clasificaciones (Story, ítem 135, padre 5).
- HU-038: Revertir puntos de acciones invalidadas (Story, ítem 138, padre 5).
- HU-041: Rendir la evaluación de una capacitación (Story, ítem 141, padre 6).
- HU-042: Emitir, consultar y descargar certificados (Story, ítem 142, padre 6).
- HU-047: Inscribirse en talleres y registrar asistencia (Story, ítem 147, padre 6).
- HU-049: Generar participaciones en sorteos (Story, ítem 149, padre 7).
- HU-055: Solicitar canjes con reserva, descuento y liberación segura de puntos (Story, ítem 155, padre 8).
- HU-056: Gestionar y entregar canjes (Story, ítem 156, padre 8).
- HU-058: Consultar historial de canjes (Story, ítem 158, padre 8).
- HU-071: Registrar y administrar juegos educativos (Story, ítem 171, padre 11).
- HU-073: Participar en juegos con resultados y límite de intentos (Story, ítem 173, padre 11).
- HU-077: Gestionar retos (Story, ítem 177, padre 11).
- HU-087: Visualizar el panel de supervisión (Story, ítem 187, padre 14).
- HU-088: Generar reporte de referidos y campañas (Story, ítem 188, padre 14).
- HU-029: Modificar campañas conservando el historial (Sub-task, ítem 129, padre 128).
- HU-043: Consultar y descargar certificados (Sub-task, ítem 143, padre 142).
- HU-059: Reservar, descontar y liberar puntos de canjes (Sub-task, ítem 159, padre 155).
- HU-072: Registrar juegos de tipos predefinidos (Sub-task, ítem 172, padre 171).
- HU-074: Finalizar partida y calcular resultado (Sub-task, ítem 174, padre 173).
- HU-076: Validar el límite de intentos (Sub-task, ítem 176, padre 173).

### Sprint 5

- HU-045: Verificar la autenticidad de un certificado (Story, ítem 145, padre 6).
- HU-050: Ejecutar sorteos, notificar ganadores y auditar resultados (Story, ítem 150, padre 7).
- HU-051: Consultar resultados de sorteos (Story, ítem 151, padre 7).
- HU-065: Aprobar contenido antes de publicarlo (Story, ítem 165, padre 9).
- HU-067: Gestionar preferencias de notificación (Story, ítem 167, padre 10).
- HU-070: Consultar el historial de envíos (Story, ítem 170, padre 10).
- HU-075: Registrar resultados de juegos (Story, ítem 175, padre 11).
- HU-078: Participar en retos (Story, ítem 178, padre 11).
- HU-079: Publicar e interactuar en la comunidad (Story, ítem 179, padre 12).
- HU-082: Gestionar reportes y moderar la comunidad (Story, ítem 182, padre 12).
- HU-083: Configurar el perfil público (Story, ítem 183, padre 12).
- HU-086: Vincular convenios a recompensas (Story, ítem 186, padre 13).
- HU-089: Generar reporte de impacto social (Story, ítem 189, padre 14).
- HU-090: Generar reporte de gamificación y recompensas (Story, ítem 190, padre 14).
- HU-091: Exportar reportes en PDF y Excel/CSV (Story, ítem 191, padre 14).
- HU-052: Notificar a los ganadores (Sub-task, ítem 152, padre 150).
- HU-053: Consultar el historial de sorteos (Sub-task, ítem 153, padre 150).
- HU-080: Interactuar con publicaciones (Sub-task, ítem 180, padre 179).
- HU-081: Reportar contenido inapropiado (Sub-task, ítem 181, padre 182).

## Integridad de las fuentes

SHA-256 del backlog original: `c5366273de629e063c1db07621baa763b1223279664817310d4466a4eacc49fa`.

El catálogo `trazabilidad.csv` relaciona las historias y subtareas con los RF, UR y CU vigentes. Las tareas técnicas de Sprint 0 están incluidas en el plan por sprint y conservadas en `backlog.json`.

Para revisar una funcionalidad, seguir el RF de la matriz hacia la HU y su criterio en `spec.md`. En `tasks.md`, las cinco tareas de la HU citan su RF y la tarea `-P` enlaza el criterio que debe verificarse. Registrar el identificador del caso, el resultado, el entorno y la evidencia. En las historias consolidadas, comprobar también los criterios de sus subtareas, que conservan sus propios RF.

El [plan transversal](000-plataforma/plan.md) conecta los recorridos entre módulos. Sus [tareas de verificación](000-plataforma/tasks.md#verificación-transversal-de-rnf) relacionan los 26 RNF con las tareas originales de Sprint 0 y la evidencia requerida para cada uno.
