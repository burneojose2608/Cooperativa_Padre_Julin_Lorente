# Modelo de datos de referidos

Tablas y atributos principales: codigo_referido, prospecto, referido, conversion, historial_estado.

Código persistente del socio, consentimiento versionado, confirmación de un solo uso, primer contacto, ciclo controlado y conversión única. Los datos se enmascaran para el socio.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.

- **`Conversion.referido`**. Identifica un referido de forma única, según `backend/apps/plataforma/models_negocio.py`.
