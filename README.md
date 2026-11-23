# Cooperativa_Padre_Julin_Lorente

La [evolución de la plataforma del 20 de noviembre](documentacion/EVOLUCION-PLATAFORMA.md)
incorpora los módulos de referidos, campañas, puntos, formación, sorteos, canjes,
juegos, comunidad, bienestar y reportes. El [índice de especificaciones](specs/README.md)
conserva las historias, subtareas, tareas técnicas y sprints originales.
La guía distingue implementación comprobada y aceptación integral pendiente.

La base existente se actualiza con `python backend/manage.py actualizar_plataforma`
después del Sprint 2; no se repiten los scripts de instalación inicial.
El trabajador `procesar_notificaciones --continuo --mantenimiento` procesa avisos y
confirmaciones, mantiene prospectos y puede generar respaldos diarios con `PG_DUMP_BIN` configurado.

La [entrega del Sprint 2](documentacion/entregable/sprint-2/LEEME-SPRINT-2.md) incorpora
perfil y contraseña, administración de cuentas y permisos, código de referido,
reglas de puntos, contenidos, materiales privados y notificaciones asíncronas.
Incluye instrucciones de ejecución y trazabilidad de sus 11 historias y 6 subtareas.

La [entrega del Sprint 1 completo](documentacion/entregable/sprint-1/LEEME-SPRINT-1.md) incluye
registro, autenticación, roles, revocación de sesiones e inactividad, con matriz
de trazabilidad, pruebas y configuración HTTPS. La documentación se consolidó para la revisión del ingeniero; los antecedentes
completos quedaron en el respaldo externo de la depuración.

## Base de datos local

El backend usa PostgreSQL en `localhost:5433`, base `cooperativa_db`, esquema
`public`. El puerto `5432` queda disponible para el contenedor del otro proyecto.
Configura los mismos valores en `backend/.env`, pgAdmin y DataGrip.

Para una instalación nueva, crea una base vacía llamada `cooperativa_db` y abre
una consola conectada a esa base. Comprueba la conexión antes de ejecutar SQL:

```sql
SELECT current_database(), inet_server_port(), current_schema();
```

Ejecuta una sola vez y en este orden los archivos de `backend/sql/`:

1. `01_base_datos_cooperativa.sql`
2. `02_ajustes_recomendados.sql`
3. `03_recuperacion_clave.sql`
4. `04_cedula_solo_diez_digitos.sql`
5. `05_registro_padron_unicidad.sql`
6. `06_cedula_formato_acordado.sql`
7. `07_sprint_2.sql`

Los scripts preparan el esquema y 5 roles iniciales, sin usuarios registrados.
Los scripts rechazan la base administrativa `postgres` y las bases plantilla.
No los vuelvas a ejecutar sobre tablas existentes.

Si ya tienes instalados 01-06, aplica exclusivamente el cambio aditivo del Sprint 2:
`.\.venv\Scripts\python.exe backend/manage.py actualizar_sprint2`.
Conserva las cuentas existentes y los permisos configurados. La recuperación de
contraseña muestra el código en la consola del backend, según la modalidad temporal
de práctica. Las notificaciones se procesan con `procesar_notificaciones --continuo`
en otra terminal.

Si ya instalaste 01–04, aplica únicamente 05 y 06; si ya instalaste 05, aplica
únicamente 06. Estos cambios conservan las cuentas existentes. La cédula exige
solo diez dígitos del 0 al 9, sin provincia ni verificador. Una cédula ausente
del padrón permite crear una cuenta general; únicamente un socio activo obtiene
el rol Socio. La tabla del padrón debe existir para que el registro funcione.
Consulta [la documentación del registro](documentacion/entregable/sprint-1/LEEME-SPRINT-1.md).

El [cierre de Valeria para Sprint 1](documentacion/entregable/sprint-1/matriz-trazabilidad.md)
incluye la matriz de aceptación y los diagramas exportados de esta entrega.

Para convertir una cuenta general existente, el administrador dispone de
**Administración → Validar socios**. Es un proceso manual temporal con confirmación
y auditoría; conserva usuario y contraseña. Consulta las
[reglas, pruebas y forma de deshabilitarlo](documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md).

En DataGrip, selecciona `cooperativa_db` como Database en las propiedades de la
conexión y habilita su esquema `public` en Schemas. Después sincroniza la conexión.
Refrescar una conexión a `postgres` no muestra las tablas de `cooperativa_db`.
