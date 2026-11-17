# Resumen del proyecto y del Sprint 1

Actualizado el 16 de noviembre de 2026. Este archivo reúne lo esencial para entender el avance, explicar decisiones y preparar la presentación al ingeniero. Las evidencias detalladas permanecen en la carpeta entregable.

## Qué se está construyendo

Una plataforma para la Cooperativa Padre Julián Lorente. El modelo contempla usuarios y perfiles, referidos, capacitaciones y recompensas, entre otros módulos. La programación actual de Sprint 1 establece la base de registro, autenticación, permisos y sesiones; los módulos de sprints posteriores siguen planificados aunque aparezcan en los diagramas o en menús de la aplicación.

## Qué está desarrollado en Sprint 1

| Historia o subtarea | Resultado |
| --- | --- |
| HU-001 | Registro con campos obligatorios, consentimiento y contraseña protegida. |
| HU-006 | Consulta de padrón de prueba antes de habilitar funciones de socio. |
| HU-008 | Prevención de duplicados de cédula, correo y usuario, también ante solicitudes simultáneas. |
| HU-009 | Inicio de sesión por usuario o correo, navegación por rol y bloqueo tras cinco fallos durante quince minutos. |
| HU-010 | Verificación de credenciales y cuenta activa, errores genéricos y auditoría de intentos con IP. |
| HU-012 | Consulta de roles vigentes y unión de accesos para cuentas con varios roles. |
| HU-015 | Cierre de sesión invalidado en servidor y caducidad tras quince minutos de inactividad. |

Son dos historias principales, HU-001 y HU-009, con cinco subtareas asociadas. La programación del alcance vigente está implementada; el cierre formal requiere corroborar los límites de aceptación indicados más adelante.

## Reglas que conviene recordar

- **Cédula:** texto de exactamente diez dígitos del 0 al 9, conservando ceros iniciales. Por solicitud del usuario no se verifica provincia ni dígito final. Esta comprobación valida el formato; no demuestra identidad.
- **Padrón activo:** permite crear una cuenta con rol Socio.
- **Cédula ausente del padrón:** permite crear una cuenta general, sin otorgar funciones de socio.
- **Padrón inactivo:** se rechaza el registro. Si falla la consulta al padrón, no se completa el alta.
- **Cuenta general → Socio:** un administrador activo debe revisar y confirmar expresamente la condición de socio en Administración → Validar socios. La operación conserva usuario y contraseña y deja auditoría.
- **Temporalidad:** esa conversión puede deshabilitarse con `CONVERSION_SOCIOS_TEMPORAL_HABILITADA=False` y reinicio del backend. Las reglas institucionales definitivas siguen pendientes de definición.
- **Referidos:** convertir una cuenta general en socio no equivale a validar una conversión comercial de referido ni concede puntos.

Estas decisiones modifican parte del CSV histórico. Se explican en [cambios de línea base](entregable/CAMBIOS-DE-LINEA-BASE.md); no se supone aprobación formal del docente.

## Aspectos técnicos destacables

Se mantiene un monolito modular: React en la interfaz, Django REST Framework en el backend y PostgreSQL como base de datos. Las vistas y serializadores reciben las solicitudes; los servicios aplican reglas y transacciones; los repositorios acceden a los datos.

Las contraseñas nuevas usan Argon2id con sal individual y se rechazan claves comunes. La unicidad se garantiza también mediante restricciones de PostgreSQL, evitando depender únicamente de una validación previa del formulario.

Los tokens access y refresh comparten un identificador de sesión firmado y comprobado en la base. Cerrar sesión revoca esa familia: borrar el almacenamiento del navegador no es la única protección. El servidor también controla la inactividad. Un token antiguo sin sesión verificable exige volver a iniciar sesión.

Los permisos se consultan contra los roles actuales en la base; ocultar un botón no sustituye la autorización del servidor. Existen las áreas Administrador, Marketing, Responsabilidad Social, Contenidos y Socio. Tener acceso a un área no significa que sus funcionalidades futuras estén desarrolladas.

## Pruebas y límites reales

La última ejecución observada, del 15 de noviembre, aprobó **135 pruebas backend y 20 de interfaz**. La compilación fue correcta y lint terminó sin errores, con 14 advertencias anteriores de Fast Refresh. El backend probó sobre una base aislada test_*, sin recrear la base de trabajo.

