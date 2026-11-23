# Constitución del proyecto de la cooperativa

Versión 1.0.0. Adoptada el 20/11/2026 a partir de la solicitud del usuario y las reglas vigentes del repositorio.

## Propósito y alcance

Desarrollar la plataforma de referidos y gamificación definida por los 14 módulos del backlog,
conservando historias, subtareas, sprints y trazabilidad. Los cambios de negocio se registran
con su origen y efecto sobre los criterios. La aprobación institucional o académica requiere evidencia propia.

## Reglas de desarrollo

1. Especificar las funcionalidades y sus criterios antes de implementarlas. Mantener vinculados
   HU, RF, UR, RNF, CU, código y verificaciones; preservar el backlog original y los GUID de EA.
2. Mantener el monolito modular React, Django REST Framework y PostgreSQL. Reutilizar sus
   servicios, repositorios, API, cliente autenticado y convenciones antes de añadir infraestructura.
3. Comprobar autenticación, rol, permiso y pertenencia en servidor. Aplicar privacidad por defecto,
   enmascarar datos en vistas compartidas y validar archivos antes de almacenarlos de forma privada.
4. Registrar puntos como movimientos inmutables. Calcular importes y resultados en servidor,
   usar transacciones y bloqueos para saldo, cupo y stock y claves de origen para idempotencia.
5. Actualizar bases existentes mediante cambios aditivos y repetibles. Verificar con datos sintéticos
   en bases test_* y conservar las cuentas, registros y permisos previamente configurados.
6. Probar criterios de aceptación y rechazos relevantes. Registrar evidencia actual y distinguirla
   de resultados históricos, simulaciones, integraciones externas y mediciones aún pendientes.
7. Conservar las decisiones explícitas vigentes sobre cédula de diez dígitos, padrón de prueba,
   habilitación administrativa temporal de socios y recuperación por consola. Documentar su sustitución
   cuando la cooperativa defina las reglas definitivas.

## Cambios y entrega

Actualizar especificaciones, código, pruebas y documentación conjuntamente. La implementación
por adelantado de un sprint conserva su planificación original y registra el avance real por separado.
La interfaz debe usar datos del servidor y presentar errores y estados vacíos comprensibles.
Las revisiones de carga, accesibilidad, integración institucional, SMTP y despliegue se certifican
únicamente con las verificaciones correspondientes. No publicar secretos ni hacer push o despliegue sin autorización.

## Gestión de esta constitución

Todo cambio debe indicar versión, fecha, regla afectada y motivo. Las instrucciones explícitas
del usuario tienen precedencia. Los criterios contradictorios se concilian con sus fuentes antes
de dar por cerrada la funcionalidad; no se rellenan decisiones institucionales con supuestos ocultos.
