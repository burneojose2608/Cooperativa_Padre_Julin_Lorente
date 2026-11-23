# Modelo de datos de autenticacion

Tablas y atributos principales: sesion, token_recuperacion, auditoria.

Access y refresh ligados a sesión revocable; roles y permisos consultados en cada solicitud.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.

- **`TokenRecuperacion.token_hash`**. Huella única de hasta 64 caracteres, según `backend/apps/usuarios/models/token_recuperacion.py`.

- **`Sesion.revocada_en`**. Fecha opcional. Una sesión revocada impide reutilizar sus tokens, según `backend/apps/usuarios/models/sesion.py` y el servicio de sesiones.
