# Modelo de datos de gamificacion

Tablas y atributos principales: actividad_validada, regla_puntos, movimiento_puntos, nivel, insignia, socio_insignia.

Libro inmutable. Disponible = acreditaciones + liberaciones - reservas - descuentos - reversos. Los puntos de logro excluyen canjes. Un origen se valida y acredita una sola vez, con límite por período. Reverso justificado sin saldo negativo.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.

- **`Nivel.umbral_puntos`**. Entero único, según `backend/apps/plataforma/models_negocio.py`.
