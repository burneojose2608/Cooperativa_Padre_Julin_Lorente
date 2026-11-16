# Entrega para revisión del proyecto Padre Julián Lorente

Fecha de revisión: 10 de noviembre de 2026. Se reunieron y completaron los formatos indicados en el mensaje del docente. **Los archivos locales están preparados. El usuario presentará el backlog de Jira directamente al profesor, por separado.** La existencia de documentación y diagramas no significa que todo el alcance del software esté implementado: la programación entregada corresponde al Sprint 1.

## Archivos principales solicitados

| Solicitud del docente | Archivo o ubicación | Resultado |
| --- | --- | --- |
| Requisitos de usuario en CSV | [requisitos_usuario.csv](requisitos_usuario.csv) | 57 UR, con fuente y vínculos RF/HU |
| Requisitos funcionales en CSV | [requisitos_funcionales.csv](requisitos_funcionales.csv) | 105 filas: 14 familias y 91 RF detallados, identificados por nivel |
| Requisitos no funcionales en CSV | [requisitos_no_funcionales.csv](requisitos_no_funcionales.csv) | 26 RNF, con relaciones RF y límites de verificación |
| Diagrama de contexto en PDF | [diagrama_contexto.pdf](diagrama_contexto.pdf) | Una página exportada desde EA; incluye aclaración del alcance de prueba |
| Diagrama de casos de uso en PDF | [diagrama_casos_uso.pdf](diagrama_casos_uso.pdf) | Panorama general y 25 diagramas de detalle, 26 páginas |
| Diagrama de clases en PDF | [diagrama_clases.pdf](diagrama_clases.pdf) | Panorama y detalles, 31 páginas; 75 clases de análisis reutilizadas |
| Plantilla Excel original | [plantilla-original/Presentacion .(1) (1).xlsx](<plantilla-original/Presentacion .(1) (1).xlsx>) | Copia íntegra, comprobada con SHA-256 |
| Fuente de Enterprise Architect | [fuente-enterprise/Modelo-negocio-Padre-Julian-Lorente.eapx](fuente-enterprise/Modelo-negocio-Padre-Julian-Lorente.eapx) | Modelo nativo con contexto, casos de uso y clases; no es el original antiguo sin clases |
| Backlog en Jira | Presentación directa del usuario al profesor; [respaldo local](backlog-jira/LEEME-JIRA.md) | Evidencia externa al paquete, según indicación del usuario |
| Sprint 1 desarrollado | [sprint-1](sprint-1/LEEME-SPRINT-1.md) | Fuente ZIP, documentación, planificación y pruebas ejecutadas |

Los CSV usan coma como separador, UTF-8 con BOM y comillas para textos con comas o saltos de línea. Los identificadores se conservan. La columna `descripcion` expresa la línea vigente; `descripcion_original` conserva la redacción de la plantilla cuando se documentó un cambio. No se alteró el Excel original ni el backlog histórico.

Los PDF mantienen páginas amplias adaptadas al diagrama. Abrir a tamaño real o ampliar para leer los detalles; los marcadores permiten ir a cada vista. La exportación gráfica procede del mismo modelo EA incluido. No se exige imprimir cada vista en A4.

## Comprobaciones y documentos de apoyo

- [Informe de cumplimiento](INFORME-CUMPLIMIENTO.md): qué estaba disponible, qué se completó y qué falta acreditar.
- [Cambios de línea base](CAMBIOS-DE-LINEA-BASE.md): cédula, registro general y validación administrativa temporal.
- [Trazabilidad principal](trazabilidad/TRAZABILIDAD-VERIFICADA.csv): 91 HU con UR/RF/RNF, CU reales, clase, operación y GUID de enlaces EA.
- [Trazabilidad de calidad](trazabilidad/RNF-RF.csv): los 26 RNF relacionados con los RF declarados en la plantilla.
- [Validación estructurada](trazabilidad/VALIDACION-ENTREGA.json): recuentos, referencias y límites.
- [Verificación del Sprint 1](sprint-1/verificacion-actual.md): 135 pruebas backend, 20 frontend, build y lint.
- `MANIFIESTO.csv`: archivos finales y SHA-256 para comprobar integridad. Los intermedios visuales de `soporte/qa` no forman parte del paquete final comprimido.

Se conservaron el repositorio EA anterior, la entrega del modelo de clases y los archivos originales. La copia del EA incluido se leyó con ACE, se compararon recuentos con la instancia abierta y se verificó que su SHA-256 coincidía con la fuente estable durante la captura.

## Presentación al profesor

El usuario mostrará directamente en Jira el backlog y el Sprint 1. No se requiere incorporar su enlace ni acreditar esa presentación dentro de esta carpeta. El CSV de planificación se conserva como respaldo histórico; sus estados no se modificaron.

Para la revisión académica, mostrar los resultados del Sprint 1 y explicar las decisiones que sustituyeron criterios históricos. La aprobación formal del docente y las mediciones de RNF futuros no se dan por realizadas.
