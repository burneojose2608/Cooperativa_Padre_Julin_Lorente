# Avance de la plataforma

## Trabajo realizado

- [x] Unificar encabezados, tarjetas, tablas, formularios y estados de foco en el panel por roles. Mejorar el indicador de notificaciones y la presentación de catálogos compartidos. Verificación local con 67 pruebas Vitest y compilación Vite. Se conserva la verificación transversal en navegadores y accesibilidad de T-041 y T-042.

- [x] Conservar el backlog original y sus 150 ítems, sprints y relaciones padre.
- [x] Generar 14 especificaciones con planes, tareas, contratos y modelo de datos.
- [x] Conservar las 91 relaciones HU–RF y enlazar UR y CU.
- [x] Establecer la constitución y visión consolidada a partir de las fuentes del proyecto.
- [x] Implementar dominio, API y pantallas para los módulos de participación de los sprints 3 a 5.
- [x] Añadir la evolución aditiva del esquema y preservar cuentas y permisos existentes.
- [x] Verificar el respaldo mediante restauración en una base aislada.
- [x] Probar el recorrido referido → puntos → canje → entrega y los conflictos de saldo, stock e intentos.
- [x] Conectar la confirmación de prospectos con una cola duradera y reintentos.
- [x] Implementar mantenimiento de prospectos y generación de respaldos desde el trabajador.
- [x] Actualizar la guía operativa y el catálogo complementario de clases.

## Cierre pendiente

- [x] Descargar y verificar la CLI y las skills oficiales de Spec Kit.
- [x] Revisar los criterios de las HU y registrar la evidencia técnica local por módulo.
- [ ] Completar las cuatro verificaciones de Autenticación y Referidos que requieren dispositivo, entorno desplegado o canal institucional.
- [ ] Conciliar Enterprise Architect, firmas, relaciones y PDF con la evolución del código.
- [ ] Ejecutar revisión visual E2E y compatibilidad en los navegadores y anchos acordados.
- [x] Medir cobertura y ejecutar las comprobaciones locales automatizadas de seguridad, accesibilidad y rendimiento.
- [ ] Medir carga de operaciones habituales con la concurrencia de RNF-04 y RNF-05 y completar las auditorías de accesibilidad y seguridad.
- [ ] Validar los valores de incentivos, el vencimiento de puntos y la integración institucional.
- [ ] Verificar SMTP y el canal telefónico definitivo.
- [ ] Configurar despliegue HTTPS, supervisión persistente del trabajador, monitoreo y política externa de respaldos.

Los pendientes de infraestructura y aceptación conservan sus tareas originales de Sprint 0.
El desarrollo anticipado de funcionalidades no cambia los estados de Jira ni certifica esos controles externos.

## Auditoría de los sprints del 22/11/2026

El verificador de trazabilidad cruzó las 91 relaciones HU–RF–UR–CU y las referencias a los 26 RNF. Los prerrequisitos de Spec Kit pasaron para los 14 módulos y el plan transversal. El [inventario por módulo](../estado-implementacion.csv) enlaza la aceptación de cada funcionalidad.

| Sprint | Historias | Subtareas | Resultado |
| --- | ---: | ---: | --- |
| 0 | — | — | Las 45 tareas técnicas se revisan en la tabla siguiente. |
| 1 | 2 | 5 | Evidencia funcional local. HU-009 conserva la comprobación visual y de HTTPS desplegado. |
| 2 | 11 | 6 | Evidencia funcional local. HU-011 conserva el correo definitivo de recuperación, HU-019 la compartición nativa y HU-023 los canales institucionales de confirmación. |
| 3 | 19 | 6 | Evidencia técnica local en los módulos correspondientes. |
| 4 | 17 | 6 | Evidencia técnica local en los módulos correspondientes. |
| 5 | 15 | 4 | Evidencia técnica local en los módulos correspondientes. |

### Evidencia de las 45 tareas técnicas

