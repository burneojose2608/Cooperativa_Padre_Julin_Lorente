# Aceptación local de Formación y sus incentivos

El 20 y 21 de noviembre de 2026 se verificaron los requisitos funcionales del módulo de Formación y el recorrido transversal T-043 con datos sintéticos, el cliente HTTP de Django, una base PostgreSQL temporal con prefijo `test_` y Vitest con jsdom. Las reglas de puntos, el reto y los sorteos del caso son datos de prueba.

| Historia y trazabilidad | Evidencia por criterio y recorrido |
| --- | --- |
| HU-027 · RF-04-3 · UR-14 · CU-G06 | La API devolvió la campaña activa y vigente del segmento del socio y excluyó la de otra agencia. |
| HU-044 · RF-06-6 · UR-24 · CU-G19 · RNF-26 | 1. Responsabilidad Social creó la capacitación, sus módulos y la evaluación, con denegación de publicar antes de configurar módulos y evaluación. 2. Subió material al repositorio de materiales educativos y lo asoció al módulo. 3. Consultó inscritos, módulos completados, porcentaje de avance, intentos y nota máxima en `/participantes/`, denegando a socios (403). |
| HU-039 · RF-06-1 · UR-20 · CU-G08 · RNF-17 | 1. El catálogo mostró capacitaciones publicadas con descripción, modalidad, duración y requisitos. 2. La API rechazó la inscripción sin confirmar los requisitos publicados (400). 3. Repetir la solicitud devolvió la inscripción existente sin duplicar filas (`uq_inscripcion`). |
| HU-040 · RF-06-2 · UR-21 · CU-G08 · RNF-10, RNF-17 | 1. El aula y la descarga privada exigieron inscripción propia en capacitación publicada, rol Socio validado y permiso vigente. 2. Completar dos módulos actualizó el avance de 50 % a 100 % con idempotencia. 3. El avance se conservó al iniciar una nueva sesión; tras revocar el permiso o cerrar sesión, la descarga y el aula se denegaron (403/404/401). |
| HU-041 · RF-06-3 · UR-22 · CU-G08 · RNF-06, RNF-12, RNF-17 | 1. La evaluación omitió las respuestas correctas, guardó las respuestas enviadas y calculó la nota en servidor (rechazando envío de `nota` desde el cliente con 400). 2. Evaluó aprobación contra `nota_minima`. 3. Controló `max_intentos` impidiendo nuevos intentos al agotarlos o tras aprobar, y bloqueó editar la evaluación con inscritos. 4. La aprobación disparó una sola acreditación de puntos y registró la inscripción en auditoría. |
| HU-042 y HU-043 · RF-06-4 y RF-06-5 · UR-23 · CU-G08 · RNF-10, RNF-16 | 1. Al aprobar se emitió un único certificado (`Certificado.inscripcion` único) cuyo PDF contiene nombre del socio, capacitación, fecha y código de verificación de 32 caracteres hexadecimales no secuenciales (`secrets.token_hex(16)`). 2. Sin aprobación no se emite certificado. 3. El socio consulta su historial en `MisActividadesView`, descarga su PDF y recibe 404 al intentar descargar el certificado de otro socio. |
| HU-045 · RF-06-7 · UR-23 · CU-G19 · RNF-16, RNF-21 | 1. El endpoint público `/api/plataforma/certificados/verificar/{codigo}/` informa `valido: True` para un código emitido y `valido: False` para un código inexistente. 2. Devuelve únicamente `{valido, titulo, emitido_en, codigo}` sin cédula ni datos personales adicionales. 3. Aplica `AnonRateThrottle`, respondiendo 429 al superar 60 consultas por minuto para impedir enumeración. |
| HU-046 · RF-06-8 · UR-48 · CU-G19 | 1. Responsabilidad Social registra talleres presenciales o virtuales con título, fecha, cupo, modalidad, lugar/enlace y duración. 2. Un taller con `cupo < 1` se rechaza con 400. 3. Los talleres registrados se consultan y editan con auditoría. |
| HU-047 · RF-06-9 · UR-49 · CU-G08 · RNF-12 | 1. La inscripción al taller respeta el cupo configurado y rechaza con 400 cuando se llena o cuando la fecha ya pasó. 2. El personal autorizado consulta inscritos y valida la asistencia una vez alcanzada la fecha del taller. 3. La asistencia acredita los puntos una sola vez (`origen_tipo='TALLER'`). |
| HU-032, HU-078 y HU-049 · RF-05-2, RF-11-8 y RF-07-2 | En el recorrido T-043, la actividad validada de capacitación acreditó 100 puntos de formación, completó el reto vigente (+100 puntos) y generó la participación en el sorteo de la campaña elegible del segmento del socio. |

## Evidencia ejecutable

- `test_t043_formacion_puntos_reto_y_sorteo_elegible`, `test_formacion_evaluacion_servidor_certificado_y_acceso_ajeno`, `test_evaluacion_limite_y_banco_no_modificable`, `test_material_de_aula_requiere_inscripcion`, `test_taller_cupo_asistencia_y_acreditacion_unica` y `test_formacion_verificacion_invalida_frecuencia_y_gestion_talleres` en [test_alcance_completo.py](../../backend/apps/plataforma/tests/test_alcance_completo.py).
- «El aula muestra el avance del servidor y habilita la evaluación al completar los módulos» en [negocio.test.jsx](../../frontend/src/panel/negocio/negocio.test.jsx).
- [Verificación de la evolución](../../documentacion/VERIFICACION-EVOLUCION.md#aceptación-local-de-formación) con los resultados de regresión.

## Pendientes externos

- Verificar en navegadores y dispositivos reales la interfaz y la accesibilidad (RNF-03, RNF-07).

## Ajuste visual del catálogo y el aula

T006 conserva la trazabilidad de HU-039, HU-040 y HU-041 indicada en la tabla. El catálogo presenta modalidad, duración en horas y requisitos. El aula tiene una vista propia con retorno al catálogo y organiza los módulos, materiales, avance y evaluación.

Verificación local mediante Vitest con datos sintéticos. La prueba de formación comprobó la duración, el progreso del 50 % al 100 %, el envío de la evaluación y el regreso al catálogo. Pasaron las 66 pruebas de frontend y la compilación de Vite.
- Validar con la cooperativa los incentivos definitivos y las integraciones institucionales.
