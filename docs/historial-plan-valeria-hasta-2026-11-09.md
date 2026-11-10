# Implementación de Valeria Chuncho en Sprint 1

Fecha: 8 de noviembre de 2026. Responsable funcional: Valeria Chuncho.

Ampliación autorizada del 9 de noviembre: se implementó [validación administrativa temporal](../documentacion/sprint-1-valeria/conversion-administrativa-temporal.md) para convertir una cuenta general existente a Socio, con confirmación manual, autorización en servidor, auditoría y transacción. No requiere nuevos cambios de esquema. La suite actual completa suma **99 pruebas aprobadas**. Se preparó un administrador temporal en la base local; la cuenta diego2026 permanece pendiente de aprobación humana en la interfaz.

Última actualización del 9 de noviembre: por instrucción explícita del usuario se elimina provincia/verificador y se exige únicamente texto con diez dígitos ASCII. Se corrigió el 503 aplicando esquema 05/06 a la base local original, sin modificar ni borrar las cuentas existentes ni cargar padrón sintético en ella. La suite final alcanza **83 pruebas aprobadas**. Esta [decisión vigente y su evidencia](../documentacion/sprint-1-valeria/decision-cedula-diez-digitos.md) reemplaza los puntos anteriores de verificador y base sin cambios de esquema; las entradas de cierres previos se conservan como historial.

Actualización vigente del 9 de noviembre de 2026: el usuario autorizó registrar como usuario general a quien tenga cédula válida ausente del padrón. Solo el socio activo obtiene el rol Socio; el inactivo conserva el bloqueo. La nueva [decisión funcional y evidencia de 80 pruebas](../documentacion/sprint-1-valeria/decision-registro-general.md) reemplaza la regla original que rechazaba también al ausente. El encargo y los resultados originales permanecen como historial.

## Objetivo y límites

Entregar HU-006 (106, RF-01-6) y HU-008 (108, RF-01-8), subtareas de HU-001 (101), conservando Django REST Framework, PostgreSQL y React. T-007 aporta únicamente validación y errores de este flujo; T-004 aporta clases y secuencia del registro. No se incluyen funcionalidades de otros sprints ni publicación, commits o despliegue.

Fuentes: `documentacion/product_con_subtareas.csv`, plan adjunto del usuario, Acta, Visión y documento PROYECTO de `documentacion/`. El CSV local reemplaza la ruta de otro equipo indicada en el plan. T-004, T-007, T-011 y T-012 figuran como tareas transversales de Sprint 0; esta entrega cubre únicamente sus dependencias del registro.

## Inventario y estado inicial

| Elemento | Estado inicial | Evidencia |
| --- | --- | --- |
| Registro por capas y transacción | Implementado, pendiente verificar | `services/registro_service.py`, repositorios y API |
| Padrón independiente y elegibilidad | Pendiente | No hay tabla, modelo ni repositorio de padrón |
| Fecha de validación | Parcial | `socio.validado_en` existe pero no se escribe |
| Unicidad | Parcial | Cédula UNIQUE e índices lower(correo), lower(username); falta controlar carreras y espacios en escritura directa |
| Dígito verificador | Contradictorio | SQL 01 contiene algoritmo, SQL 04 lo relaja; validador y test_cedula aceptan diez dígitos, test_servicios y test_api exigen verificador |
| Consentimiento | Parcial | React lo solicita; backend registra sin comprobar aceptación |
| Hash | Pendiente | Configuración por defecto PBKDF2; Argon2 no está instalado inicialmente |
| Errores seguros | Parcial | Errores de negocio controlados, fallos no previstos delegados a DRF |

Cambios previos del usuario conservados: README, backend/.env.example, backend/.gitignore y SQL 01–04. `documentacion/` ya estaba sin seguimiento. No se leen ni muestran secretos. `manage.py check` inicial: sin incidencias. Pruebas iniciales sobre base temporal: 17 ejecutadas y una fallida (`test_cedula_invalida`, el registro aceptaba verificador inválido).

## Criterios de aceptación

- HU-006 y cambio posterior: solo cédulas activas del padrón sintético obtienen rol Socio; ausente crea cuenta general y el inactivo conserva el error genérico; ante fallo del padrón se rechaza toda creación; no se crean filas parciales ni se acepta estado/rol/validado_en del cliente.
- HU-008: cédula, correo y username únicos, con espacios exteriores normalizados y correo/username sin distinción de mayúsculas; comprobación previa y garantía SQL; carreras con conexiones independientes producen una sola cuenta y un duplicado controlado.
- Dependencias HU-001: verificador válido, consentimiento explícito, hash Argon2id; preservar ceros iniciales de la cédula.
- Entrega: pruebas reales PostgreSQL, regresiones, lint/build cuando cambie React, diagramas, matriz y aplicación/reversión SQL reproducibles.

