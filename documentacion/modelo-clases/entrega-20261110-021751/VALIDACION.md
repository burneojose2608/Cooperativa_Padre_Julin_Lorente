# Validación del modelo UML

| Comprobación | Resultado | Detalle |
|---|---|---|
| 75 clases nativas sin duplicados de identificador estable | Correcto |  |
| Todas las clases son UML Class editables | Correcto |  |
| Atributos y operaciones nativos coinciden con catálogo | Correcto |  |
| Diez enumeraciones UML nativas | Correcto |  |
| 103 asociaciones con extremos y multiplicidades válidos | Correcto |  |
| 44 dependencias de dominio separadas de asociaciones | Correcto |  |
| Vista_Logica identificada por jerarquía y GUID | Correcto |  |
| Todos los diagramas nuevos cuelgan de Vista_Logica | Correcto |  |
| Panorama con nombre requerido en Vista_Logica | Correcto |  |
| Elementos reutilizados sin duplicación dentro de vistas | Correcto | [] |
| Cajas de clases sin solapamientos geométricos | Correcto | [] |
| Compartimentos configurados visibles | Correcto | [] |
| Todas las clases se muestran en alguna vista | Correcto |  |
| Todas las relaciones tienen vista asignada | Correcto |  |
| Relaciones asignadas efectivamente visibles en EA | Correcto | [] |
| Reglas conservadas como restricciones UML nativas | Correcto |  |
| Repositorio reabierto en EA y 75 clases editables comprobadas | Correcto |  |
| Todos los PNG proceden de exportación EA y tienen contenido | Correcto |  |
| 14 familias RF y 91 referencias HU únicas | Correcto |  |
| Subtareas conservan padres originales | Correcto |  |
| Trazabilidad nativa de las 91 HU con GUID/ID reales | Correcto |  |
| Todas las operaciones tienen dueño, fuente y tipo de responsabilidad | Correcto |  |
| Firmas nativas completas con nombres, tipos, orden y retorno | Correcto | [] |
| Servicios de dominio sin atributos artificiales | Correcto |  |
| Tipos de análisis y enumeraciones coherentes | Correcto | [] |
| Conservación de datos anteriores t_object | Correcto | [] |
| Conservación de datos anteriores t_package | Correcto | [] |
| Conservación de datos anteriores t_diagram | Correcto | [] |
| Conservación de datos anteriores t_connector | Correcto | [] |
| Conservación de datos anteriores t_attribute | Correcto | [] |
| Conservación de datos anteriores t_operation | Correcto | [] |
| Escenarios originales conservados | Correcto |  |
| Objetos y conectores de diagramas originales conservados | Correcto |  |
| Original intacto y respaldo consistente identificado | Correcto |  |
| Reejecuciones reutilizan GUID de clases y conexiones | Correcto |  |

## Límites

- No se reejecutaron suites de aplicación ni se accedió a PostgreSQL.
- La correspondencia de análisis y el enlace UML no certifican aceptación de todos los criterios.
- La validación de lectura/edición se hace por API de EA; la captura interactiva posterior agotó la autorización. La revisión visual utiliza PNG exportados por EA.