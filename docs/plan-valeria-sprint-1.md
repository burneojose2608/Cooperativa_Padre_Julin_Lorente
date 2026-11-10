# Plan y cierre de Valeria Chuncho para Sprint 1

Revisión posterior: el [plan del Sprint 1 completo](plan-sprint-1-equipo.md) y su entrega implementan también los pendientes de autenticación que este cierre parcial dejaba en otros responsables. Este documento conserva la trazabilidad de la fase anterior.

Actualizado el 10 de noviembre de 2026, zona America/Guayaquil. Responsable según CSV: vale0401g@gmail.com.

## Objetivo y alcance

Completar HU-006 / 106 / RF-01-6 y HU-008 / 108 / RF-01-8, subtareas de HU-001, con el apoyo de T-004 y T-007 correspondiente al flujo de usuarios de Sprint 1. Se conservan Django REST Framework, PostgreSQL, React y la arquitectura por capas existente.

La conversión administrativa temporal se incluye como ampliación expresamente autorizada por el usuario. No se implementan las asignaciones de Valeria de otros sprints ni las subtareas de autenticación de otros responsables.

## Fuentes y evolución de las reglas

- Línea base: documentacion/product_con_subtareas.csv, filas 101, 106, 108, 304 y 307; dependencias 311 y 312.
- [Encargo original conservado](encargo-valeria-sprint-1.txt).
- [Historial del plan anterior](historial-plan-valeria-hasta-2026-11-09.md), con resultados de las revisiones 74, 80, 83 y 99 pruebas. Se conserva como historial, no como política vigente.
- [Cuenta general si no consta en padrón](../documentacion/sprint-1-valeria/decision-registro-general.md), decisión posterior del usuario.
- [Diez dígitos sin verificador y corrección del esquema local](../documentacion/sprint-1-valeria/decision-cedula-diez-digitos.md), decisión posterior del usuario.
- [Conversión administrativa temporal](../documentacion/sprint-1-valeria/conversion-administrativa-temporal.md), ampliación autorizada.

El CSV no se modificó. Sus criterios originales de verificador y rechazo al ausente fueron sustituidos por instrucciones posteriores del usuario, documentadas en esos archivos.

## Estado inicial y resultado

| Elemento | Estado inicial | Estado de cierre |
| --- | --- | --- |
| Padrón independiente | No existía tabla ni adaptador | Tabla de prueba y contrato de tres estados |
| validado_en | Columna existente sin escritura | Solo se asigna después de confirmar condición activa |
| Duplicados | Consultas previas e índices parciales | Normalización, índices, rollback y carreras PostgreSQL probados |
| Cédula | Reglas contradictorias entre código, SQL y pruebas | Diez dígitos ASCII en frontend, backend y SQL, por instrucción del usuario |
| Consentimiento | Solo se solicitaba en React | Booleano true obligatorio en API y servicio; fecha y versión persistidas |
| Hash | PBKDF2 predeterminado | Argon2id para nuevas claves, lectura y actualización de hashes históricos |
| Fallos internos | Sin respuesta global segura para todos los fallos | Respuesta genérica y diagnóstico por tipo de error sin detalles sensibles |
| Código de socio | Carrera posible tras comprobar disponibilidad | Reintentos acotados con savepoints para la restricción conocida |
| Diagramas | Faltaba consolidar el flujo real | Cuatro fuentes Mermaid y cuatro SVG generados |

## Reglas vigentes

1. Cédula como texto, exactamente diez dígitos ASCII del 0 al 9. Se conservan ceros iniciales; no se calcula verificador ni se valida provincia. El servicio elimina espacios exteriores antes de comprobar el formato.
2. Correo y username se normalizan con trim y minúsculas. Los índices únicos protegen también las escrituras directas con espacios ordinarios exteriores.
3. Padrón ACTIVO: crear usuario, socio con fecha, rol Socio y consentimiento.
4. Padrón NO_ENCONTRADO: crear usuario general y consentimiento, sin fila socio ni roles. Puede entrar a Mi cuenta; el servidor deniega áreas protegidas.
5. Padrón INACTIVO: rechazar el registro. Un fallo de infraestructura o estado desconocido no se interpreta como ausencia ni actividad.
6. Campos de estado, roles, fecha o resultados de validación enviados por el cliente se rechazan.
7. El administrador activo puede confirmar y convertir una cuenta general activa. La función temporal no reactiva padrón inactivo, no modifica claves y no convierte cuentas con otros roles. Reintentos administrativos no duplican efectos.
8. Consentimiento, contraseña, obligatoriedad y límite de solicitudes siguen siendo autoridades del backend.

## Arquitectura y transacción

Las vistas y serializadores gestionan HTTP y formato; los servicios coordinan las reglas y transacciones; los repositorios encapsulan el acceso ORM a PostgreSQL. El puerto Padron.consultar_estado devuelve un EstadoPadron explícito y puede inyectarse en pruebas. No hay API pública de consulta del padrón.

