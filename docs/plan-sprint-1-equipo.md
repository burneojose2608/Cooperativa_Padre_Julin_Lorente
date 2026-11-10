# Plan de cierre del Sprint 1 del equipo

Fecha: 10 de noviembre de 2026. Solicitud: completar todo Sprint 1 sin limitarse al responsable original. Los responsables del CSV se conservan como trazabilidad, sin cambiar sus estados ni asignaciones.

## Línea base

| Historia | ID | Criterios principales | Estado inicial |
| --- | --- | --- | --- |
| HU-001 | 101 | Registro obligatorio, hash seguro, consentimiento, integración padrón/duplicados | Implementada con cambios de regla autorizados |
| HU-006 | 106 | Condición activa antes de habilitar Socio | Implementada; ausente permite cuenta general por decisión posterior |
| HU-008 | 108 | Unicidad cédula, correo y usuario, incluso concurrencia | Implementada y verificada |
| HU-009 | 109 | Acceso por usuario/correo, rol, bloqueo, vista adaptable y HTTPS | Parcial |
| HU-010 | 110 | Hash, cuenta activa, fallo genérico y auditoría con IP | Parcial; faltan uniformidad y algunas auditorías |
| HU-012 | 112 | Todos los roles, menú y unión de accesos | Backend existente; selector incompleto para RSE/contenidos |
| HU-015 | 115 | Logout revocado en servidor e inactividad 15 minutos | Pendiente; solo borra almacenamiento del navegador |

Fuente: documentacion/product_con_subtareas.csv y documentación de documentacion/. Se preservan las decisiones posteriores del usuario: cédula de diez dígitos sin verificador, registro general si no consta en padrón y conversión administrativa temporal.

## Decisiones y cambios previstos

- Sesión persistida en la tabla sesion existente, con ultimo_uso, vence_en y revocada_en. JWT access y refresh incluyen un identificador de sesión firmado; ambos se comprueban contra la base. No se almacenan tokens en claro.
- Revocar en logout y denegar access/refresh reutilizados; no aceptar tokens históricos sin sesión verificable. La clave del usuario no cambia: basta iniciar sesión otra vez.
- Inactividad: 15 minutos en servidor y en interfaz. Renovar un token no resucita una sesión revocada o inactiva. La actividad real de la interfaz puede notificar al servidor mientras el usuario trabaja.
- Login: misma respuesta 401 de credenciales para inexistente, contraseña incorrecta, cuenta inactiva y bloqueo. Mantener bloqueo real tras cinco fallos durante quince minutos, y auditar cada intento sin clave o token. Serializar contadores para no perder fallos concurrentes.
- Roles: la base sigue siendo autoridad; la interfaz ofrece todos los accesos asignados, incluidos RSE y contenidos, sin conceder nuevas funciones de sprints posteriores.
- HTTPS: configuración de exigencia y entorno TLS local verificable sin publicar ni cambiar la confianza del sistema operativo. Documentar la diferencia entre desarrollo HTTP local y operación HTTPS.
- Mantener las capas existentes; adaptar JWT mediante autenticación y servicios del propio módulo. Reutilizar PostgreSQL y scripts SQL existentes; documentar cualquier índice incremental necesario.

## Fases

| Fase | Estado |
| --- | --- |
| Inventario y contratos | Completada |
| Sesiones, logout y refresh | Implementada y verificada en PostgreSQL |
| Login y auditoría | Implementada, incluida concurrencia y respuesta uniforme |
| Interfaz, inactividad y multirrol | Implementada y verificada con pruebas DOM/temporizadores |
| HTTPS y adaptación de pantallas | Implementada; TLS comprobado, revisión visual 320–1920 px no verificada |
| Pruebas, diagramas y matriz de cierre | Completada con límites explícitos de verificación |

## Verificación prevista

Pruebas PostgreSQL aisladas de revocación, refresh, inactividad, bloqueo concurrente, auditoría y todos los roles; regresiones del registro y conversión; pruebas de interfaz con temporizadores y transporte simulado; lint/build; comprobación de configuración HTTPS. No recrear cooperativa_db, no exponer secretos y no hacer commits ni publicaciones.

## Resultados y decisiones finales

- **135 pruebas backend aprobadas**, 27.232 s; **20 pruebas de interfaz aprobadas**, 2.30 s.
- Build correcto, 58 módulos; lint salida 0 con las 14 advertencias previas de paneles.
- HTTPS real: cadena y hostname verificados con una CA local de prueba; logout 204 y reutilización/inactividad 401. No se instaló confianza en Windows ni en el navegador.
- Sesion reutiliza la tabla de SQL 01 y ultimo_uso de SQL 02. No se añadieron tablas, no se recreó la base original ni se modificaron las credenciales de sus cuentas. La verificación de red con login se realizó en la demo aislada.
- El lookup prioriza username, correo y finalmente cédula, y usa trim/minúsculas para cuentas históricas. No se normalizan registros existentes mediante escrituras automáticas.
- La expiración y la auditoría de fallos se confirman antes de emitir el rechazo HTTP para no perder los cambios por rollback accidental.
- Los tokens anteriores sin sid dejan de aceptarse: se solicita iniciar sesión nuevamente, sin cambiar la contraseña.
- Un token revocado se rechaza incluso al repetir logout. El servicio interno evita duplicar escrituras si dos cierres ya autenticados concurren.
- Se conserva el desarrollo HTTP local. Para el modo seguro se exige HTTPS mediante configuración y se usa un cliente de mismo origen detrás de un proxy explícitamente confiable limitado a loopback.

## Entrega y aceptación

[Índice del Sprint 1 completo](../documentacion/sprint-1-equipo/README.md), [matriz por criterio](../documentacion/sprint-1-equipo/matriz-trazabilidad.md), [verificación](../documentacion/sprint-1-equipo/verificacion.md) y [diagramas](../documentacion/sprint-1-equipo/diagramas/README.md).

La programación de las siete filas de historia/subtarea de Sprint 1 está implementada con las decisiones funcionales autorizadas. No se declara aceptación visual completa de HU-009 C3: la comprobación interactiva de 320–1920 px está no verificada por indisponibilidad del host de navegador. La confianza de certificado para un entorno real y el despliegue no se ejecutaron. Estos límites no se ocultan como pruebas aprobadas.

Se mantuvieron las asignaciones del CSV y todos los cambios locales previos. Sin commits, push ni despliegues.

## Dependencias transversales

La cobertura de T-001 a T-012, ubicadas actualmente en Sprint 0 por el CSV, se detalla en [arquitectura y entornos](../documentacion/sprint-1-equipo/arquitectura-y-entornos.md). Incluye pipeline local preparado, contratos, validador de claves comunes, diccionario de once tablas y modelo E-R. El diseño global de módulos posteriores, Figma, la ejecución remota de CI y la aceptación formal conservan sus límites explícitos.
