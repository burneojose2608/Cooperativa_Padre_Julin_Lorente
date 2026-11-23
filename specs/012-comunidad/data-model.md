# Modelo de datos de comunidad

Tablas y atributos principales: publicacion, comentario, reaccion, reporte_comunidad, suspension_comunidad, socio.alias.

Comunidad solo para socios; alias y ranking público desactivado por defecto. El texto se muestra con escape de React. Los reportes se resuelven con motivo y permiten ocultar, retirar o suspender temporalmente la participación.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.
