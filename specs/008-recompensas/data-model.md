# Modelo de datos de recompensas

Tablas y atributos principales: beneficio, canje, movimiento_puntos, historial_estado.

Reservar bloquea socio y beneficio, verifica saldo, stock y convenio y conserva el costo de la solicitud. Aprobar libera la reserva y registra el descuento, sin descontar dos veces; rechazar libera puntos y stock. La entrega conserva fecha y responsable.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.

- **`Canje.clave`**. UUID opcional en el esquema. El índice `uq_canje_clave` hace única la clave por socio cuando está presente, según `backend/sql/08_alcance_completo.sql`.
