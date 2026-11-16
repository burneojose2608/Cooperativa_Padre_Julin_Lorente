# Cooperativa_Padre_Julin_Lorente

La [entrega del Sprint 1 completo](documentacion/sprint-1-equipo/README.md) incluye
registro, autenticación, roles, revocación de sesiones e inactividad, con matriz
de trazabilidad, pruebas y configuración HTTPS. El cierre anterior de Valeria se
conserva como antecedente de la implementación de registro.

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

Los scripts preparan el esquema y 5 roles iniciales, sin usuarios registrados.
Los scripts rechazan la base administrativa `postgres` y las bases plantilla.
No los vuelvas a ejecutar sobre tablas existentes.

Si ya instalaste 01–04, aplica únicamente 05 y 06; si ya instalaste 05, aplica
únicamente 06. Estos cambios conservan las cuentas existentes. La cédula exige
solo diez dígitos del 0 al 9, sin provincia ni verificador. Una cédula ausente
del padrón permite crear una cuenta general; únicamente un socio activo obtiene
el rol Socio. La tabla del padrón debe existir para que el registro funcione.
Consulta [la documentación del registro](documentacion/sprint-1-valeria/README.md).

El [cierre de Valeria para Sprint 1](documentacion/sprint-1-valeria/cierre-valeria-sprint-1.md)
incluye la matriz de aceptación y los diagramas exportados de esta entrega.

Para convertir una cuenta general existente, el administrador dispone de
**Administración → Validar socios**. Es un proceso manual temporal con confirmación
y auditoría; conserva usuario y contraseña. Consulta las
[reglas, pruebas y forma de deshabilitarlo](documentacion/sprint-1-valeria/conversion-administrativa-temporal.md).

En DataGrip, selecciona `cooperativa_db` como Database en las propiedades de la
conexión y habilita su esquema `public` en Schemas. Después sincroniza la conexión.
Refrescar una conexión a `postgres` no muestra las tablas de `cooperativa_db`.
