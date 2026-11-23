# Plan transversal de la plataforma

Los [14 planes de módulo](../README.md) detallan sus recorridos, puntos de entrada y dependencias. Este plan coordina las transiciones entre módulos y la aceptación de los requisitos de calidad. La numeración T-001 a T-045 corresponde al Sprint 0 original.

## Secuencia de integración

1. Usuarios y Autenticación establecen identidad, padrón de prueba, consentimiento, sesión y permisos.
2. Campañas y Referidos establecen elegibilidad, consentimiento de prospectos y conversión comercial. Notificaciones procesa la confirmación fuera de la solicitud HTTP.
3. Gamificación recibe actividades validadas de Referidos, Formación y Juegos. Sorteos y Retos consumen actividades elegibles. Recompensas consume saldo y vigencia de Bienestar.
4. Contenidos y Comunidad aplican publicación autorizada, descarga privada y moderación. Reportes agrega datos autorizados y los exporta con fecha y filtros.

## Aceptación

Ejecutar los [recorridos de la visión](spec.md#recorridos-de-aceptación-entre-módulos) con datos sintéticos, PostgreSQL aislado y roles reales de la aplicación. Capturar resultados nominales, rechazos, transiciones y efectos persistidos. Para los recorridos monetarios de puntos, registrar saldo y stock antes y después, además del resultado de reintentar la misma acción.

Registrar por criterio el resultado, el caso ejecutado, el entorno y el enlace a la evidencia. Usar la [matriz HU–RF–UR–CU](../trazabilidad.csv) para los requisitos funcionales y las [tareas transversales](tasks.md#verificación-transversal-de-rnf) para los RNF. Versionar las decisiones que cambien el alcance en la [línea base](../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md).

La [evidencia registrada](../../documentacion/VERIFICACION-EVOLUCION.md) sirve para seleccionar regresiones. La aceptación visual, la carga, la disponibilidad y la operación de canales externos tienen verificaciones propias.