## Cambios previstos y trazabilidad

| Archivos | Motivo |
| --- | --- |
| Nuevo modelo/contrato/repositorio de padrón | HU-006; mínimo T-011 |
| SQL 05 y reversión separada; carga sintética explícita | HU-006/HU-008; mínimos T-011/T-012 |
| Servicio de registro, repositorio de socio y excepciones | HU-006/HU-008: elegibilidad, validado_en, rollback y colisiones conocidas |
| Serializador, configuración de hash, requirements, validador de cédula | Dependencias necesarias HU-001 y T-007 |
| Manejador de errores | T-007: respuesta segura sin detalles internos |
| Validación React y mensaje de cédula | Integración HU-001, autoridad del servidor |
| Pruebas y runner de base aislada | Evidencia de HU-006/HU-008 y regresión |
| docs y documentacion | Trazabilidad y diagramas T-004 de este alcance |

## Contratos y decisiones

El contrato vigente `Padron.consultar_estado(cedula) -> EstadoPadron` usa texto y devuelve ACTIVO, INACTIVO o NO_ENCONTRADO, sin datos personales. Sustituye el booleano inicial porque hay que distinguir ausencia e inactividad. El adaptador PostgreSQL consulta una tabla de prueba independiente; se inyecta en el caso de uso con un valor predeterminado local. Los fallos de acceso o estados desconocidos no se interpretan como ausencia ni elegibilidad. No existe endpoint público del padrón.

Cédula: texto ASCII de diez dígitos, trim exterior, provincia 01–24 o 30, tercer dígito menor que 6 y módulo 10, consistente con la función SQL existente. Correo/username: trim exterior y lowercase para almacenamiento y consulta. Espacios interiores de username se rechazan. La base compara `lower(btrim(...))` para impedir evasión por escritura directa. No se fusionan ni borran cuentas existentes.

Se mantiene el contrato HTTP: éxito 201 y campos existentes; para cuenta general, codigo_socio=null y roles=[]; duplicado 409 `dato_duplicado` con campo; formato/verificador/consentimiento 400; inactivo 403 `socio_no_elegible` con mensaje genérico; infraestructura 503 `servicio_no_disponible`; fallo inesperado 500 genérico. La igualdad original entre inexistente e inactivo queda reemplazada por la decisión posterior. Ninguna respuesta incluye SQL, rutas ni trazas.

El consentimiento debe ser booleano JSON `true`, tanto en API como en servicio; no se infiere de la existencia del formulario. Se usa Argon2id para nuevas claves y se conserva PBKDF2 como lector de hashes históricos. Estas decisiones siguen el CSV; no se encontró una instrucción posterior del usuario que autorice omitir el verificador.

Transacción del servicio: consultar el padrón antes de crear usuario, consentimiento y auditoría de éxito, dentro de `atomic`; únicamente ACTIVO añade socio con fecha y rol Socio. Capturar `IntegrityError` fuera de `atomic`, después del rollback; solo SQLSTATE 23505 y nombres de unicidad de identificadores conocidos se convierten en 409. Otros fallos no se disfrazan como duplicados. Auditoría de rechazo sin PII ni credenciales.

Evolución: modelos `managed=False`; SQL 01–04 se conservan y SQL 05 aplica cambios incrementales transaccionales. Reversión fuera del directorio que el runner ejecuta automáticamente. Prevalidar conflictos y abortar sin modificar datos. No ejecutar SQL sobre `cooperativa_db` durante esta entrega.

## Dependencias y riesgos

T-011 y T-012 corresponden a Jefferson Paredes; no existen entregables de padrón en el repositorio. Se prepara únicamente tabla, adaptación y datos sintéticos requeridos por estas subtareas. HU-001 mantiene su responsabilidad principal compartida con Evelyn Riofrio según CSV. El padrón sintético no verifica existencia institucional de una persona.

Reactivar el verificador puede detectar cédulas históricas inválidas; el script debe abortar y dejar su resolución al responsable de BD. Nuevos índices pueden detectar duplicados por espacios; tampoco se corrigen automáticamente. Cambiar el hash requiere instalar argon2-cffi. La base de trabajo permanece sin cambios hasta revisión del usuario.

## Fases

