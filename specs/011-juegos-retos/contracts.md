# Contratos de juegos-retos

Planificación original: Sprint 4 y Sprint 5.

## API

- `/api/plataforma/negocio/juegos/`.
- `/api/plataforma/negocio/juegos/{id}/iniciar/`.
- `/api/plataforma/negocio/partidas/{id}/finalizar/`.
- `/api/plataforma/negocio/retos/`.

## Implementación

- Dominio y API: `backend/apps/plataforma/negocio.py`.
- Pantallas: `frontend/src/panel/negocio/Modulos.jsx`.

Las escrituras validan los campos admitidos y la autorización en servidor. Los catálogos separan gestión y consulta del socio. Las acciones usan POST y los datos de negocio se calculan desde el servidor. Los rechazos de validación responden 400; la sesión ausente o inválida, 401; la falta de permisos, 403; el objeto inaccesible, 404.

Las pruebas backend están en `backend/apps/usuarios/tests` y `backend/apps/plataforma/tests`; las pruebas de las nuevas pantallas están en `frontend/src/panel/negocio/negocio.test.jsx`. La aceptación completa por criterio y la revisión visual se registran separadamente de la existencia del código.
