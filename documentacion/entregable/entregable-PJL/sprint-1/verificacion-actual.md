# Verificación actual del Sprint 1

Ejecutada el 10 de noviembre de 2026 sobre el código entregado. La suite backend creó y destruyó su base aislada `test_*`; no se ejecutaron migraciones manuales sobre la base de trabajo.

| Comando | Resultado |
| --- | --- |
| backend/venv/Scripts/python.exe manage.py test --noinput | 135 pruebas aprobadas en 30.953 s; comprobación Django sin incidencias |
| npm test | 20 pruebas aprobadas, cinco archivos, 4.45 s |
| npm run lint | Salida 0; 14 advertencias preexistentes de Fast Refresh |
| npm run build | Correcto; 58 módulos; 744 ms |

Los logs de fallos inyectados en tests no equivalen a tests fallidos. La evidencia previa de HTTPS se incluye en documentacion-equipo/verificacion.md; no se presenta como una prueba TLS reejecutada ahora. No se certifica cobertura completa de RNF por pasar estas suites.

El CSV de planificación mantiene sus estados originales. No se cambiaron tareas en Jira ni se declara terminado un sprint remoto sin verificarlo. Registro y acceso cubren el alcance vigente; las diferencias respecto a la plantilla histórica se explican en CAMBIOS-DE-LINEA-BASE.md.
