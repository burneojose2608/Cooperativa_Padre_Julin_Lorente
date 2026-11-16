# Arquitectura, entornos y tareas transversales de Sprint 1

## Arquitectura y contratos iniciales

Se conserva el monolito modular Django REST Framework/PostgreSQL con presentación React. Las vistas y serializadores reciben HTTP, los servicios coordinan reglas y transacciones, y los repositorios acceden a datos mediante ORM. Registro, autenticación, sesiones, roles y conversión tienen responsabilidades separadas dentro del módulo de usuarios. No se crean microservicios ni otro sistema de identidad.

| Contrato | Entrada | Salida |
| --- | --- | --- |
| POST registro | Datos personales, clave y consentimiento | 201 con cuenta y rol/código si corresponde |
| POST login | identificador y clave | access, refresh y usuario con roles/áreas |
| GET yo | JWT access y sesión vigente | Perfil propio y roles actuales |
| GET areas/area | JWT y rol vigente en base | 200 permitido o 403 denegado |
| POST refresh | Refresh firmado y sesión vigente | Nuevo access sujeto al mismo sid |
| POST logout | Access de una sesión vigente | 204 después de revocar en servidor |
| POST actividad | Access de una sesión vigente | 204 sin revivir una sesión caducada |
| Administración de conversión | Administrador y confirmación explícita | Conversión única con auditoría |

Los errores de negocio mantienen código, mensaje y campo; los errores de autenticación/renovación pueden responder 401 con detail genérico. No se devuelven hash, SQL, contraseñas o trazas. Los demás subsistemas conservan sus historias futuras y no se presentan como módulos funcionales nuevos.

## T-005 repositorio, pipeline y entornos

El repositorio mantiene su rama local main. La política definida es main para integración revisada, ramas feature/sprint-1-descripcion para cambios y pull request con comprobaciones antes de fusionar. No se crearon ramas ni protecciones remotas sobre los cambios locales del usuario.

Se preparó [.github/workflows/sprint-1.yml](../../.github/workflows/sprint-1.yml), con dos trabajos independientes:

- Backend: PostgreSQL 17 efímero, Python 3.14, instalación, check y suite Django sobre test_cooperativa_ci.
- Frontend: Node 26, npm ci, pruebas, lint y build.

El workflow contiene únicamente credenciales ficticias del servicio efímero de CI, nunca las locales. No utilizar sus valores en un despliegue. .env, entornos virtuales y claves TLS locales permanecen fuera del repositorio.

La configuración está preparada, pero **no se ejecutó en GitHub**, porque no se hizo commit ni push. Los comandos de los trabajos sí se ejecutaron localmente en los entornos aislados descritos en el informe de verificación.

| Entorno | Propósito | Separación |
| --- | --- | --- |
| cooperativa_db | Trabajo local | Cuentas conservadas, sin reinicialización |
| test_* | Suite automatizada | Creación y destrucción por runner protegido |
| sprint1_* | Demo y HTTPS | Datos y sesiones de prueba separados |
| cooperativa_ci / test_cooperativa_ci | CI preparado | Contenedor efímero, sin secretos locales |

## T-009 contraseñas

El validador compartido exige ocho caracteres como mínimo, letras y números, y rechaza claves comunes mediante el catálogo incluido en Django. Se aplica a registro público, cuentas internas y recuperación. El servidor es la autoridad y el formulario muestra el error en clave.

Las nuevas claves usan Argon2id con sal individual. Se conservan los lectores históricos y su actualización durante login. No se aplica el rechazo de claves comunes retroactivamente para bloquear cuentas existentes. Hay pruebas de claves comunes, clave aceptada, sales diferentes y rechazo sin cuenta parcial.

## T-010 modelo de datos de esta entrega

- [Diccionario de once tablas y 52 columnas](datos/diccionario-datos.md).
- [E-R en SVG](datos/modelo-er.svg) y [fuente editable](datos/modelo-er.mmd).
- [Generador de metadatos](../../backend/scripts/exportar_esquema_sprint1.py).

El generador consulta information_schema y catálogos PostgreSQL en READ ONLY. Incluye tipos, nulabilidad, claves, restricciones e índices normalizados. No consulta filas de personas ni exporta valores de claves o tokens.

Este catálogo cubre usuarios de Sprint 1. El modelo integral de los catorce módulos y su revisión conjunta formal siguen en el alcance transversal de T-010, sin declararse completos por esta exportación.

## Tareas transversales originalmente ligadas a Sprint 1

El CSV actual ubica T-001 a T-012 en Sprint 0, ejecutadas según las necesidades funcionales. Se distinguen de las siete filas de historias/subtareas de Sprint 1:

| Tarea | Cobertura en este cierre | Límite |
| --- | --- | --- |
| T-001 | Decisiones y matriz UR/RF/HU/RNF | No se inventa aprobación de PO/docente |
| T-002 | Capas y contratos iniciales de usuarios | Módulos posteriores no implementados |
| T-003 | Flujos del subsistema implementado | Actividades de referidos, canjes y evaluación son diseño transversal futuro |
| T-004 | Clases, registro, login, sesiones y conversión de cuenta | Conversión a puntos/canjes no declarados como código de Sprint 1 |
| T-005 | Workflow, ramas y entornos | CI remoto y protecciones no ejecutados |
| T-006 | Interfaz y ajustes móviles existentes | Archivo Figma, WCAG completo y revisión visual no verificados |
| T-007 | Entradas, ORM y errores seguros | Subsistema actual |
| T-008 | Rutas, layout, HTTP y formularios con tests | Revisión de píxeles pendiente por host no disponible |
| T-009 | Argon2id, sal y rechazo de claves comunes | Sin cambiar claves anteriores |
| T-010 | Diccionario y E-R de usuarios | Modelo global de catorce módulos fuera de este cierre |
| T-011 | Esquema, restricciones y reversión del registro | Sin recrear cooperativa_db ni añadir otra tabla de sesiones |
| T-012 | Carga sintética reproducible | Solo bases aisladas |

Código funcional terminado no equivale a aceptación de todas las tareas documentales y de diseño transversal del proyecto.
