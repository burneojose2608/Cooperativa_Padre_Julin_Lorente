# Modelo de datos de notificaciones

Tablas y atributos principales: plantilla_notificacion, preferencia_notificacion, notificacion, envio_notificacion.

Cola duradera, reserva de trabajador, preferencias por evento y canal y hasta tres reintentos. Cambio de contraseña y validación de socio son comunicaciones obligatorias. Las plantillas por canal pueden usar {mensaje}. El correo tiene semántica al menos una vez.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.