| Tareas | Resultado de la revisión |
| --- | --- |
| T-001, T-002 | Trazabilidad comprobada y arquitectura modular documentada en el [plan transversal](plan.md) y los planes de módulo. |
| T-003, T-004 | Hay diagramas de casos de uso, actividades y clases. Sigue pendiente la conciliación con el código y la evidencia actualizada de las secuencias. [Resumen del modelo](../../documentacion/RESUMEN-PROYECTO.md). |
| T-005 | Repositorio y workflow de [CI](../../.github/workflows/ci-plataforma.yml) configurados. La operación del entorno definitivo sigue pendiente. |
| T-006 | No se localizó un enlace o exportación de Figma que permita verificar los prototipos del backlog. |
| T-007, T-008 | Django y React funcionan en local. Hay pruebas de validación, errores y compilación. La compatibilidad visual conserva su verificación propia. |
| T-009, T-011, T-014, T-036 | Evidencia local de hash y política de clave, identidad y padrón, bloqueo, permisos, titularidad y revocación. [Usuarios](../001-usuarios/acceptance.md) y [Autenticación](../002-autenticacion/aceptacion.md). |
| T-010 | Hay evidencia del diccionario y E-R del Sprint 1 y modelos por módulo. Sigue pendiente un diccionario y E-R consolidados del esquema vigente. [Sprint 1](../../documentacion/entregable/sprint-1/matriz-trazabilidad.md). |
| T-012 | Las pruebas usan datos sintéticos y bases aisladas. La carga `poblar_demostracion` prepara catálogos y actividad sintética reproducibles. Se probó en PostgreSQL aislado y se aplicó de forma aditiva en la base local. |
| T-013, T-017 | Auditoría desde los servicios y bitácora inmutable comprobadas localmente. La implementación observada usa llamadas explícitas a la auditoría. El backlog original describe un interceptor. |
| T-015, T-016 | Evidencia local de minimización por rol y de validación y almacenamiento privado de archivos. [Referidos](../003-referidos/aceptacion.md), [Contenidos](../009-contenidos/aceptacion.md), [Comunidad](../012-comunidad/aceptacion.md) y [Reportes](../014-reportes/aceptacion.md). |
| T-018, T-019, T-020, T-021, T-022, T-023, T-024, T-025, T-026 | Esquema e integración local comprobados para referidos, movimientos de puntos, contenidos, notificaciones, campañas, formación, canjes, sorteos y convenios. La entrega institucional de avisos conserva su comprobación externa. [Aceptación por módulo](../estado-implementacion.csv). |
| T-027, T-040 | Evidencia local de concurrencia, idempotencia y recorrido desde referido hasta entrega del canje. [Referidos](../003-referidos/aceptacion.md). |
| T-028, T-029 | Configuración HTTPS/HSTS y endpoint de salud comprobados localmente. Faltan TLS y redirección en el servidor definitivo, sondas operativas y el período de disponibilidad de RNF-08. |
| T-030, T-031 | Evidencia local de persistencia y recorridos de juegos, retos y comunidad. [Juegos y retos](../011-juegos-retos/aceptacion.md) y [Comunidad](../012-comunidad/aceptacion.md). |
| T-032, T-044 | Consultas, exportaciones y persistencia tienen evidencia local. Queda por revisar rendimiento, planes de ejecución e índices con volumen representativo. [Reportes](../014-reportes/aceptacion.md). |
| T-033, T-045 | Comando de respaldo y restauración de 59 tablas comprobada históricamente en base temporal. Falta acreditar la ejecución diaria y retención operativa. [Verificación de la evolución](../../documentacion/VERIFICACION-EVOLUCION.md). |
| T-034 | Mantenimiento local probado con expiración y anonimización de prospectos. Falta evidencia de ejecución periódica en el entorno definitivo. [Referidos](../003-referidos/aceptacion.md). |
| T-035 | La evidencia disponible corresponde a 200 y 500 solicitudes a `/api/salud/`, con 20 y 40 hilos, respectivamente. Falta el perfil de operaciones habituales y la concurrencia especificada por RNF-04 y RNF-05. |
| T-037, T-042 | Hay regresión defensiva y pruebas automatizadas de accesibilidad. Sigue pendiente la revisión integral, incluidos el contraste y la navegación con tecnología de asistencia. |
| T-038 | La documentación de entrega local existe. Su cierre definitivo depende de las verificaciones abiertas. |
| T-039 | Evidencia histórica de cobertura del 93,3 % para los módulos medidos. [Resultado y alcance](../../documentacion/VERIFICACION-EVOLUCION.md#verificación-de-ci-y-requisitos-no-funcionales-locales-21112026). |
| T-041 | Pendiente matriz de compatibilidad de 320 a 1920 px y versiones de Chrome, Edge, Firefox y Safari. |
| T-043 | Recorridos integrados de Formación, Comunidad y Reportes comprobados localmente. La ejecución visual en dispositivos y navegadores conserva su verificación propia. |

## Verificación transversal de RNF

Las referencias T- identifican las tareas originales de [Sprint 0](../README.md#sprint-0). Registrar fecha, entorno, caso y resultado para cada RNF, incluso cuando una ejecución cubra varios.

| RNF | Tarea original | Evidencia requerida |
| --- | --- | --- |
| RNF-01 | T-009, T-036 | Pruebas de hash y sal, mínimo de 8 caracteres, claves comunes rechazadas y campos ocultos. |
| RNF-02 | T-011, T-018, T-043 | Alta de socio y confirmación de prospecto con fecha, hora y versión de política. |
| RNF-03 | T-041 | Resultados y capturas de 320 a 1920 px en las dos últimas versiones estables de Chrome, Edge, Firefox y Safari. |
| RNF-04 | T-035, T-044 | Perfil de consultas habituales, 200 usuarios concurrentes y percentil 95 de respuesta de hasta 2 s. |
| RNF-05 | T-035 | Informe con 500 usuarios concurrentes y menos del 1 % de respuestas HTTP 5xx. |
| RNF-06 | T-013, T-017 | Bitácora con campos exigidos y comprobación de que la aplicación impide editar o eliminar entradas. |
| RNF-07 | T-042 | Auditoría WCAG 2.1 AA de contraste y etiquetado, más evidencia de mensajes correctivos en formularios. |
| RNF-08 | T-029 | Sondas e informe mensual de disponibilidad mínima del 99 % durante 6 meses, con exclusiones documentadas. |
| RNF-09 | T-028 | Verificar TLS 1.2 o superior, redirección HTTP y encabezado HSTS en el entorno desplegado. |
| RNF-10 | T-036 | Casos por rol, permiso revocado y titular ajeno para lectura y escritura en servidor. |
| RNF-11 | T-036 | Verificar la invalidación de access y refresh tras 15 minutos de inactividad. |
| RNF-12 | T-027, T-040 | Reintentos y operaciones simultáneas de acreditación, reserva y descuento. Verificar saldo no negativo y sin movimientos duplicados. |
| RNF-13 | T-018, T-024, T-025 | Verificar estado anterior y nuevo, responsable y fecha en referidos, canjes y sorteos. |
| RNF-14 | T-015, T-043 | Comparar datos visibles por rol en listados, reportes, clasificaciones, sorteos y comunidad. |
| RNF-15 | T-033, T-045 | Registros de respaldo cada 24 h y retención mínima de 7 días. Adjuntar restauración en base aislada. |
| RNF-16 | T-023, T-043 | Comprobar unicidad y generación no secuencial del código, y rechazo de códigos inválidos. |
| RNF-17 | T-007, T-043 | Comprobar confirmaciones, advertencias y errores comprensibles sin detalles internos. |
| RNF-18 | T-021, T-043 | Simular un fallo de entrega, verificar hasta tres reintentos, persistencia del error y respuesta independiente de la solicitud principal. |
| RNF-19 | T-002, T-039 | Revisar separación de capas y registrar cobertura de al menos el 70 % de la lógica de referidos, gamificación y canjes. |
| RNF-20 | T-007, T-037 | Revisar validación del servidor, consultas parametrizadas y escape de salida. Adjuntar evidencia de regresión defensiva. |
| RNF-21 | T-014, T-036 | Verificar bloqueo de 15 min tras cinco intentos fallidos y límites de los formularios públicos. |
| RNF-22 | T-025, T-043 | Verificar generador criptográfico, congelación de participaciones y hash previo a la ejecución. |
| RNF-23 | T-012 | Verificar origen sintético o anonimizado de datos y destinos de integración en el entorno MVP. |
| RNF-24 | T-026, T-043 | Revisar formularios, API y persistencia de Bienestar para comprobar ausencia de datos clínicos. |
| RNF-25 | T-034 | Verificar la anonimización o eliminación configurable a 12 meses por defecto y el procedimiento a solicitud del titular. |
| RNF-26 | T-016, T-043 | Verificar tipo real, extensión, tope de 10 MB, renombrado y almacenamiento privado. |

## Recorridos integrados

- [x] T-040 Verificar RF-03-2, RF-03-3, RF-03-8, RF-05-2, RF-08-2, RF-08-3 y RF-08-6 desde el consentimiento hasta la entrega. Repetir con rechazo de canje y comprobar liberación de puntos y stock. [Evidencia en PostgreSQL aislado](../003-referidos/aceptacion.md#integración-con-gamificación-y-recompensas).
- [x] T-043 Verificar campaña elegible, matrícula, material privado, evaluación, certificado y actividad resultante para puntos, retos y sorteos. [Evidencia en PostgreSQL aislado](../006-formacion/aceptacion.md).
- [x] T-043 Verificar publicación con alias, reporte, resolución motivada y visibilidad posterior según la decisión de moderación. [Evidencia en PostgreSQL aislado](../012-comunidad/aceptacion.md).
- [x] T-043 Verificar consultas y exportaciones por rol con filtros, fecha, minimización de datos y comprobación de CSV. [Evidencia en PostgreSQL aislado](../014-reportes/aceptacion.md).
