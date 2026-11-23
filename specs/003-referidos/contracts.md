# Contratos de referidos

Planificación original: Sprint 2 y Sprint 3.

## API

- `/api/plataforma/negocio/referidos/`.
- `/api/plataforma/negocio/referidos/{id}/estado/`.
- `/api/plataforma/referidos/codigo/`.
- `/api/plataforma/invitaciones/{codigo}/referir/`.
- `/api/plataforma/referidos/confirmar/{token}/`.

## Implementación

- Dominio y API: `backend/apps/plataforma/negocio.py`.
- Pantallas: `frontend/src/panel/negocio/Modulos.jsx`.

Las escrituras validan los campos admitidos y la autorización en servidor. Los catálogos separan gestión y consulta del socio. Las acciones usan POST y los datos de negocio se calculan desde el servidor. Los rechazos de validación responden 400; la sesión ausente o inválida, 401; la falta de permisos, 403; el objeto inaccesible, 404.

El registro público toma el código de la ruta y responde 429 al exceder su límite. El listado de gestión requiere permiso de Referidos y habilita los datos completos después de la confirmación. El listado del socio siempre aplica titularidad y enmascaramiento.

Las pruebas backend están en `backend/apps/usuarios/tests` y `backend/apps/plataforma/tests`; las pruebas de las nuevas pantallas están en `frontend/src/panel/negocio/negocio.test.jsx`. La aceptación completa por criterio y la revisión visual se registran separadamente de la existencia del código.
