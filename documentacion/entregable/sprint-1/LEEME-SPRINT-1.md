# Sprint 1 desarrollado

## Alcance

Dos historias principales, HU-001 y HU-009, y cinco subtareas: HU-006, HU-008, HU-010, HU-012 y HU-015. Incluyen registro, padrón, duplicados, autenticación, auditoría, roles y cierre de sesión revocable con quince minutos de inactividad. Se conserva la ampliación temporal de conversión administrativa.

La [matriz de criterios](matriz-trazabilidad.md) relaciona cada requisito con implementación y pruebas. Las reglas que sustituyen criterios del CSV original están en [cambios de línea base](../CAMBIOS-DE-LINEA-BASE.md). Campañas, referidos, puntos, sorteos y canjes pertenecen a sprints posteriores.

## Código que se presenta

- Código vigente: [backend](../../../backend/) y [frontend](../../../frontend/), dentro de este repositorio.
- [codigo_fuente_sprint_1.zip](codigo_fuente_sprint_1.zip): captura actualizada el 16 de noviembre de 2026 con los nombres y clases de servicio del modelo vigente.
- [manifiesto-codigo.json](manifiesto-codigo.json): huellas de la captura actual, cotejadas con los archivos vigentes.

La captura se verifico contra el codigo vigente del repositorio al cerrar esta revision. No incluye entornos virtuales, node_modules ni credenciales locales. Para instalación nueva seguir el [README del proyecto](../../../README.md); no ejecutar de nuevo los scripts iniciales sobre una base con datos.

## Evidencia y demostración

Consultar [verificación](verificacion-actual.md) y [operación de sesiones y HTTPS](operacion.md). La revisión del 15 de noviembre aprobó 135 pruebas backend y 20 frontend, además de lint y build. Esta limpieza documental no volvió a ejecutar esas pruebas ni cambió la aplicación.

Para demostrar: registrar cuenta general o socio según padrón; iniciar sesión; comprobar accesos por rol; cerrar sesión; verificar que la sesión anterior ya no sirve. Un administrador puede revisar y convertir una cuenta general mediante el proceso temporal autorizado.

La revisión visual 320–1920 px, WCAG completa, HTTPS del entorno definitivo y aceptación formal no se declaran terminadas. Jira se presenta directamente al docente; el [CSV de planificación](../backlog-jira/sprint_1_planificado.csv) conserva los estados originales.
