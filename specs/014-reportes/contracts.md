# Contratos de reportes

Planificación original: Sprint 4 y Sprint 5.

## API

- `/api/plataforma/negocio/reportes/?tipo={general|referidos|social|gamificacion}&desde=AAAA-MM-DD&hasta=AAAA-MM-DD&formato={json|csv|pdf}`.

## Implementación

- Dominio y API: `backend/apps/plataforma/api_reportes.py`.
- Pantallas: `frontend/src/panel/negocio/Modulos.jsx`.

Las escrituras validan los campos admitidos y la autorización en servidor. Los catálogos separan gestión y consulta del socio. Las acciones usan POST y los datos de negocio se calculan desde el servidor. Los rechazos de validación responden 400; la sesión ausente o inválida, 401; la falta de permisos, 403; el objeto inaccesible, 404.

Las pruebas backend están en `backend/apps/usuarios/tests` y `backend/apps/plataforma/tests`; las pruebas de las nuevas pantallas están en `frontend/src/panel/negocio/negocio.test.jsx`. La aceptación completa por criterio y la revisión visual se registran separadamente de la existencia del código.
