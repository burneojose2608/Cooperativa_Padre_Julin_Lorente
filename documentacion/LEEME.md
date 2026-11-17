# Documentación para la revisión del ingeniero

Organizada el 15 de noviembre de 2026 según la lista del docente: requisitos en CSV, diagramas en PDF, plantilla original, fuente de Enterprise Architect, backlog y Sprint 1 desarrollado.

Para leer todo lo importante en un solo archivo: [RESUMEN-PROYECTO.md](RESUMEN-PROYECTO.md).

El [Sprint 2 desarrollado](entregable/sprint-2/LEEME-SPRINT-2.md) contiene la guía de ejecución,
la trazabilidad de sus 17 ítems y la verificación de sus criterios.

## Originales conservados

- Anexo 01 - Acta de Constitución Proyecto1.docx.
- Anexo 02 - Documento Vision Proyecto1.docx.
- Modelo-negocio-Padre-Julian-Lorente.eapx: fuente editable de contexto, casos de uso, clases y actividades.
- Presentacion.xlsx: plantilla original de requisitos.
- product_con_subtareas.csv: backlog original completo, sin cambiar sus estados.
- PROYECTO.docx.

Los documentos originales, el Excel y el backlog se conservaron sin alterar su contenido.
El fuente EA se actualiza por petición del usuario para mantener los diagramas y su trazabilidad.
El Excel y el fuente EA se usan directamente desde esta raíz; los respaldos quedan fuera del repositorio.

## Qué abrir para presentar

En [entregable/LEEME.md](entregable/LEEME.md) está la correspondencia entre cada solicitud y su archivo. Esa carpeta contiene los CSV de requisitos, los PDF de contexto, casos de uso, clases y actividades, la trazabilidad y las evidencias del Sprint 1. El backlog se presenta también directamente desde Jira; el CSV es su respaldo local.

El código vigente se encuentra en [backend](../backend/) y [frontend](../frontend/). La carpeta de entrega conserva una sola copia ZIP del código presentado el 10 de noviembre, identificada como una captura de esa fecha.

## Depuración realizada

Se retiraron de esta carpeta las copias completas anidadas de la entrega, los ZIP duplicados, las exportaciones XML/JSON e imágenes intermedias, los scripts de generación del modelo y los informes históricos repetidos. Los documentos útiles de Sprint 1 se consolidaron en [entregable/sprint-1](entregable/sprint-1/LEEME-SPRINT-1.md).

Antes de retirar archivos se generó y verificó un respaldo íntegro fuera del repositorio, en `../respaldos-documentacion/` respecto de la raíz del proyecto. Ese respaldo permite recuperar cualquier auxiliar sin mantenerlo mezclado con lo que se presenta al docente.

Después de que el usuario guardó y cerró Enterprise Architect se retiró también la carpeta antigua del modelo. Su copia guardada se preservó en el respaldo externo sin sustituir el Enterprise original de esta raíz, ya que sus bytes difieren tras ese último guardado. Con el resumen único añadido, la documentación consolidada consta de 30 archivos.

El Enterprise y el PDF de casos de uso se actualizaron después de la depuración, por solicitud del usuario, en la revisión de negocio finalizada el 16 de noviembre. Los otros cinco originales protegidos mantienen su contenido. Véase [el resumen de la revisión](RESUMEN-PROYECTO.md#casos-de-uso-orientados-al-negocio).
## Diagrama de clases completo

El modelo contiene un solo diagrama de clases para todos los modulos (ID 58). El PDF es una pagina panoramica ampliable. La correspondencia exacta de clases, miembros y codigo se consulta en [CLASES-CODIGO.csv](entregable/trazabilidad/CLASES-CODIGO.csv); el estado planificado se distingue del implementado.

## Diagrama de actividades general

El recorrido de registro, referidos y recompensas se encuentra en Enterprise Architect, en Vista_Actividades, diagrama DA-01. Se basa en objetivos de CU-00 y utiliza cinco carriles por responsabilidad. La nube y la integración institucional se representan como diseño propuesto. Se puede revisar el [PDF de actividades](entregable/diagrama_actividades.pdf) y su [trazabilidad hacia los casos generales](entregable/trazabilidad/ACTIVIDADES-GENERALES.csv).
