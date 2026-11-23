# Contratos de usuarios

Planificación original: Sprint 1 y Sprint 2.

## API

- `/api/auth/yo/`.
- `/api/administracion/`.

## Implementación

- Dominio y API: `backend/apps/usuarios/services/gestion_cuentas_service.py`.
- Pantallas: `frontend/src/panel/sprint2/Usuarios.jsx`.

Las escrituras validan los campos admitidos y la autorización en servidor. Los catálogos separan gestión y consulta del socio. Las acciones usan POST y los datos de negocio se calculan desde el servidor. Los rechazos de validación responden 400; la sesión ausente o inválida, 401; la falta de permisos, 403; el objeto inaccesible, 404.

Las pruebas backend están en `backend/apps/usuarios/tests` y `backend/apps/plataforma/tests`; las pruebas de las nuevas pantallas están en `frontend/src/panel/negocio/negocio.test.jsx`. La aceptación completa por criterio y la revisión visual se registran separadamente de la existencia del código.
