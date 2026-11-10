> **Entrega posterior creada en EA:** consulte [ENTREGA-ACTUAL.md](ENTREGA-ACTUAL.md). El contenido siguiente se conserva como antecedente de preparación.

# Preparación del diagrama de clases de negocio

Revisión del 10 de noviembre de 2026. Este material prepara el trabajo de Codex CLI sobre Enterprise Architect. El archivo `.eapx` se consultó en modo de lectura; **no se creó ni modificó su diagrama de clases**.

## Entregables

- [Prompt completo para Codex CLI](PROMPT-CODEX-CLI.md): copiar su bloque de instrucciones en Codex CLI, ejecutado desde la raíz del repositorio.
- [Catálogo de clases y relaciones](CATALOGO-CLASES.md): propuesta de análisis con atributos, operaciones de negocio, multiplicidades y responsabilidades.
- [Trazabilidad de las 91 HU originales](TRAZABILIDAD.md): conserva los identificadores de las historias que ahora son subtareas y relaciona UR, RF, RNF, CU y operaciones propuestas.
- [Decisiones, reglas y asuntos pendientes](DECISIONES-Y-REGLAS.md): distingue evidencia, propuestas y discrepancias.
- [Fuentes extraídas de Enterprise Architect](inventario-ea.json): paquetes, diagramas, casos de uso y sus conectores, consultados mediante ADODB con `Mode=Read`.
- [Fuente PlantUML por módulos](diagramas/): especificaciones textuales de referencia. No son diagramas nativos de EA ni se ha verificado su renderizado visual.
- [Generador de la documentación](fuentes/generar_documentacion.py): permite reproducir catálogo, trazabilidad y fuentes PlantUML, leyendo el backlog local. No escribe en EA.

## Resultado de la revisión

El modelo actual tiene `Vista_Logica` con Package_ID 34, sin diagramas. El contexto está en el paquete `diagrama de contexto` y los casos de uso están bajo `Vista_Escenarios`. La ubicación mencionada en el prompt inicial no coincide con el archivo inspeccionado. Debe conservarse esta estructura y agregar el modelo de clases dentro de `Vista_Logica`.

El alcance completo contiene catorce familias RF y 91 HU originales. El backend revisado implementa principalmente identidad, registro, autenticación, sesiones, recuperación y conversión administrativa temporal. Los paneles restantes contienen datos demostrativos en `frontend/src/datos/demo.js`; los scripts SQL de esos módulos constituyen diseño de persistencia, no evidencia de funcionamiento completo.

Por ello se propone un **modelo de clases de análisis del dominio**, con un panorama general y detalles por módulo. Las operaciones expresan responsabilidades de negocio y no afirman que existan como métodos Python. No se pretende convertir cada archivo, actor, tabla o pantalla en una clase.

## Cómo usar el material

1. Leer las decisiones antes de aceptar las clases como línea base.
2. Ejecutar Codex CLI desde `Cooperativa_Padre_Julin_Lorente` y entregarle el prompt completo.
3. Revisar el resultado nativo de EA y la trazabilidad; una fuente PlantUML o una imagen por sí sola no satisface la creación del diagrama dentro del `.eapx`.

La correspondencia CU–HU es una propuesta semántica basada en los nombres y contenidos disponibles. Los códigos `CU-Gxx` proceden de los títulos de diagramas existentes; no se supone que estén guardados como Alias de cada caso de uso. Las decisiones pendientes deben quedar visibles en el modelo final.