Hay evidencia de HTTPS local del 10 de noviembre, con validación de cadena y nombre del certificado. No equivale a un despliegue ni a confianza instalada en Windows. La [verificación detallada](entregable/sprint-1/verificacion-actual.md) distingue esa comprobación histórica de las suites posteriores.

Quedan sin acreditar la revisión visual de 320–1920 px, WCAG completa, HTTPS del entorno definitivo y aceptación formal. Tampoco se presentan como comprobadas las mediciones de carga, disponibilidad de meses, SMTP real o integración institucional. Las pruebas aprobadas no demuestran por sí solas cumplimiento de todos los RNF del proyecto.

## Qué llevar a la revisión del ingeniero

Los tres CSV de requisitos y los tres PDF de contexto, casos de uso y clases se encuentran en [entregable](entregable/LEEME.md). Los CSV conservan 57 requisitos de usuario, 91 requisitos funcionales detallados más 14 familias y 26 requisitos no funcionales.

En la raíz de documentacion se mantienen intactos los anexos 01 y 02, `Presentacion.xlsx`, `Modelo-negocio-Padre-Julian-Lorente.eapx`, `product_con_subtareas.csv` y `PROYECTO.docx`. El backlog se muestra directamente en Jira; sus estados no se modificaron al preparar esta documentación.

El [código vigente](../README.md) está en backend y frontend. El ZIP conservado en entregable/sprint-1 es una captura del 10 de noviembre y no reemplaza al repositorio actual. Para relacionar requisitos, implementación y pruebas, usar la [matriz del Sprint 1](entregable/sprint-1/matriz-trazabilidad.md).

Una demostración útil sigue este orden: registrar una cuenta general o socio según padrón, iniciar sesión, comprobar permisos por rol, revisar una conversión administrativa si corresponde y cerrar sesión verificando que la anterior ya no sirve.

## Organización y precauciones de trabajo

La documentación se consolidó para conservar una sola entrega. Los auxiliares y duplicados se trasladaron a `proyectoPJL/respaldos-documentacion`, fuera del repositorio; antes se verificó un ZIP completo. La copia antigua que estaba abierta en Enterprise Architect también quedó preservada allí después de cerrarla. Su último guardado difiere en bytes del original de la raíz, por lo que se conservó aparte sin sustituir el archivo protegido.

No volver a ejecutar los scripts iniciales SQL sobre una base con datos. No incluir credenciales, tokens ni archivos .env en la entrega. Esta consolidación documental no cambió el funcionamiento de la aplicación ni hizo commits, push o despliegues.

## Casos de uso orientados al negocio

Revisión del 15 de noviembre de 2026 solicitada por el usuario. Las validaciones de credenciales, estado, rol, duplicados, permisos, auditoría y guardado se documentan dentro de las reglas y escenarios de los objetivos del actor. Se reclasificaron 37 óvalos internos como requisitos ReglaInterna, conservando sus GUID y enlaces originales. No se eliminaron las reglas del software ni las historias del backlog.

Iniciar sesión mantiene las comprobaciones de credenciales, estado y roles en su especificación. La vista muestra iniciar sesión, recuperar acceso y cerrar sesión. El actor Persona usuaria reúne las operaciones comunes; Socio, Administrador, Marketing, Responsabilidad Social y Contenidos mantienen sus roles específicos y su correspondencia con las entidades del contexto.

Las relaciones include y extend usan ahora sus subtipos UML nativos y dirección explícita: include va del caso base al comportamiento obligatorio incluido; extend va del comportamiento opcional o condicionado al caso base. Se conservaron dos inclusiones y trece extensiones justificadas, con condiciones en las descripciones. Por indicación del usuario se retiró la presentación de extension points y sus notas de las vistas. Las relaciones que solo describían navegación, pasos internos o momentos distintos se retiraron de la vista y quedaron como correspondencias históricas. Un diagrama de casos de uso no representa una secuencia de ejecución.

Ejemplos: registrar un referido incluye obtener consentimiento; resolver un canje incluye evaluar la solicitud. Aprobar o rechazar el canje son variantes condicionadas de su resolución. La consulta posterior de un resultado no se presenta como extensión automática de una inscripción anterior.

La habilitación temporal de cuenta general como Socio tiene un objetivo propio, ligado a la decisión posterior y a la clase ValidacionAdministrativaSocio. Se distingue de confirmar la conversión comercial del referido, módulo futuro que exige evidencia comercial y contempla efectos de puntos.

