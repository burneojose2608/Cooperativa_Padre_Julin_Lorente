# Plan de campañas e incentivos

## Arquitectura

Mantener React y su cliente HTTP autenticado, Django REST Framework y PostgreSQL. Reutilizar
usuarios, sesiones, permisos, auditoría, archivos privados y cola de notificaciones existentes.
El dominio se implementa en servicios, con validación explícita en los límites de la API.

## Flujo del módulo

Borrador → segmentación → activación → consulta elegible → resultados.

Probar vigencia y elegibilidad con socios dentro y fuera del segmento. Conservar historial y reglas aplicables tras activar. Reportes consume conversiones y gastos confirmados.

Puntos de entrada documentados: [`api_negocio.py`](../../backend/apps/plataforma/api_negocio.py), [`Modulos.jsx`](../../frontend/src/panel/negocio/Modulos.jsx), [`negocio.test.jsx`](../../frontend/src/panel/negocio/negocio.test.jsx). Consultar los [contratos](contracts.md) y el [modelo](data-model.md).

## Datos y compatibilidad

Reutilizar las tablas del SQL inicial y sus nombres físicos. Añadir columnas y restricciones
mediante scripts transaccionales repetibles y un comando de actualización; probar en base test_*.
Conservar los registros existentes y las asignaciones de permisos revocadas. Ninguna operación
de interfaz ejecuta los scripts de instalación inicial.

## Contratos y seguridad

Documentar rutas y campos en los serializadores y la guía operativa. Separar consulta propia,
catálogo visible y gestión autorizada. El servidor calcula puntuaciones, saldos y elegibilidad;
los identificadores del cliente nunca deciden el titular ni el importe de una recompensa.
Bloquear los agregados que compiten por saldo, cupo, stock o cambios de estado. Las operaciones
repetidas conservan un resultado único por actividad de origen.

## Dependencias y orden

Respetar los RF de dependencia incluidos en spec.md y los sprints originales. La base común
es identidad y permisos, seguida de campañas y referidos, libro de puntos y formación;
los canjes, sorteos, juegos y reportes consumen esas actividades validadas.

## Verificación

Cubrir los criterios de cada HU, incluyendo las subtareas consolidadas. Ejecutar pruebas backend
en PostgreSQL aislado, pruebas de interfaz, lint y build. Registrar los comandos y resultados
actuales y las limitaciones de integraciones, revisión visual, carga y despliegue.

Evidencia de referencia: test_alcance_completo.py, escenarios de segmentación e indicadores. Registrar los criterios comprobados en [tareas](tasks.md) y los resultados en la evidencia de aceptación del módulo.

RNF de este módulo: RNF-03, RNF-04, RNF-05, RNF-06, RNF-08, RNF-09, RNF-10, RNF-15, RNF-19, RNF-20, RNF-23. Vincular los resultados con la [verificación transversal](../000-plataforma/tasks.md#verificación-transversal-de-rnf).