| Fase | Estado |
| --- | --- |
| 1 Inventario y trazabilidad | Completada |
| 2 Decisiones y contratos | Completada |
| 3 Persistencia y datos sintéticos | Completada en PostgreSQL aislado |
| 4 HU-006 | Completada con pruebas de elegibilidad y rechazos |
| 5 HU-008 | Completada con tres carreras PostgreSQL independientes |
| 6 Integración y seguridad | Completada mediante HTTP automatizado, regresiones y build |
| 7 Verificación y entrega | Completada; límites de verificación descritos abajo |

## Evidencia final

La tabla siguiente corresponde al cierre original. Después del cambio funcional del 9 de noviembre, la suite completa pasó a **80 pruebas aprobadas (20.073 s)**, incluyendo alta/login/perfil de usuario general, ausencia de privilegios, rollback y carrera de una cuenta general. Build correcto; lint conserva 14 advertencias ajenas al cambio; cuatro comprobaciones de rutas aprobadas. No hay cambios adicionales de esquema. El detalle actualizado está en la decisión funcional enlazada al inicio.

Fecha de cierre técnico local: 8 de noviembre de 2026, zona America/Guayaquil.

| Comprobación ejecutada | Resultado |
| --- | --- |
| `manage.py check` | Sin incidencias |
| Persistencia, comprobación previa por fase | 3 pruebas aprobadas en PostgreSQL real |
| Elegibilidad e integración inicial por fase | 11 pruebas aprobadas; posteriormente ampliadas |
| Concurrencia por cédula, correo y username | 3 carreras aprobadas; dos PID PostgreSQL distintos por carrera, un 201 y un 409, una sola cuenta completa |
| Suite final `manage.py test --noinput` | **74 pruebas aprobadas**, 12.642 s; base temporal creada y eliminada por el runner |
| Aplicación y reversión SQL | Aprobadas dentro de la suite; reaplicación y aborto sin pérdida ante verificador inválido o duplicados normalizados |
| Hash | Argon2id comprobado; login con hash PBKDF2 histórico y actualización a Argon2id aprobados |
| `npm.cmd run lint` | Salida 0; 14 advertencias Fast Refresh en paneles sin modificar, incluidas copias bajo frontend/frontend |
| `npm.cmd run build` | Correcto, 53 módulos transformados |
| Validación JS mediante Node/assert | 10 casos correctos: válidos, inválidos, ceros iniciales, salto de línea y tipos incorrectos |
| `python -m pip check` | Sin dependencias rotas |
| `git diff --check` | Sin errores de espacios; aviso de Git sobre futura conversión de fin de línea del README previo |

HU-006 entrega padrón sintético independiente, puerto sustituible, fallo cerrado y validado_en generado después de comprobar actividad. Con la regla posterior, el ausente obtiene cuenta general y el inactivo conserva rechazo genérico. HU-008 entrega normalización, consultas previas, índices únicos y captura selectiva de colisiones fuera de atomic para ambas clases de cuenta. Los rechazos y fallos intermedios no dejan usuario, socio, rol ni consentimiento parciales; la auditoría de rechazo permitida no contiene identificadores personales ni claves.

El SQL incremental es `backend/sql/05_registro_padron_unicidad.sql`; la reversión manual está en `backend/sql/reversiones/05_registro_padron_unicidad.sql`. La carga explícita es `manage.py cargar_padron_sintetico`, limitada a bases test_* o sprint1_*. SQL 01–04 permanecen intactos respecto al estado inicial del usuario. No se ejecutó el cambio de esquema ni la carga en cooperativa_db.

Documentación de entrega:

- [Índice de revisión](../documentacion/sprint-1-valeria/README.md).
- [Arquitectura, contratos y diagramas Mermaid](../documentacion/sprint-1-valeria/arquitectura-y-contrato.md).
- [Entorno, datos, aplicación/reversión y matriz requisito → implementación → prueba](../documentacion/sprint-1-valeria/operacion-y-verificacion.md).
- [Encargo original](encargo-valeria-sprint-1.txt).

No verificado: interacción manual en navegador, renderizado gráfico de Mermaid, correo SMTP real, despliegue e integraciones institucionales. Estas comprobaciones no se presentan como realizadas. El flujo HTTP de registro/login/perfil/refresh sí se verificó automáticamente y React compiló.

Pendientes ajenos al cierre de estas dos subtareas: revisión e integración general T-011/T-012 por Jefferson Paredes; secuencias de otros módulos de T-004; avisos de paneles ajenos al registro; aprobación funcional del usuario antes de aplicar SQL a una base con datos. No se cierra toda HU-001 ni las tareas transversales del equipo. No hay bloqueos técnicos conocidos para las dos subtareas verificadas.

Cambios locales listos para corroboración. Sin commits, push, publicaciones ni modificaciones de secretos o datos de la base de trabajo.
