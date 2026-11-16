# Preparación y verificación de Sprint 1

Evidencia vigente del 10 de noviembre: [108 pruebas y cierre por requisito](cierre-valeria-sprint-1.md). La creación de socio incluye reintentos selectivos por colisión de código y los errores no previstos registran solo el tipo, sin SQL ni datos de petición.

Última regla: [cédula de diez dígitos sin verificador y solución del 503](decision-cedula-diez-digitos.md). SQL 05/06 ya se aplicaron al esquema de la base local original conservando sus cuentas; los apartados históricos que indicaban solo pruebas aisladas describen el estado anterior. Las instalaciones nuevas deben ejecutar 01–06.

La [regla vigente de registro](decision-registro-general.md) admite cuentas generales para cédulas válidas ausentes del padrón. Solo los socios activos reciben rol Socio. Esta ampliación usa el mismo esquema SQL 05 y no requiere nuevas migraciones. La tabla del padrón debe existir y poder consultarse en ambos casos: un fallo de infraestructura nunca equivale a una cédula ausente.

## Entorno y protección de datos

La implementación se verificó en Windows con el entorno virtual existente `backend/venv`, Django 6.1.2 y PostgreSQL real. No se mostró ni modificó `.env`. Se instaló `argon2-cffi==25.1.0` en ese entorno y se agregó a requirements, cuyo formato se normalizó de UTF-16 a UTF-8.

Los comandos siguientes se ejecutan desde la raíz del repositorio, en PowerShell. Se necesita un PostgreSQL accesible y una cuenta con permiso para crear la base de pruebas. Las credenciales se configuran localmente según `.env.example`; no deben copiarse en documentos ni comandos compartidos.

```powershell
& .\backend\venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
Push-Location backend
& .\venv\Scripts\python.exe manage.py check
& .\venv\Scripts\python.exe manage.py test --noinput
Pop-Location
Push-Location frontend
npm.cmd run lint
npm.cmd run build
Pop-Location
```

El runner crea `test_<DB_NAME>`, carga SQL 01–05 y elimina esa base al terminar. Valida el prefijo `test_` antes de preparar la base, incluso si alguien configura `TEST.NAME`. Las pruebas de concurrencia y reversión también comprueban este prefijo. No usar `--keepdb`: estos scripts iniciales crean tablas y no son idempotentes. `--noinput` puede reemplazar una base de pruebas previa; debe reservarse este nombre para pruebas desechables.

## Preparar una demostración aislada

1. Crear manualmente una base vacía `sprint1_valeria` con la cuenta local autorizada. No recrear ni eliminar `cooperativa_db`.
2. Conectarse a esa base en pgAdmin/DataGrip y comprobar `SELECT current_database(), inet_server_port(), current_schema();`.
3. Ejecutar en orden SQL 01, 02, 03, 04, 05 y 06 de backend/sql. En una instalación que ya tiene 01–04, aplicar solamente 05 y 06 después de revisar conflictos. Si ya tenía SQL 05, ejecutar solo 06.
4. En la terminal del backend, seleccionar temporalmente esa base y cargar los datos:

```powershell
$env:DB_NAME = 'sprint1_valeria'
& .\venv\Scripts\python.exe manage.py cargar_padron_sintetico
& .\venv\Scripts\python.exe manage.py runserver
```

5. En otra terminal, ejecutar `npm.cmd run dev` en frontend. El cliente usa el backend local configurado en su entorno.
6. Al terminar la demostración y detener el servidor, ejecutar `Remove-Item Env:DB_NAME` para retirar la selección temporal de la terminal. Este procedimiento no modifica `.env`.

El comando de carga solo admite bases con prefijo `test_` o `sprint1_`; rechaza la base de trabajo. La carga es reproducible y no sobrescribe estados existentes: si un identificador ya tiene otro estado, aborta transaccionalmente para revisión.

| Cédula sintética | Estado | Uso |
| --- | --- | --- |
| 0100000009 | Activo | Registro permitido |
| 0100000017 | Activo | Segunda cuenta para ensayos |
| 0100000025 | Inactivo | Registro rechazado |
| 0100000033 | Sin fila | Crea cuenta general sin rol ni fila socio |

