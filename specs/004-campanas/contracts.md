# Contratos de campanas

Planificación original: Sprint 3 y Sprint 4.

## API

- `/api/plataforma/negocio/campanas/`.
- `/api/plataforma/negocio/gastos/`.
- `/api/plataforma/negocio/segmentos/{socio}/`.

## Implementación

- Dominio y API: `backend/apps/plataforma/api_negocio.py`.
- Pantallas: `frontend/src/panel/negocio/Modulos.jsx`.

Las escrituras validan los campos admitidos y la autorización en servidor. Los catálogos separan gestión y consulta del socio. Las acciones usan POST y los datos de negocio se calculan desde el servidor. Los rechazos de validación responden 400; la sesión ausente o inválida, 401; la falta de permisos, 403; el objeto inaccesible, 404.

Las pruebas backend están en `backend/apps/usuarios/tests` y `backend/apps/plataforma/tests`; las pruebas de las nuevas pantallas están en `frontend/src/panel/negocio/negocio.test.jsx`. La aceptación completa por criterio y la revisión visual se registran separadamente de la existencia del código.
