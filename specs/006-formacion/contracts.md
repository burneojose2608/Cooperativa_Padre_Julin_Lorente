# Contratos de formacion

Planificación original: Sprint 3 a Sprint 5.

## API

- `/api/plataforma/negocio/capacitaciones/`.
- `/api/plataforma/negocio/talleres/`.
- `/api/plataforma/negocio/mis-actividades/`.
- `/api/plataforma/negocio/certificados/{id}/pdf/`.
- `/api/plataforma/certificados/verificar/{codigo}/`.
- `GET /api/plataforma/negocio/capacitaciones/{id}/aula/` devuelve `porcentaje_avance` (entero de 0 a 100), módulos con material, preguntas sin clave de respuesta y los intentos restantes.
- `GET /api/plataforma/materiales/{id}/archivo/` exige rol de Socio, validación, permiso de Formación e inscripción en un curso publicado para el acceso por aula. Ante falta de acceso al material privado responde 404.

## Implementación

- Dominio y API: `backend/apps/plataforma/negocio.py`.
- Pantallas: `frontend/src/panel/negocio/Modulos.jsx`.

Las escrituras validan los campos admitidos y la autorización en servidor. Los catálogos separan gestión y consulta del socio. Las acciones usan POST y los datos de negocio se calculan desde el servidor. Los rechazos de validación responden 400; la sesión ausente o inválida, 401; la falta de permisos, 403; el objeto inaccesible, 404.

Las pruebas backend están en `backend/apps/usuarios/tests` y `backend/apps/plataforma/tests`; las pruebas de las nuevas pantallas están en `frontend/src/panel/negocio/negocio.test.jsx`. La aceptación completa por criterio y la revisión visual se registran separadamente de la existencia del código.
