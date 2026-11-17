# Verificación del Sprint 1

Última ejecución observada: 15 de noviembre de 2026, durante el análisis del proyecto anterior a esta limpieza documental. Se reejecutaron las suites sobre el código del repositorio. El backend creó y destruyó una base aislada test_*; no se recreó la base de trabajo.

| Comando | Resultado |
| --- | --- |
| backend/venv/Scripts/python.exe manage.py test --noinput, desde backend | 135 pruebas aprobadas, 32.154 s; comprobación Django sin incidencias |
| npm test, desde frontend | 20 pruebas aprobadas en cinco archivos, 6.45 s |
| npm run lint | Salida 0; 14 advertencias anteriores de Fast Refresh |
| npm run build | Correcto; 58 módulos, 1.23 s |

La matriz enlaza las pruebas de registro y concurrencia, hash, consentimiento, padrón, conversión, bloqueo, auditoría, roles, revocación, refresh, inactividad y carreras de sesión en interfaz. Los mensajes de errores inyectados en algunas pruebas no fueron fallos de la suite: terminó en OK.

## HTTPS: evidencia anterior

La verificación del 10 de noviembre comprobó HTTPS real en loopback con cadena y hostname validados: página/login/perfil 200, logout 204, reutilización de access y refresh 401 e inactividad 401. Se utilizó una base demo separada y confianza limitada al cliente de pruebas; no se instaló confianza en Windows ni se omitió TLS. Esta prueba no se reejecutó el 15 de noviembre ni durante la depuración. Su configuración y explicación se conservan en [operación](operacion.md).

## Límites de aceptación

La geometría visual entre 320 y 1920 px no se verificó: no estuvo disponible el host del navegador. Las pruebas DOM no sustituyen esa revisión. Tampoco acreditan WCAG completa, carga de 500 usuarios, disponibilidad de meses, SMTP real ni integración institucional. El workflow de CI se preparó, pero no se acredita aquí ejecución remota. La aceptación del docente y los estados de Jira son externos a estos resultados.

## Revision de nombres y arquitectura del 16/11/2026

La refactorizacion a clases de servicio y el tipado de firmas superaron de nuevo 135 pruebas backend, en 25.533 s, con `manage.py test apps.usuarios --noinput`. Se creo y destruyo una base test_*; Django no reporto incidencias. No se modificaron rutas ni contratos JSON de la API. Las pruebas frontend, lint y build conservan la ejecucion del 15/11: no se reejecutaron por esta revision de backend. Se verifico por AST la correspondencia de 28 tipos propios y por relectura API los nombres, atributos, operaciones y parametros del modelo. Los elementos Planificado no se cuentan como codigo implementado.
