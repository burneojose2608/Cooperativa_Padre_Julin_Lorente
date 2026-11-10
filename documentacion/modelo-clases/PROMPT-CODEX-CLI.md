# Prompt completo para Codex CLI

Copia las siguientes instrucciones completas. El catálogo adjunto es una propuesta verificable que debes contrastar con el repositorio y con el modelo existente.

```text
Trabaja sobre el proyecto:
C:\Users\Lenovo\Documents\proyectoPJL\Cooperativa_Padre_Julin_Lorente

El repositorio de Enterprise Architect es:
C:\Users\Lenovo\Documents\proyectoPJL\Cooperativa_Padre_Julin_Lorente\documentacion\ProyeectoPadreJulianLorente.eapx

OBJETIVO
Analiza el alcance del proyecto y crea dentro del package existente Vista_Logica un modelo UML de clases de análisis, en español, que permita comprender el negocio de la plataforma de referidos y gamificación. Incluye clases relevantes, atributos del dominio, operaciones de negocio, relaciones justificadas, multiplicidades, restricciones y trazabilidad. El modelo debe servir como fundamento del diseño del software.

CONTEXTO YA INSPECCIONADO
En la revisión del 10/11/2026, Vista_Logica (Package_ID 34) estaba vacío; el contexto estaba en el paquete diagrama de contexto y los casos de uso bajo Vista_Escenarios. Verifica de nuevo la estructura actual: estos IDs son referencias de la revisión, no constantes para programar. Conserva los diagramas y elementos existentes. Lee documentacion/modelo-clases/README.md, CATALOGO-CLASES.md, TRAZABILIDAD.md y DECISIONES-Y-REGLAS.md. No trates la propuesta como un requisito aprobado ni importes mecánicamente sus clases.

FUENTES Y ANÁLISIS
1. Busca y cumple los AGENTS.md aplicables. Revisa README, documentación del sprint, decisiones posteriores, backend, frontend, SQL 01–06 y pruebas relevantes. No leas ni publiques secretos de .env ni credenciales.
2. Lee los DOCX del Acta, Visión y especificación general; revisa product_con_subtareas.csv y, si aporta requisitos, Presentacion .(1) (1).xlsx. Inspecciona el .eapx mediante la API de EA o acceso de lectura compatible para conocer paquetes, GUID, notas, escenarios, casos de uso y relaciones. No basta con mirar capturas.
3. Confronta alcance documentado, comportamiento implementado, scripts de persistencia y pantallas de demostración. Clasifica cada módulo y elemento: implementado, implementado parcialmente, planificado o propuesta de análisis. La existencia de una tabla SQL o de una pantalla no prueba que el módulo esté implementado.
4. Usa las decisiones explícitas posteriores documentadas para interpretar cambios respecto al backlog. Conserva las referencias originales y registra las diferencias. Si una regla no tiene respaldo, anótala como pendiente o hipótesis; no inventes políticas, fórmulas, actores ni integraciones institucionales.

NIVEL DEL MODELO Y NOMENCLATURA
5. Modela conceptos del dominio y sus responsabilidades. Una clase no equivale automáticamente a una tabla, un archivo, un actor o una pantalla. Incluye clases asociativas, objetos de valor, enumeraciones o servicios de dominio solamente cuando ayuden a explicar una responsabilidad real. No agregues controladores, vistas React, serializadores, repositorios, DTO, endpoints ni clases base del framework al diagrama principal de negocio.
6. Utiliza nombres de clases y atributos en español; usa nombres legibles y consistentes. Representa cada clase con nombre, atributos y operaciones, como en la referencia enviada por el usuario. Tipos de análisis: Texto, Entero, Decimal, Booleano, Fecha, FechaHora, enumeraciones y referencias a conceptos del dominio. Marca atributos derivados con / y opcionales con [0..1]. No muestres claves foráneas si la asociación ya explica la relación.
7. Los métodos son operaciones de negocio: por ejemplo, calcularTasaConversion(), verificarElegibilidad(), confirmarConversion(), calcularSaldoDisponible(), reservarPuntos(), aprobarCanje(), registrarAsistencia() o calcularAvance(). Son responsabilidades conceptuales, aunque el código actual las ejecute en servicios. Incluye parámetros y retorno que expliquen su sentido. No llenes las clases con getters, setters, constructores, __str__, CRUD genérico ni operaciones técnicas de persistencia.
8. No fuerces métodos artificiales en registros inmutables u objetos de valor. Explica su invariante y asigna el comportamiento a su dueño o a un servicio de dominio cuando corresponda. Distingue operación de consulta, cambio de estado y coordinación entre conceptos. Ninguna clase debe concentrar todo el negocio.
9. No conviertas Administrador, Marketing, Responsabilidad Social y Gestor de contenidos en subclases de Usuario solo por ser actores. El proyecto admite varios roles por usuario. Considera Usuario con 0..1 Socio y una asociación a Rol, justificando el enfoque y separando condición de socio de autorización.

COHERENCIA DE NEGOCIO
10. Diferencia Usuario, Socio, Prospecto y Referido. Diferencia codigo_socio de CódigoReferido; no hay evidencia para afirmar que sean el mismo identificador. Distingue conversión comercial de un referido y conversión administrativa temporal de una cuenta general a socio.
11. Representa el consentimiento de la cuenta y el del prospecto, con finalidad, aceptación, fecha y versión; no vincules obligatoriamente el prospecto a una cuenta existente. Mantén la unicidad de cuentas, el padrón de prueba y los cambios documentados: cédula de diez dígitos sin verificador, cuenta general para ausente, socio para activo, rechazo para inactivo o indisponibilidad del padrón. La validación administrativa es manual y temporal, sin autoconversión.
12. Explica el ciclo del referido, evidencia de conversión, historial con responsable/fecha/motivo y acreditación única. Modela campaña, segmentación, incentivos y sus condiciones vigentes sin alterar incentivos ya reconocidos.
13. Modela puntos con movimientos inmutables, origen, idempotencia, límites por período y reversos compensatorios. Distingue saldo contable, reservado y disponible. La reserva seguida de aprobación no debe descontar dos veces. Si no está definida la base de nivel, clasificación, reversos o límites, registra la decisión pendiente en vez de inventar una política.
14. Cubre también niveles, insignias, clasificaciones, capacitaciones, módulos, materiales, evaluaciones, intentos, certificados, talleres y asistencia; sorteos, elegibles congelados, evidencia, premios, ganadores y suplentes; beneficios y canjes; contenido institucional, comunidad y moderación; juegos y retos; convenios de bienestar; notificaciones y reportes. No incorpores cuentas financieras reales, préstamos operativos, historiales clínicos ni integración productiva con el core bancario.

RELACIONES UML
15. Cada asociación debe expresar su significado y multiplicidad en ambos extremos. Identifica roles cuando aclaren la lectura. No uses herencia por conveniencia ni composición solo porque hay una FK. Justifica la composición por pertenencia exclusiva y ciclo de vida. Conserva registros de auditoría, conversiones y movimientos aunque cambie el estado de sus objetos relacionados. Separa las dependencias de servicios y reportes de las asociaciones persistentes.
16. Revisa que ninguna clase o relación quede sin justificación y que cada operación tenga dueño coherente. Para servicios sin estado, no inventes atributos solo para llenar el compartimento.

TRAZABILIDAD
17. Genera una matriz con UR, RF, HU original, historia consolidada o padre cuando corresponda, CU existente, clase, atributo/regla relevante, operación, fuente concreta y estado de cobertura. Mantén las 91 HU originales como referencias; varias son ahora subtareas y no deben duplicarse como trabajo independiente.
18. Para cada vínculo al modelo existente identifica el elemento real por GUID/ID y nombre. Los CU-Gxx de la documentación corresponden a títulos de diagramas: verifica qué elemento UseCase los representa. La correspondencia semántica propuesta no demuestra que un enlace UML ya exista.
19. En EA reutiliza elementos de requisitos o CU existentes; si faltan elementos de requisitos, créalos dentro de una ubicación identificada bajo Vista_Logica con IDs originales y fuente. Utiliza conexiones UML de trazabilidad/dependencia adecuadas y notas o tagged values para detalles. No uses asociaciones de negocio para enlazar requisitos. No inventes GUID. Conserva la diferencia entre trazabilidad propuesta y enlace efectivamente creado/verificado.

CREACIÓN SEGURA EN ENTERPRISE ARCHITECT
20. Trabaja con una copia de respaldo fechada del .eapx y conserva el original anterior. Detecta si EA tiene el repositorio abierto: el .ldb por sí solo no prueba un bloqueo activo. No fuerces acceso exclusivo ni elimines el .ldb. Usa la Automation Interface de Enterprise Architect u otro mecanismo de importación soportado. No escribas directamente en las tablas internas de Access/EA.
21. Identifica Vista_Logica por nombre, jerarquía y GUID; crea subpackages por dominio solo cuando mejoren la navegación. El diagrama principal se llamará Diagrama de clases de negocio. Agrega diagramas de detalle por módulo para que todas las clases, atributos y operaciones sean legibles sin saturar el panorama general. Reutiliza las mismas clases en las vistas; no dupliques elementos.
22. Las clases deben ser elementos UML editables y sus atributos, operaciones y conectores deben ser nativos. No insertes una imagen como sustituto del modelo ni declares que un .puml es un diagrama de EA. Emplea una distribución clara, compartimentos visibles y conectores sin cruces innecesarios; configura saltos de línea y tamaño apropiado.
23. Haz la actualización repetible: busca elementos existentes por GUID o identificador estable, reutilízalos y actualízalos sin borrar trabajo ajeno ni duplicar clases/diagramas al ejecutar otra vez. Guarda un registro de elementos creados/actualizados.
24. Si el entorno no puede editar EA, completa el análisis, catálogo, relaciones y trazabilidad, y entrega un archivo de intercambio realmente compatible con EA si puedes producirlo y validarlo. Identifica claramente la limitación. No afirmes haber modificado el .eapx si no ocurrió ni fabriques un XMI sin verificar su importación. No modifiques código ni base de datos de la aplicación para hacer encajar el modelo.

ENTREGABLES Y VALIDACIÓN
25. Entrega el .eapx actualizado cuando sea técnicamente posible, respaldo identificado, exportaciones legibles de diagramas, catálogo de clases y responsabilidades, relaciones con multiplicidades, reglas, matriz de trazabilidad y decisiones pendientes. Conserva todo bajo documentacion/modelo-clases con nombres claros, sin sobrescribir evidencia previa innecesariamente.
26. Valida: cobertura de las 14 familias RF y las 91 referencias HU; ausencia de clases duplicadas; relaciones con extremos válidos y multiplicidades; operaciones con responsabilidad y fuente; tipos y enumeraciones coherentes; ninguna regla propuesta presentada como implementada. Describe brechas sin afirmar cobertura completa de aceptación por el solo hecho de mapear una HU.
27. Abre o vuelve a leer el repositorio resultante mediante EA, confirma que los diagramas cuelgan de Vista_Logica, que las clases son editables y que muestran atributos/operaciones. Exporta e inspecciona visualmente todos los diagramas para comprobar legibilidad. Verifica que contexto y casos de uso originales se conservan. Informa qué comprobaciones realizaste y cuáles no pudieron ejecutarse.
28. Al terminar, resume el modelo, diferencias resueltas, decisiones pendientes, cantidad de clases/relaciones, archivos entregados y evidencia de trazabilidad. No presentes una propuesta textual como si el trabajo dentro de Enterprise Architect estuviera terminado.

Realiza el trabajo completo autorizado. Decide autónomamente detalles rutinarios de organización. Consulta al usuario únicamente si una ambigüedad de negocio impide avanzar con sentido; mientras tanto, progresa en los módulos independientes y deja trazabilidad de las hipótesis.
```