Se comprobaron 91 cadenas de historias a requisitos, clases y casos de negocio. La matriz conserva además el ID, GUID y enlace de las reglas que antes aparecían como casos técnicos. El contexto y las clases conservan sus identidades; no se modificó código, Excel original, anexos, Proyecto.docx ni backlog. El PDF de casos de uso se regenera desde las vistas del mismo Enterprise Architect.

La revisión finalizada el 16 de noviembre también separa responsabilidades que la matriz anterior había asociado a consultas generales: configurar incentivos, corregir puntos, recibir reconocimientos, gestionar y recibir avisos, revisar contenido para publicación y administrar convenios. Son objetivos ya exigidos por los RF e historias existentes, no ampliaciones de programación. Los actores de cada objetivo se contrastan con el texto de la historia: por ejemplo, configurar puntuación corresponde al administrador, y consultar reportes se limita al perfil indicado. Personal autorizado expresa una responsabilidad con permiso específico, no un sexto rol implementado.

Referencia de notación: [UML 2.5.1, sección 18](https://www.omg.org/spec/UML/2.5.1/PDF). Evidencias nativas y copia anterior del modelo permanecen en el respaldo externo de la revisión; no se agregan carpetas auxiliares a documentacion.

## Formato del diagrama general

El 16 de noviembre se ajustó CU-00 al formato solicitado por el usuario: un único rectángulo representa la Plataforma de Referidos y Gamificación (MVP), con los 36 objetivos generales dentro y los ocho actores fuera. La vista muestra únicamente 39 asociaciones de participación. Las inclusiones, extensiones y condiciones se mantienen en los diagramas y especificaciones de detalle.

El personal interno de la cooperativa —Administrador, Marketing, Responsabilidad Social, Gestor de contenidos y Personal autorizado— se sitúa a la izquierda. Los actores externos —Persona usuaria, Socio y sistema institucional— se sitúan a la derecha. Todos quedan fuera del rectángulo y ninguno se coloca arriba ni abajo del sistema. El sistema institucional sigue siendo una referencia conceptual: el MVP utiliza el padrón local de prueba. Las operaciones comunes se agrupan bajo Persona usuaria y los participantes complementarios se documentan en el detalle.

Se reutilizó el límite original del modelo y se conservaron los identificadores, objetivos y asociaciones principales. Se recuperó además la participación del sistema institucional en los tres objetivos generales de referidos. Solo cambió la vista CU-00 y la primera página del PDF; las otras 25 páginas, los diagramas de detalle, los requisitos, la trazabilidad y el programa se conservaron.


## Navegacion y detalle de todos los casos generales

Revision del 16/11/2026: los 36 objetivos del general disponen de un diagrama especifico y un enlace compuesto nativo verificado; doble clic en el ovalo abre su detalle. Se crearon CU-G26 a CU-G36 para 11 objetivos antes compartidos en vistas de modulo: registro, recuperacion, cierre de sesion, habilitacion temporal como socio, incentivos, correccion de puntos, plantillas, historial de avisos, revision editorial, convenios y publicacion de recompensas de convenio. Se reutilizaron los mismos elementos y GUID.

El [indice de casos](entregable/trazabilidad/INDICE-CASOS-USO.csv) relaciona cada objetivo con su diagrama, actores, HU, RF y clases. Las 91 cadenas HU/RF/clases y todos los conectores originales se verificaron sin alteraciones; solo se actualiza el identificador del detalle correspondiente en la matriz. La habilitacion temporal conserva su decision y clase ValidacionAdministrativaSocio, sin inventar un RF. Las vistas anteriores, contexto y clases se conservan. El PDF contiene el general y 36 detalles (37 paginas). No se modifico codigo ni se certificaron nuevos modulos como implementados.

## Diagrama de clases unico y correspondencia con codigo

Revision del 16/11/2026: por indicacion del usuario se conserva un solo diagrama de clases completo, ID 58, con 103 tipos UML y 180 relaciones visibles, organizado en 16 areas. Incluye identidad, seguridad, auditoria, referidos, campanas, puntos, formacion, sorteos, recompensas, contenidos, avisos, juegos, comunidad, bienestar, reportes, tipos y servicios. Se retiraron las vistas parciales de clases, conservando todos los elementos y sus GUID. Los casos de uso y sus enlaces compuestos siguen intactos.

Las relaciones tienen verbos, multiplicidades y extremos UML revisados: asociaciones estructurales, navegabilidad de referencias ORM, composicion en el propietario exclusivo, agregacion de material reutilizable, herencia hacia AbstractBaseUser y dependencia hacia la clase utilizada. PadronRepository realiza estructuralmente el protocolo Padron. UsuarioRol representa las asignaciones de roles; no existe herencia Socio/Administrador/Marketing sobre Usuario.

Se normalizaron tambien los miembros planificados a snake_case y los tipos a str, int, bool, date, datetime y colecciones Python. Se cotejaron 28 tipos propios con el AST del codigo y dos operaciones utilizadas del framework AbstractBaseUser. Los modelos usan exactamente Usuario, Socio, Rol, UsuarioRol, Consentimiento, PadronPrueba, Sesion, TokenRecuperacion y Auditoria. Ocho servicios antes escritos como funciones ahora son clases sin estado, con sus llamadas, pruebas e imports actualizados: ServicioRegistro, ControlAcceso, ServicioAutorizacion, ValidacionAdministrativaSocio, ServicioSesiones, ServicioRecuperacion, ServicioUsuariosInternos y ServicioSocios. Se tiparon firmas sin cambiar las reglas, tablas ni columnas, y el registro se denomina registrar_cuenta porque permite cuentas generales y de socio.

Los miembros implementados conservan sus nombres Python exactos y su visibilidad real. Las clases futuras llevan Planificado. ServicioGestionCuentas conserva las responsabilidades futuras de actualizar contacto, cambiar clave autenticada, cambiar estado y administrar roles, sin inventar implementacion en Usuario. El atributo foto es explicita y exclusivamente planificado. No se crearon stubs para aparentar que los modulos futuros estan programados.

La matriz conserva las 91 cadenas HU/RF/CU/clase y registra los enlaces previos cuando cambia la clase responsable. El [indice de clases y codigo](entregable/trazabilidad/CLASES-CODIGO.csv) y el [catalogo de relaciones](entregable/trazabilidad/RELACIONES-VERIFICADAS.csv) permiten comprobar los nombres y la semantica. Los CSV originales de requisitos y backlog y los cinco documentos originales protegidos se conservan sin cambios. El modelo EA se actualiza por autorizacion del usuario.

Validacion final del backend: 135 pruebas aprobadas en 25.533 s, en base aislada test_*, comprobacion Django sin incidencias. La base cooperativa_db no se recreo. Frontend, responsive, WCAG completa, HTTPS definitivo y aceptacion formal conservan sus limites anteriores. El archivo de codigo de la entrega se regenera con la fuente vigente y huellas verificadas, sin entornos ni credenciales. No se hizo commit ni push.

Referencia de automatizacion consultada: [documentacion oficial de Sparx para diagramas](https://www.sparxsystems.com/enterprise_architect_user_guide/17.2/add-ins___scripting/diagram2.html).

## Legibilidad de las relaciones del diagrama completo

Revision visual del 16/11/2026. Se redistribuyeron las 103 clases, interfaces y enumeraciones de la vista unica y los recorridos de sus 180 relaciones. Cada conexion usa anclajes separados y se acortaron los tramos con desvios innecesarios. Las relaciones de la misma area usan gris oscuro y las conexiones entre areas usan azul grisaceo. El conjunto mantiene cruces entre areas que comparten Usuario, Socio y servicios.

Se verifico que elementos, atributos, operaciones, conectores, multiplicidades, extremos UML y enlaces de trazabilidad conservan sus registros originales. Las otras vistas del modelo y el codigo se conservan. El PDF de clases se exporto nuevamente desde Enterprise Architect en una sola pagina ampliable. El respaldo previo queda fuera del repositorio.

## Revision de nombres y retiro de query

Revision del 16/11/2026. Se retiro la indicacion {query} de las 57 operaciones que la mostraban en Enterprise Architect. Los nombres de las operaciones, sus parametros y retornos se verificaron contra el catalogo y el codigo. La vista completa contiene 103 tipos UML y 180 relaciones visibles, con 181 relaciones en el catalogo al incluir la referencia historica.

La verificacion cubre 28 tipos propios implementados y dos operaciones heredadas de Django, 46 campos declarados y 51 metodos propios cotejados mediante AST, ademas de las propiedades derivadas. Se verificaron las firmas del modelo, los catalogos de clases y relaciones, los 36 casos generales con detalle y las 91 cadenas HU/RF/CU/clase mediante sus identificadores y GUID. Los tipos futuros estan identificados como Planificado.

Se corrigieron cuatro referencias del CSV de requisitos funcionales. EntradaPadron corresponde ahora a PadronPrueba y RecuperacionAcceso a TokenRecuperacion. Las columnas historicas de trazabilidad documentan los nombres anteriores. Las notas vigentes del modelo y los documentos originales revisados no contienen esos nombres anteriores.

El proceso central del contexto usa el mismo nombre del limite del sistema del diagrama general, Plataforma de Referidos y Gamificación (MVP). Los seis participantes del contexto coinciden nominalmente con sus actores en los casos de uso. Tambien se corrigio el flujo Certificados digitales. Los PDF de clases y contexto se exportaron nuevamente desde las vistas nativas y se revisaron visualmente.

## Presentación uniforme del diagrama de clases

Revisión del 17/11/2026. Por indicación del usuario se retiró de la vista de clases la presentación de estereotipos personalizados y la distinción de colores por estado de implementación. Las 103 clases, interfaces y enumeraciones utilizan el mismo fondo claro y borde negro. Las conexiones se presentan en negro. También se retiró de esta vista la leyenda que explicaba los colores anteriores. Esta presentación sustituye la convención visual registrada en las revisiones del 16/11.

El diagrama muestra los nombres, atributos, métodos, relaciones y multiplicidades. El catálogo CLASES-CODIGO.csv documenta el estado implementado o planificado y la fuente del código. Se verificaron las 91 cadenas de trazabilidad y la correspondencia de nombres y firmas con el código implementado. La revisión modifica la presentación de la vista 58 y su PDF.

## Diagrama de actividades general desde CU-00

Revisión del 17/11/2026. Se creó DA-01, diagrama nativo de actividades ID 107, dentro de Vista_Actividades. El alcance elegido por el usuario es el recorrido general desde la creación de cuenta hasta los referidos y las recompensas. El origen son 13 objetivos presentes en CU-00, ID 6. La trazabilidad registra 31 enlaces nativos hacia esos objetivos, con sus requisitos, clases y fuentes del código.

El diagrama usa cinco carriles de responsabilidad, 19 acciones, diez decisiones con salidas Sí/No, cinco fusiones de caminos alternativos, un inicio y seis finales de actividad. Las ramas contemplan registro no completado, cuenta general pendiente de habilitación como socio, acceso denegado, consulta del estado del referido, decisión de canjear y aprobación o rechazo del canje. El rechazo libera la reserva; la aprobación confirma el descuento y conduce a la entrega registrada.

La habilitación administrativa temporal de una cuenta como socio y la confirmación comercial de un referido tienen actividades propias y fuentes diferenciadas. La primera corresponde a ValidacionAdministrativaSocio en el código vigente. La confirmación comercial, la acreditación de puntos, la reserva, resolución y entrega del canje corresponden al diseño futuro de Referido, Conversion, ActividadValidada, CuentaPuntos, MovimientoPuntos, Canje y Beneficio. Las acciones automáticas de negocio se vinculan con sus objetivos generales y RF de origen.

La plataforma en la nube y la integración con el sistema institucional se representan como diseño propuesto. El MVP usa PadronPrueba local. Se presupone personal autorizado autenticado, reglas de puntuación configuradas y beneficios vigentes. La matriz ACTIVIDADES-GENERALES.csv documenta esta distinción de alcance.

Se verificaron todos los identificadores, GUID y enlaces a CU-00, los nombres de clases y requisitos, las guardas de decisión, la llegada de todas las ramas a un final y la ausencia de líneas superpuestas o que atraviesen las actividades. Los registros de los diagramas anteriores y sus elementos coinciden con el respaldo previo. El PDF se generó desde la imagen nativa y se revisó visualmente.

La notación utiliza [acciones y flujos de control de actividades de UML](https://www.sparxsystems.com/enterprise_architect_user_guide/17.2/guide_books/specifying_action_sequence_with_control_flows.html) y [carriles de responsabilidad de Enterprise Architect](https://sparxsystems.com/enterprise_architect_user_guide/17.2/modeling_fundamentals/swimlanes.html).

## Sprint 2 desarrollado y trazado

Revisión del 17/11/2026. Se implementaron los 11 Stories y 6 Sub-tasks con **Sprint planificado = Sprint 2**, incluyendo HU-064 consolidada. La [guía del Sprint 2](entregable/sprint-2/LEEME-SPRINT-2.md) contiene los pasos para iniciar backend, frontend y trabajador, las pantallas disponibles por rol y los límites de esta entrega.

El perfil permite consultar identidad y editar contacto y foto privada. El cambio de contraseña exige la actual, aplica la política vigente y revoca sesiones. Administración permite crear personal, buscar y filtrar cuentas, editar contacto, registrar cambios de estado con motivo y responsable, y asignar/revocar roles y permisos. Cada cambio se audita; las restricciones se verifican nuevamente en cada petición. Se protege al último administrador activo. La validación manual temporal de socios sigue vigente.

El socio validado obtiene un **CodigoReferido** persistente, aleatorio y único, diferente de codigo_socio. Se genera al validar al socio y se completa para los socios existentes al actualizar. Puede consultarse desde el perfil, copiarse y compartirse; su enlace abre una invitación sin revelar información personal. Registrar personas referidas y confirmar conversiones comerciales permanece en sus historias posteriores.

Las reglas de puntos tienen versiones por actividad, límite, período y vigencia; las nuevas condiciones conservan las acreditaciones anteriores. Gestor de contenidos prepara borradores, edita, publica, programa o retira noticias, anuncios y multimedia. La visibilidad se comprueba con la fecha de Ecuador en el servidor. El texto se muestra codificado por React. Gestor y Responsabilidad Social administran una biblioteca privada de materiales de hasta 10 MB, reutilizables en módulos de capacitación.

Las notificaciones tienen bandeja propia, estado de lectura y preferencias por evento/canal. La operación principal registra eventos en PostgreSQL. Un trabajador independiente distribuye publicaciones y entrega los avisos de plataforma/correo, con reserva de trabajo y hasta tres reintentos adicionales. Los eventos de módulos posteriores se conectan cuando se implementen. Para ver avisos automáticos debe ejecutarse `procesar_notificaciones --continuo`.

**Recuperación por consola:** por instrucción expresa del usuario, HU-011 / RF-02-3 muestra el código temporal y enlace en la terminal de Django y nunca utiliza SMTP. El código conserva caducidad de 30 minutos, hash SHA-256, un solo uso y respuesta HTTP genérica. La pantalla admite introducirlo manualmente. El backlog original por correo permanece intacto; esta decisión temporal se registra en CAMBIOS-DE-LINEA-BASE y en la aceptación del Sprint 2.

La actualización aditiva `07_sprint_2.sql` ya se aplicó localmente sobre un respaldo completo y conserva las 3 cuentas y los 2 socios existentes. El comando es repetible y no restaura permisos revocados. Los archivos privados se guardan fuera del frontend y se descargan únicamente con autorización. Las pantallas activas consultan datos persistidos; los módulos futuros se identifican como pendientes.

Se aprobaron **163 pruebas de backend y 29 de frontend**, más 53 comprobaciones HTTP con los cinco roles y seis rutas frontend en un entorno sintético. La construcción y el análisis del frontend terminan sin errores; quedan avisos anteriores de Fast Refresh en archivos de demostración. La revisión visual interactiva del navegador quedó pendiente porque la herramienta no pudo verificar la URL de Chrome y detuvo las acciones.

Las matrices del Sprint 2 trazan sus **17 ítems y 58 criterios**. Se cotejaron 22 contratos del código con el modelo único de 103 tipos y se conservaron las 91 cadenas generales. Se corrigieron el orden de parámetros, tamaños y anclajes de las cajas afectadas; se revisó el PDF exportado. La relación de plantilla ahora genera Notificacion, como indica su FK; los envíos referencian esa notificación. Un material puede existir sin publicación institucional. Los estados de diseño futuro permanecen explícitos en el catálogo, manteniendo la presentación UML uniforme y los GUID. Contexto, casos de uso generales y específicos y el diagrama de actividades conservan su estructura. Obtener código de referido pasa a estar implementado en la matriz de actividades; el registro de referidos, puntos y canjes sigue planificado.

La [verificación completa](entregable/sprint-2/VERIFICACION.md) registra pruebas, evidencias y límites. Los documentos originales protegidos se conservan y los cambios quedan locales para corroboración.
