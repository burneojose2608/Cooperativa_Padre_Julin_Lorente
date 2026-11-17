# Verificación del Sprint 2

Revisión local del 17/11/2026. Se continuó desde los cambios guardados en documentación y diagramas. En ese estado no había código nuevo del Sprint 2. Se conservaron esos cambios y se implementaron los 11 Stories y 6 Sub-tasks marcados como Sprint 2 en el backlog original.

| Comprobación | Resultado |
|---|---|
| Backend PostgreSQL aislado | **163 pruebas aprobadas**, incluidas las 135 existentes |
| Frontend Vitest / Testing Library | **29 pruebas aprobadas** |
| Construcción del frontend | `npm run build` correcto |
| Análisis del frontend | `npm run lint` sin errores; conserva 14 avisos de Fast Refresh en los paneles y copias de demostración anteriores. Los archivos nuevos no introducen esos avisos |
| API por HTTP real | **53 comprobaciones correctas**, usando JWT y cinco cuentas sintéticas en una base aislada |
| Rutas de frontend | 6 rutas servidas correctamente, además de la construcción completa |
| Cola asíncrona por comando real | 4 entregas procesadas en la base sintética; sin SMTP externo |
| Alcance y aceptación | 17 ítems y **58 criterios** vinculados con RF, UR, RNF, CU, código, pantallas y pruebas |
| Modelo de clases | **22 contratos** cotejados con nombres, atributos, propiedades, métodos y orden de parámetros del código |
| Modelo completo | 103 tipos y 91 cadenas generales; GUID de elementos preservados |
| Contexto, casos de uso y actividades | Vistas y relaciones gráficas conservadas; catálogo de actividades actualizado para reflejar CodigoReferido implementado |
| Exportación de clases | Una página panorámica desde Enterprise Architect, renderizada y revisada en vista general y detalles |
| Base existente | Respaldo completo previo fuera del repositorio. Actualización aditiva aplicada, conservando las 3 cuentas y los 2 socios existentes |
| Documentos protegidos | Anexo 01, Anexo 02, Presentacion.xlsx, product_con_subtareas.csv y PROYECTO.docx conservados |

Las pruebas verifican pertenencia del perfil y notificaciones, denegación por rol, cambios de permisos sin renovar sesión, política y hash de contraseña, revocación de sesiones, rechazo de adjuntos falsificados y de más de 10 MB, código de referido único incluso con solicitudes simultáneas, vigencia de contenidos, reutilización de materiales, conservación de acreditaciones al configurar reglas y coordinación de trabajadores con reservas e idempotencia.

La revisión de concurrencia del Sprint 1 distingue ahora la auditoría de registro de la nueva auditoría de generación de código de referido. Se comprueba un registro exitoso y una sola generación de código para el socio; para la cuenta general no se genera código.

La revisión HTTP utilizó cuentas creadas exclusivamente para una base `test_sprint2_revision_20261117`. Sus credenciales y datos sintéticos no se incorporan a la entrega ni a las cuentas reales. Los resultados detallados y el respaldo previo están en `respaldos-documentacion/sprint2-20261117`, fuera del repositorio.

## Límites de la verificación

La herramienta de control del navegador detuvo la revisión visual interactiva porque no pudo determinar con certeza la URL de Chrome. Se detuvieron las acciones de interfaz. La navegación visual de las pantallas queda para corroboración del usuario; se completaron las pruebas de componentes, construcción y peticiones HTTP. El PDF y su imagen nativa sí se revisaron visualmente como archivos.

La compartición móvil se verifica mediante llamadas a Web Share y su alternativa de copiado en pruebas de componentes. No se certifica una prueba física en todos los dispositivos. No se certifica entrega a un servidor SMTP real; el transporte está probado con sustitutos de prueba y la cola con consola local.

HU-011 mantiene la excepción autorizada: código y enlace en la consola del backend, sin correo. Se mantienen hash, caducidad, un solo uso y respuesta genérica. Esta excepción sustituye el criterio de entrega por correo del backlog original durante la práctica.

Las funciones posteriores de campañas, registro y conversión comercial de referidos, acreditación de puntos, capacitaciones, sorteos y canjes conservan su diseño y trazabilidad futura. Este resultado certifica el alcance programado del Sprint 2 dentro de las verificaciones indicadas. Los estados del backlog en Jira requieren la corroboración del equipo.

Los cambios permanecen locales, sin commit ni push.