Registro y conversión usan atomic. La consulta de una fila existente del padrón la bloquea hasta terminar la operación. La conversión bloquea además la cuenta destino. Usuario, socio cuando corresponde, rol, consentimiento y auditoría se confirman o revierten juntos según el caso de uso.

Solo SQLSTATE 23505 y nombres conocidos de restricciones de identificadores se traducen a duplicado de cuenta después del rollback. Las colisiones del código de socio usan savepoints internos: hasta tres intentos de inserción y hasta diez búsquedas por generación de candidato. Una colisión de otra restricción se propaga como tal. Si se agota la generación, se devuelve 503 y se revierte el caso de uso completo.

Las respuestas internas no incluyen SQL, rutas, contraseñas ni trazas. El log de fallos no previstos registra únicamente el tipo de excepción, sin su mensaje ni el contenido de la petición.

## Persistencia y datos

Modelos managed=False: el esquema se gestiona mediante SQL 01–06. Se reutilizaron roles, usuario, socio, consentimiento y auditoría; se incorporaron padrón e índices normalizados como mínimo de T-011/T-012 necesario para estas subtareas.

En una fase anterior se aplicaron SQL 05/06 al esquema de cooperativa_db para resolver el 503 de la aplicación habitual, conservando las cuentas y sus valores. No se cargó padrón sintético en esa base. La demo separada conserva sus propios datos sintéticos y cuentas de prueba. Se creó anteriormente admin.validacion en la base local para probar el proceso administrativo solicitado.

Durante este cierre del 10 de noviembre no se modificaron datos ni esquema de la base de trabajo: las pruebas usan bases temporales test_*. No se recreó ni eliminó cooperativa_db, no se editaron secretos ni .env, y no se hicieron commits, push o despliegues.

Preparación y reversión: [guía de operación](../documentacion/sprint-1-valeria/operacion-y-verificacion.md). Los scripts de reversión están separados del conjunto que carga el runner. Ningún script corrige o elimina cuentas automáticamente ante conflictos.

## Fases y cierre

| Fase | Estado | Evidencia |
| --- | --- | --- |
| 1 Inventario y trazabilidad | Completada | CSV, estado inicial e historial conservados |
| 2 Decisiones y contratos | Completada | Reglas posteriores y contrato actual explícitos |
| 3 Persistencia y datos sintéticos | Completada para esta entrega | Preparación, restricciones y reversión verificadas en PostgreSQL |
| 4 HU-006 | Completada según reglas acordadas | Activo, inactivo, ausente, fallo, campos manipulados y ausencia de efectos parciales |
| 5 HU-008 | Completada | Duplicados, escritura directa, normalización, carreras y colisiones de códigos |
| 6 Integración y errores | Completada por pruebas automatizadas | API de registro y conversión, permisos, errores seguros y React compilado |
| 7 Documentación y verificación | Completada con límites explícitos | Reporte de cierre y cuatro diagramas exportados |

## Evidencia final del 10 de noviembre

- manage.py check: sin incidencias.
- Suite completa: **108 pruebas aprobadas**, PostgreSQL real, 30.070 s. La base temporal se creó y eliminó mediante el runner protegido.
- Casos nuevos: colisión real del código con reintento, agotamiento y rollback, integridad distinta sin reinterpretación, generación acotada, reutilización en conversión, JSON mal formado, obligatoriedad, entrada SQL tratada como texto y logs seguros.
- Carreras de registro por cédula, correo y username, más cuenta general; conversión por dos administradores: verificadas con conexiones PostgreSQL independientes.
- npm run build: correcto, 55 módulos transformados.
- npm run lint: salida 0, conserva las 14 advertencias anteriores de Fast Refresh en paneles; no añade advertencias en los cambios de cierre.
- [Fuentes e imágenes de clases, registro, login y conversión](../documentacion/sprint-1-valeria/diagramas/README.md).
- [Matriz de aceptación y resumen de cierre](../documentacion/sprint-1-valeria/cierre-valeria-sprint-1.md).

## Límites y responsabilidades pendientes

No se marca completo todo el Sprint 1 del equipo. HU-010, HU-012 y HU-015 tienen responsables distintos y sus brechas no se resuelven mediante esta entrega. La verificación visual interactiva del formulario, HTTPS, SMTP real e integraciones institucionales no se presentan como realizadas.

T-004 y T-007 quedan cubiertas para este flujo. No se cierra su alcance transversal en módulos futuros. T-013, T-027, T-039 y T-040 figuran en Sprint 0 como transversales, pero su trabajo previsto corresponde a fases posteriores y a módulos de auditoría general, puntos, referidos o canjes. T-011/T-012 conservan la responsabilidad de integración general de su responsable de BD.

Las historias de Valeria planificadas en Sprint 2–5 permanecen fuera del alcance acordado de este cierre. No se inventan resultados de cobertura global ni pruebas sobre módulos aún no implementados.
