# Entrega de Valeria Chuncho para Sprint 1

Este es el cierre parcial de Valeria. La revisión posterior del [Sprint 1 completo del equipo](../sprint-1-equipo/README.md) implementa también los pendientes de autenticación, logout, inactividad y unión de roles. Su matriz y resultados tienen prioridad para evaluar el estado actual del sprint completo.

Estado consolidado al 10 de noviembre: **108 pruebas aprobadas**, registro y conversión con reintentos seguros del código de socio, validación y errores reforzados, y cuatro diagramas exportados. El [cierre vigente](cierre-valeria-sprint-1.md) distingue esta entrega de las asignaciones posteriores de Valeria y del resto del Sprint 1 del equipo.

Esta entrega implementa la validación de socio activo HU-006 y la prevención de duplicados HU-008, subtareas de HU-001. Por decisiones posteriores del usuario del 9 de noviembre, la cédula solo exige diez dígitos y quien no consta en el padrón puede crear una cuenta general sin permisos de socio. Para resolver el 503 en la aplicación habitual, se aplicó el esquema 05/06 a la base local conservando las cuentas y sus datos. No se realizaron commits ni publicaciones.

## Documentos de revisión

- [Cierre de Valeria en Sprint 1 y evidencia por requisito](cierre-valeria-sprint-1.md).
- [Diagramas de clases, registro, login y conversión en SVG](diagramas/README.md).
- [Proceso temporal para validar y convertir cuentas a socio desde Administración](conversion-administrativa-temporal.md).
- [Regla vigente de diez dígitos y corrección del 503 en la aplicación habitual](decision-cedula-diez-digitos.md).
- [Regla vigente de registro general y socio, con pruebas](decision-registro-general.md).
- [Demostración local lista para probar y diagnóstico del bloqueo](demo-local.md).
- [Plan, inventario, decisiones y fases](../../docs/plan-valeria-sprint-1.md).
- [Arquitectura, contrato HTTP y diagramas](arquitectura-y-contrato.md).
- [Preparación, SQL, pruebas y matriz de trazabilidad](operacion-y-verificacion.md).
- [Encargo original conservado](../../docs/encargo-valeria-sprint-1.txt).
- Fuente de requisitos: `../product_con_subtareas.csv`, filas 101, 106, 108, 304, 307, 311 y 312. El estado del CSV no fue modificado.

## Alcance por responsable

| Elemento | Resultado de esta entrega | Coordinación |
| --- | --- | --- |
| HU-006, Valeria | Padrón independiente; solo activos obtienen rol Socio; ausentes crean cuenta general | Regla ajustada por decisión posterior del usuario |
| HU-008, Valeria | Comprobaciones normalizadas y unicidad SQL, incluidas carreras | Integrada en HU-001 |
| HU-001, responsable principal del CSV | Verificador, consentimiento y Argon2id como dependencias de integración | No implica cerrar toda la historia principal |
| T-007 | Validación y errores seguros del registro | Cobertura acotada a este flujo |
| T-004 | Clases y secuencia del registro | Otros módulos y secuencias continúan pendientes de sus responsables |
| T-011 y T-012, Jefferson Paredes | Mínimo de tabla, índices, reversión y padrón sintético | Revisar e integrar con entregables generales de BD |

Los documentos Word originales permanecen sin cambios. No se incorporan integraciones institucionales ni datos de socios reales.