Los números se generan por algoritmo, no se obtienen de personas ni prueban que no coincidan con alguna identificación real. Solo se usan como datos de prueba aislados. La carga no crea cuentas, claves ni roles; los cinco roles base proceden de SQL 01.

## Aplicación y reversión del esquema

SQL 05 añade `padron_prueba(cedula PK, activo NOT NULL)`, con comprobación de diez dígitos; añade índices únicos normalizados para correo y username y conserva los anteriores. SQL 06 actualiza la regla de cédula en instalaciones que habían aplicado la revisión inicial de SQL 05 con verificador. Usuario y padrón exigen ahora únicamente diez dígitos ASCII.

Cada script está dentro de una transacción. Ante cédulas con formato incompatible o duplicados por espacios, PostgreSQL aborta sin corregir, borrar ni fusionar registros. Antes de aplicarlo en una base con datos, el responsable de BD debe revisar privadamente:

```sql
-- Devuelven únicamente cantidades, sin revelar identificadores.
SELECT count(*) AS cedulas_incompatibles
FROM usuario WHERE cedula !~ '^[0-9]{10}$';

SELECT count(*) AS grupos_correo_duplicado
FROM (
  SELECT 1 FROM usuario GROUP BY lower(btrim(correo)) HAVING count(*) > 1
) AS conflictos;

SELECT count(*) AS grupos_username_duplicado
FROM (
  SELECT 1 FROM usuario GROUP BY lower(btrim(username)) HAVING count(*) > 1
) AS conflictos;
```

La reversión de padrón se encuentra en `backend/sql/reversiones/05_registro_padron_unicidad.sql`, fuera del conjunto que el runner carga automáticamente. Antes de ejecutarla, detener o retirar la versión del backend que depende del padrón y exportar su tabla. La reversión elimina esa tabla y los dos índices nuevos y conserva la comprobación de diez dígitos. Conserva cuentas, roles, socio y consentimiento; no revierte hashes ya generados ni normalización de nuevas cuentas. La reversión de SQL 06 permite restaurar deliberadamente la política histórica con verificador y aborta si existen cédulas incompatibles; no se deben borrar cuentas para hacerla pasar. Una versión antigua del backend sin soporte Argon2 no debe desplegarse contra claves nuevas sin compatibilidad de lectura.

Aplicación, reversión, reaplicación y aborto por datos incompatibles se probaron exclusivamente en base temporal. No se aplicó SQL 05 ni se cargaron datos en la base de trabajo.

## Matriz de trazabilidad

