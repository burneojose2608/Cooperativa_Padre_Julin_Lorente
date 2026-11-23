# Modelo de datos de juegos-retos

Tablas y atributos principales: juego, partida, reto, progreso_reto, actividad_validada.

El cliente envía índices de respuestas; el servidor conserva la configuración y calcula el resultado. Un inicio consume un intento. Los retos cuentan actividades validadas dentro de su vigencia y acreditan una recompensa única.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.
