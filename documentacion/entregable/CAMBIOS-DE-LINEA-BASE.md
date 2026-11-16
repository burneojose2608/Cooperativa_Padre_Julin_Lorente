# Cambios documentados de la línea base de requisitos

Se conserva intacta la plantilla original del grupo. Los CSV exportados distinguen la descripción vigente de la descripción original para evitar que la revisión automática confunda decisiones posteriores con incumplimientos silenciosos. Estos cambios proceden de instrucciones posteriores documentadas del usuario; no se afirma que el docente los haya aprobado formalmente.

| Referencia local | Fuente del cambio | Requisitos afectados | Regla vigente |
| --- | --- | --- | --- |
| DEC-CEDULA-10-DIGITOS | sprint-1/documentacion-registro/decision-cedula-diez-digitos.md | UR-01, RF-01-1, HU-001 y validación de entrada | Exactamente diez dígitos ASCII, conservados como texto. Sin cálculo de provincia ni verificador. |
| DEC-REGISTRO-GENERAL | sprint-1/documentacion-registro/decision-registro-general.md y actualizaciones posteriores | UR-01, RF-01-1, RF-01-6, HU-001/HU-006 | Padrón activo crea socio; ausente permite cuenta general sin roles; inactivo rechaza; fallo del padrón impide el alta. |
| DEC-VALIDACION-TEMPORAL | sprint-1/documentacion-registro/conversion-administrativa-temporal.md | Ampliación posterior de validación de cuentas; sin inventar HU/RF | Administrador revisa y confirma socio activo de forma manual y temporal; no autoconversión ni reactivación de padrón inactivo. |

La conversión comercial de referido sigue siendo HU-018/RF-03-3, basada en apertura de cuenta o producto crediticio validado con datos de prueba. **No equivale a habilitar como socio una cuenta general.** Tampoco se confunde `codigo_socio` con `CodigoReferido`.

Los estados del backlog original no se editaron. La columna `To Do` del archivo de planificación no demuestra que el código esté pendiente, y las pruebas locales aprobadas no demuestran que alguien haya actualizado la tarea en Jira. La conciliación de ambas evidencias está en backlog-jira/conciliacion_sprint_1.csv.

El contexto conserva un sistema institucional como referencia conceptual externa. Durante el MVP su interacción se limita al padrón local de prueba; no se declara conexión a producción. La aclaración figura también en el PDF de contexto.