| Requisito o dependencia | Implementación | Evidencia automatizada |
| --- | --- | --- |
| HU-006 activo | Puerto Padron, adaptador ORM y servicio | test_activo_crea_fecha_consentimiento_y_hash_argon2id |
| HU-006 inactivo | SocioNoElegible y error 403 genérico | test_inactivo_se_rechaza_sin_crear_cuenta |
| Decisión posterior: ausente | Usuario y consentimiento sin socio ni rol | test_ausente_del_padron_crea_cuenta_general_y_puede_iniciar_sesion |
| Cuenta general sin privilegios | Autorización del servidor por áreas | Perfil 200 y cinco áreas 403 en la prueba de alta general |
| Unicidad de cuenta general | Comprobaciones e índices existentes | test_duplicados_tambien_se_rechazan_para_cuentas_generales y test_carrera_por_cedula_de_cuenta_general |
| Atomicidad de cuenta general | Consentimiento y auditoría dentro de atomic | test_fallo_intermedio_de_cuenta_general_revierte_todo |
| Resultado desconocido del adaptador | Rechazo seguro sin cuenta | test_estado_desconocido_del_adaptador_no_autoriza_ninguna_cuenta |
| HU-006 fallo de padrón | ServicioNoDisponible y atomic | test_fallo_padron_cierra_registro_y_no_filtra_detalles |
| HU-006 independencia del padrón | Tabla sin FK a usuario y carga explícita | test_carga_reproducible_y_estados_independientes |
| HU-006 reemplazo del adaptador | Protocol y argumento padron | test_contrato_inyectable |
| HU-006 autoridad del servidor | Lista de campos permitidos y fecha generada en backend | test_no_acepta_campos_controlados_por_servidor |
| HU-008 duplicados normales | Repositorio y prevalidaciones del servicio | test_normaliza_antes_de_almacenar_y_rechaza_duplicados y pruebas existentes de duplicados |
| HU-008 garantía SQL | Restricciones e índices normalizados | test_unicidad_directa_de_cedula_correo_y_username |
| HU-008 carreras reales | Captura tras rollback y SQLSTATE/nombre de restricción | test_carrera_por_cedula, test_carrera_por_correo, test_carrera_por_username |
| HU-008 errores de integridad desconocidos | No convertirlos en duplicados | test_integridad_desconocida_no_se_convierte_en_duplicado |
| HU-008 y creación de socio | Savepoint y reintento selectivo de código | test_codigos_socio.py, con violación real de restricciones PostgreSQL |
| T-007 entradas y logs | Obligatoriedad, JSON y diagnóstico sin detalles sensibles | test_validacion_y_errores.py y entrada SQL tratada como texto en test_registro_sprint1.py |
| HU-006/HU-008 atomicidad | Usuario, socio, rol, consentimiento y auditoría en atomic | test_fallo_intermedio_revierte_todas_las_filas y sin_cuenta en rechazos |
| Decisión posterior: diez dígitos sin verificador | Validación Python, SQL y React | test_cedula.py, test_sql_acepta_diez_digitos_sin_verificador y test_sql_rechaza_caracteres_no_numericos |
| HU-001 consentimiento | Booleano explícito y validación del servicio | test_consentimiento_obligatorio_y_booleano_estricto |
| HU-001 ceros iniciales | Cédula textual y serializador | test_cedula_numerica_se_rechaza y prueba de registro activo |
| HU-001 hash | Argon2PasswordHasher y lectores históricos | Prueba de hash Argon2id, test_hash_historico_pbkdf2_permite_login_y_se_actualiza, login y recuperación existentes |
| T-007 errores seguros | Manejador global genérico, ORM y serializador | Pruebas de infraestructura, fallo intermedio, manipulación y cuerpo JSON |
| T-007 límite de solicitudes | LimiteAutenticacion conservado | test_limite_solicitudes_conservado |
| T-011 reversibilidad | SQL 05 y reversiones/05 | test_reversion_y_reaplicacion_en_postgresql |
| T-011 conflictos sin pérdida | DDL transaccional | test_conflictos_abortan_sin_alterar_cuentas_ni_esquema |
| T-004 documentación | Diagramas Mermaid de clases y secuencia | Revisión textual de correspondencia con código |

La concurrencia utiliza dos APIClient en hilos, conexiones distintas verificadas mediante `pg_backend_pid()` y transacciones independientes. La barrera solo sincroniza el momento posterior a las consultas previas: las consultas y escrituras PostgreSQL son reales. Cada carrera comprueba un 201, un 409 con campo correcto, una sola fila de usuario/socio/rol/consentimiento y una auditoría de éxito.

## Resultados y límites

Los resultados finales y el conteo consolidado se registran en [el plan](../../docs/plan-valeria-sprint-1.md#evidencia-final). Se preservó el fallo inicial como evidencia de la discrepancia: 17 pruebas iniciales, una fallida por verificador inválido aceptado.

Se verificó el flujo HTTP de registro, login, perfil y refresh mediante APIClient, con PostgreSQL real, además del build React. No se realizó una sesión manual de navegador ni se verificó envío real de correo, integraciones institucionales o despliegue. Los diagramas Mermaid se entregan como fuente Markdown; no se generó un documento Word ni se verificó su renderizado visual.

Persisten fuera del alcance: advertencias de Fast Refresh en componentes de panel sin modificar; integración general de T-011/T-012 por su responsable; otros diagramas de T-004; estrategia institucional de padrón real y tareas de sprints posteriores. El código duplicado existente bajo `frontend/frontend/` no se reorganizó.
