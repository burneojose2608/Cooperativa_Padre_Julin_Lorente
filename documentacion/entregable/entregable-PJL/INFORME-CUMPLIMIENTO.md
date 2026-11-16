# Revisión de los entregables solicitados

La lista recibida exige seis formatos principales y cuatro evidencias adicionales. Antes de organizar esta carpeta, el proyecto contenía la plantilla Excel, backlog CSV, documentación y código del Sprint 1, contexto y casos de uso en EA y una entrega posterior con clases nativas. Los requisitos estaban mezclados en el Excel; no existían los tres CSV separados ni los tres PDF solicitados. Estos seis formatos se generaron a partir de fuentes existentes y se reunieron con sus evidencias.

## Resultado por obligación

| Entregable | Antes de esta revisión | Acción y evidencia | Estado final local |
| --- | --- | --- | --- |
| UR en CSV | Estaban en hoja UserReq. | Extracción de 57 UR, sin perder IDs, nombres, descripción y actores; vínculos con RF/HU | Preparado |
| RF en CSV | Estaban en hoja Req. Funcionales | Extracción de 91 RF detallados y 14 familias; padre y nivel explícitos; estado del alcance separado de su modelado | Preparado |
| RNF en CSV | Estaban en hoja Req. No Funcionales | Extracción de 26 RNF, prioridad, RF asociados y evidencia/brecha; matriz RNF-RF normalizada | Preparado |
| Contexto PDF | Había diagrama nativo | Exportación por API de EA, aclaración del padrón simulado del MVP | Preparado |
| Casos de uso PDF | Había panorama y detalles en EA | Exportación de CU-00 y CU-G01 a CU-G25; se excluyó el diagrama genérico de plantilla Starter Use Case Model | Preparado |
| Clases PDF | Había 75 clases nativas y 31 vistas en la entrega posterior | Reexportación actual del panorama y detalles; clases, atributos, operaciones y multiplicidades pertenecen al modelo editable | Preparado |
| Excel original | Archivo disponible | Copia byte por byte con huella coincidente | Incluido con incidencias heredadas identificadas |
| Fuente EA con los tres diagramas | El archivo original antiguo no tenía clases; la copia posterior sí | Se incluyó la copia posterior, con los tres tipos de vistas y trazabilidad nativa | Incluido y contrastado |
| Backlog en Jira | CSV local disponible | El usuario indicó que lo presentará directamente al profesor; se conserva el respaldo local | Presentación externa al paquete por cuenta del usuario |
| Sprint 1 desarrollado | Código y evidencia previa disponibles | Se reunieron fuentes y documentación; se reejecutaron backend/frontend, lint y build | Código y pruebas incluidos; aceptación completa no certificada |

## Trazabilidad comprobada

Se contrastaron las tablas del modelo EA vigente mediante consultas de lectura y se compararon las referencias de la matriz posterior. Se verificaron los GUID de la clase, HU, RF y caso de uso de cada fila; la existencia de la operación asignada sobre su clase; y los extremos y GUID de los conectores declarados. Las 91 referencias HU se encuentran sin duplicar y tienen correspondencia con los 91 RF detallados.

Las 57 UR tienen asociación con RF/HU en la matriz. Los 26 RNF tienen asociación RF según la plantilla. RNF-05, RNF-08, RNF-15 y RNF-19 no están citados directamente en las HU: su alcance es transversal y se conserva mediante RNF-RF.csv. No se inventaron HU para resolver esta diferencia. Los RNF se documentan en los CSV y la matriz; no se afirma que todos tengan elementos Requirement independientes en el repositorio EA.

Esta comprobación valida referencias y correspondencia documental. No certifica que cada operación de análisis exista como un método Python, que cada criterio de aceptación esté implementado o que los RNF hayan sido medidos.

La copia del fuente EA conserva 75 clases, 281 atributos, 153 operaciones de análisis y diez enumeraciones en su modelo nativo. El catálogo y la matriz distinguen estados implementados/parciales/planificados. Los actores de administración no se convierten en subclases de Usuario y las mismas clases se reutilizan entre diagramas.

## Diferencias que se corrigieron documentalmente

Se añadió la línea vigente del registro en los CSV, sin borrar el texto histórico: cédula de diez dígitos sin verificador; cuenta general para cédula ausente del padrón; socio habilitado para padrón activo; rechazo para inactivo y bloqueo del alta ante indisponibilidad del padrón. La validación administrativa manual y temporal se documenta como decisión posterior, distinta de la conversión comercial HU-018 y sin atribuirle puntos por referido.

Los cambios constan en CAMBIOS-DE-LINEA-BASE.md y en los documentos originales de decisiones del Sprint 1. El Excel y el CSV del backlog quedan intactos para que el docente pueda comparar la línea base y los cambios.

## Brechas de calidad y evidencia externa

- Jira: por indicación del usuario, el backlog se mostrará directamente al profesor. Se excluye la comprobación remota del alcance de este paquete; no se requiere su enlace y no constituye un pendiente documental de la carpeta.
- Excel: contiene cinco nombres definidos con referencia `#REF!`: Atributos, Clasificacion, Estado, Matrizreq y Moscow. Son defectos preexistentes de nombres de plantilla; los textos de UR/RF/RNF se pudieron extraer. Se conserva el original solicitado sin ocultar ni reparar silenciosamente esos nombres.
- RNF-03 y RNF-07: las pruebas DOM no certifican todos los navegadores, geometría 320–1920 px ni WCAG AA completa.
- RNF-04, RNF-05 y RNF-08: no hay mediciones suficientes de tiempo de respuesta bajo carga, concurrencia de 500 usuarios o disponibilidad de seis meses.
- RNF-15: no se acreditó tarea diaria de respaldo con siete días de retención y restauración probada. Los respaldos del modelo EA no sustituyen esta obligación operativa.
- RNF-19: las suites aprobadas no demuestran por sí solas el 70 % de cobertura de lógica de referidos, gamificación y canjes; esos módulos futuros no se presentan como desarrollados.
- Los módulos RF-03 a RF-14 se modelan como alcance planificado; tablas o pantallas demo no equivalen a funcionalidad completa.

Estas brechas se informan para la revisión del avance. La tarea de esta entrega no amplía el Sprint 1 a la programación de todos los sprints futuros ni fabrica pruebas de operación de meses.

## Pruebas ejecutadas en esta revisión

135 pruebas backend aprobadas con PostgreSQL aislado; 20 pruebas frontend aprobadas; lint con salida 0 y 14 advertencias anteriores; build correcto de 58 módulos. Los comandos, tiempos y límites están en sprint-1/verificacion-actual.md y resultados-pruebas.json. No se reejecutó la prueba HTTPS histórica; se conserva su evidencia previa con esa aclaración.

## Conclusión de cumplimiento

**El paquete contiene los archivos solicitados para la revisión:** los seis formatos principales, la plantilla original, el fuente EA y el código y evidencia del Sprint 1. El usuario presentará Jira directamente al profesor, por separado, por lo que no se requiere verificar ni adjuntar ese enlace aquí. Se mantienen las limitaciones técnicas y de aceptación identificadas; la preparación documental no certifica el cumplimiento completo de todos los requisitos del software.
