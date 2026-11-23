# Modelo de datos de sorteos

Tablas y atributos principales: sorteo, participacion_sorteo, ganador.

Participaciones desde actividades validadas y campañas elegibles. La ejecución congela candidatos y SHA-256, usa secrets y conserva ganadores y suplentes; un socio recibe como máximo un premio por sorteo. La evidencia completa se restringe al personal.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.
