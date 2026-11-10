# Cierre de la entrega de Valeria en Sprint 1

Fecha de revisión: 10 de noviembre de 2026. Este documento resume la implementación vigente y su evidencia. Los documentos de decisiones anteriores conservan el historial; para el estado actual deben consultarse este cierre y el plan consolidado.

## Resultado y límites

HU-006 y HU-008 están completas para las reglas expresamente acordadas con el usuario. Se completó el apoyo de T-004 y T-007 para el módulo de usuarios de esta entrega. La conversión administrativa temporal también está implementada y cubierta por pruebas. Esto no equivale a cerrar todas las historias del Sprint 1 del equipo ni las tareas transversales completas de módulos futuros.

| Asignación de Valeria | Criterio vigente | Evidencia y resultado |
| --- | --- | --- |
| HU-006 / RF-01-6 | Solo activo obtiene rol Socio | Padrón independiente, puerto inyectable y pruebas activo/inactivo/ausente/fallo |
| HU-006 y cambio posterior | Ausente puede crear usuario general | Cuenta sin socio ni rol, perfil propio y áreas protegidas denegadas |
| HU-006 | No confiar en estado o validación del cliente | Campos prohibidos rechazados; fecha generada en servidor |
| HU-008 / RF-01-8 | Cédula, correo y username únicos | Comprobaciones normalizadas, índices PostgreSQL y escrituras directas probadas |
| HU-008 | Concurrencia sin cuentas parciales | Cuatro carreras de registro con conexiones independientes |
| HU-008 y soporte del registro | Colisión del código de socio sin fallo prematuro | Restricción real PostgreSQL, savepoint y reintento selectivo; agotamiento revierte toda el alta |
| T-007, apoyo Sprint 1 | Validar en servidor y usar consultas parametrizadas | Serializador obligatorio, consentimiento true, ORM y prueba de SQL tratado como texto |
| T-007, apoyo Sprint 1 | Errores sin SQL, secretos, rutas o trazas | Contrato HTTP genérico y log solo por tipo; pruebas de ambos canales |
| T-004, apoyo Sprint 1 | Clases y secuencias de lo entregado | Cuatro fuentes Mermaid y cuatro SVG: clases, registro, login y conversión administrativa |
| Ampliación autorizada | Validación y conversión administrativa temporal | Administrador vigente, confirmación explícita, transacción, auditoría e idempotencia |

Las reglas posteriores sustituyen dos criterios del CSV original: se aceptan diez dígitos sin verificador y se permite cuenta general para cédulas ausentes. El padrón activo sigue siendo obligatorio para el rol Socio. Esas diferencias no se ocultan ni se presentan como cumplimiento literal del CSV sin cambios.

## Trabajo completado en esta revisión

Se detectó una carrera residual entre la generación de un código libre y su inserción. El generador compartido ahora acota la búsqueda a diez candidatos y permite hasta tres intentos de inserción. Solo reintenta SQLSTATE 23505 de socio_codigo_socio_key después del rollback del savepoint. No transforma una colisión de cédula ni una clave primaria en supuesto código repetido. Agotar los intentos produce 503 y rollback del caso de uso completo.

El formulario marca sus campos obligatorios, informa su obligatoriedad, valida los espacios exteriores de manera coherente con lo que envía al backend y evita un segundo envío mientras está procesando. Se conserva la validación del servidor como autoridad.

El manejador registra únicamente el tipo de los fallos no previstos. No escribe el mensaje bruto de la excepción ni la petición, y mantiene las respuestas genéricas. Se comprobaron errores de programación, infraestructura y ejecución para evitar filtraciones tanto en respuesta como en log.

Se consolidó el plan para retirar contradicciones entre cierres anteriores. El plan previo permanece en docs/historial-plan-valeria-hasta-2026-11-09.md. No se modificó el CSV original ni se cambiaron los responsables del equipo.

## Evidencia ejecutada

| Verificación | Resultado |
| --- | --- |
| manage.py check | Sin incidencias |
| Pruebas dirigidas de esta revisión | 28 aprobadas; subconjunto incluido en la suite final |
| Suite completa del backend | **108 pruebas aprobadas**, 30.070 s, PostgreSQL real |
| Base de pruebas | Runner con prefijo test_; creada y eliminada sin recrear cooperativa_db |
| Concurrencia de cuentas | Cédula, correo y username de socio, más cuenta general; una sola cuenta por carrera |
| Concurrencia de conversión | Dos administradores y conexiones diferentes; una conversión y una auditoría |
| Colisiones de código | Primera inserción realmente rechazada por PostgreSQL; siguiente inserción aceptada sin transacción rota |
| npm run build | Aprobado, 55 módulos transformados |
| npm run lint | Salida 0; 14 advertencias previas de Fast Refresh en paneles, sin nuevas advertencias del cierre |
| Diagramas | Cuatro fuentes Mermaid procesadas y exportadas a SVG; revisión de sus imágenes de control |

Archivos nuevos de evidencia de cierre: backend/apps/usuarios/tests/test_codigos_socio.py y test_validacion_y_errores.py. Se amplió además test_registro_sprint1.py. Las pruebas de registro, persistencia, esquema, roles, recuperación y conversión anteriores forman parte de las 108 pruebas; no se suman otra vez como verificaciones independientes.

## Documentos para corroboración

- [Plan consolidado y fases](../../docs/plan-valeria-sprint-1.md).
- [Diagramas SVG y fuentes editables](diagramas/README.md).
- [Arquitectura y contrato del registro](arquitectura-y-contrato.md).
- [Preparación, SQL y reversión](operacion-y-verificacion.md).
- [Regla de diez dígitos y corrección del 503](decision-cedula-diez-digitos.md).
- [Conversión administrativa temporal](conversion-administrativa-temporal.md).

No se necesitan cambios nuevos de esquema para este cierre: las bases ya preparadas con SQL 01–06 mantienen sus tablas. Durante esta revisión no se cambiaron datos o secretos de la base de trabajo, ni se promovió ninguna cuenta adicional. El código de los servicios comparte la creación segura de socio tanto para el registro como para la conversión.

## Lo que continúa fuera de esta entrega

El CSV asigna otras historias a Valeria en sprints posteriores. Se conservaron sin intervenir:

| Sprint | Historias de Valeria fuera de este cierre |
| --- | --- |
| 2 | HU-005, HU-007, HU-016, HU-062, HU-064 |
| 3 | HU-018, HU-020, HU-024, HU-026, HU-040, HU-046, HU-048, HU-084 |
| 4 | HU-028, HU-029, HU-033, HU-041, HU-049, HU-055, HU-072 |
| 5 | HU-052, HU-065, HU-075, HU-076, HU-078, HU-081, HU-086, HU-089, HU-090 |

Las tareas T-013, T-027, T-039 y T-040 figuran como transversales en Sprint 0, con planificación original posterior. El interceptor general de auditoría, los puntos, la cobertura de referidos/gamificación/canjes y su integración no se declaran terminados por estas pruebas. Tampoco se declaran completos los diagramas de esos módulos.

Los pendientes de HU-010, HU-012 y HU-015 siguen en el responsable de autenticación indicado por el CSV. El diagrama de login refleja esas brechas: documentar el comportamiento no implementa la invalidación de sesión ni modifica las políticas de login.

La revisión visual interactiva de la aplicación, SMTP real, HTTPS y despliegue no se presentan como comprobaciones realizadas en este cierre. Las imágenes de los diagramas sí se renderizaron y revisaron localmente. No se generó un informe de cobertura global para módulos futuros ni se publicaron resultados en CI.

Cambios locales listos para revisión. Sin commits, push ni despliegue.
