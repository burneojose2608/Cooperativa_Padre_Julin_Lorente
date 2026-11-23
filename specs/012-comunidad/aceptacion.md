# Aceptación técnica local de Comunidad e interacción social

Verificación local del módulo y del recorrido integrado T-043 de Comunidad con datos sintéticos en PostgreSQL aislado (`test_`), almacenamiento temporal privado, el cliente HTTP de Django y Vitest con jsdom.

| Historia y trazabilidad | Resultado por criterio | Código y evidencia ejecutable |
| --- | --- | --- |
| HU-079 · RF-12-1 · UR-52 · RNF-20, RNF-26 · CU-G12 | 1. El socio habilitado publica texto (hasta 10 000 caracteres) e imagen opcional. 2. Solo socios autenticados, validados y con permiso activo consultan publicaciones e imágenes (anónimos reciben 401; cuentas generales sin rol Socio reciben 403). 3. Las imágenes se validan por firma binaria real (PNG, JPEG, WebP), extensión y tamaño `<= 10 MB`, se almacenan fuera del directorio público y se descargan con `Cache-Control: private, no-store` y `X-Content-Type-Options: nosniff`. | `ComunidadView`, `ImagenComunidadView`, `guardar_archivo`, `Comunidad.jsx`. `test_comunidad_privacidad_reaccion_reporte_moderacion` y `test_comunidad_foto_privada_y_reporte_de_comentario`. |
| HU-080 · RF-12-2 · UR-52 · RNF-20 · CU-G12 | 1. Los socios reaccionan (`ME_GUSTA`, `APOYO`, `CELEBRO`, con unicidad por usuario y publicación mediante `update_or_create` y `uq_reaccion`) y comentan publicaciones visibles. 2. Tanto publicaciones como comentarios se renderizan con escape en React sin ejecutar HTML ni scripts (XSS). 3. Una publicación oculta o eliminada por moderación responde 404 ante intentos de comentar, reaccionar o descargar su imagen. | `InteraccionView`, `Comunidad.jsx`. `test_comunidad_privacidad_reaccion_reporte_moderacion` y `negocio.test.jsx` («la comunidad presenta texto escapado y no ejecuta etiquetas del usuario»). |
| HU-081 · RF-12-3 · UR-52 · RNF-06 · CU-G12 | 1. Un socio reporta una publicación o un comentario visible indicando el motivo obligatorio. 2. El reporte se registra como pendiente en la cola de moderación (`resuelto_en=None`). 3. Se persisten el usuario reportante (`usuario_id`), el contenido afectado y la fecha (`creado_en`). | `InteraccionView` (`reportar`), `ReporteComunidad`, `Comunidad.jsx`. `test_comunidad_privacidad_reaccion_reporte_moderacion` y `test_comunidad_foto_privada_y_reporte_de_comentario`. |
| HU-082 · RF-12-4 · UR-53 · RNF-06, RNF-14 · CU-G24 | 1. El Gestor de contenidos y el Administrador consultan la cola de reportes pendientes (un socio recibe 403). 2. Pueden `OCULTAR`, `ELIMINAR` o `DESCARTAR` la publicación o comentario reportado y aplicar `suspension_dias` temporal al autor en `SuspensionComunidad`, bloqueando nuevas publicaciones e interacciones mientras dure la suspensión. 3. La resolución exige motivo obligatorio (sin motivo responde 400), impide resolver dos veces el mismo reporte (responde 404) y registra el motivo en `ReporteComunidad.resolucion` y en auditoría (`MODERAR_COMUNIDAD`). | `ModeracionView`, `comunidad_habilitada`, `Moderacion` en `Comunidad.jsx`. `test_comunidad_privacidad_reaccion_reporte_moderacion` y `test_comunidad_foto_privada_y_reporte_de_comentario`. |
| HU-083 · RF-12-5 · UR-52 · RNF-14 · CU-G12 | 1. El socio configura su `alias` (hasta 60 caracteres) y su preferencia de aparición en la clasificación pública (`ranking_publico`). 2. Por defecto la información personal está oculta (`alias=''` que se presenta como `'Socio'` y `ranking_publico=False`). 3. Las respuestas de comunidad y comentarios solo incluyen `alias`, texto y fecha, sin exponer `usuario`, cédula, correo ni teléfono. | `PerfilPublicoView`, `alias`, `publicacion_datos`, `PerfilPublico` en `Comunidad.jsx`. `test_comunidad_privacidad_reaccion_reporte_moderacion` y `test_ranking_opt_in_y_reportes_por_rol_y_exportacion`. |

## Pendientes externos

- Revisión visual mobile-first en navegadores reales (RNF-03).

## Ajuste visual del muro

Los comentarios muestran la foto de perfil de su autor o la inicial si no tiene foto. La API exige permiso de Comunidad y que tanto el comentario como la publicación sigan visibles (HU-080, HU-083, RF-12-2, RF-12-5, UR-52, RNF-14, CU-G12).

En los comentarios, el alias elegido tiene prioridad y, si falta, se muestra el primer nombre del autor. La prueba de integración verifica ambos casos sin añadir apellidos ni datos de cuenta a la respuesta (HU-080, HU-083, RF-12-2, RF-12-5, UR-52, RNF-14, CU-G12).

La foto de perfil del autor se consulta usando el identificador de la publicación visible y el permiso de Comunidad. El muro conserva el alias y muestra la inicial si la foto falta (HU-079 y HU-083). La API no expone el identificador de la cuenta ni la ruta del archivo.

Las imágenes adjuntas se muestran en la publicación mediante la API autenticada y se sirven con disposición `inline`, sin acción de descarga en el muro (HU-079, RF-12-1, UR-52, RNF-20, RNF-26, CU-G12). Se conservan el almacenamiento privado, las comprobaciones de permisos y moderación, y la política `private, no-store`.

El muro presenta un formulario compacto, tarjetas por publicación, hilos desplegables y reportes dentro de la publicación correspondiente (HU-079, HU-080 y HU-081, con la trazabilidad de la tabla). Vitest confirmó el escape del contenido y el envío del identificador del comentario y el motivo al reportar desde su hilo. Pasaron 67 pruebas de frontend y la compilación.
