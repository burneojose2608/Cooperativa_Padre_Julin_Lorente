# Diccionario de datos de Sprint 1

Generado desde metadatos PostgreSQL en una transacción de solo lectura. No incluye registros de personas, claves o tokens.
El alcance es usuarios, autenticación, roles, padrón y auditoría. Los modelos físicos de módulos posteriores no se declaran cerrados por este catálogo.

## usuario

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_usuario | int8 | NO | PK |
| cedula | varchar | NO | - |
| nombre | varchar | NO | - |
| apellido | varchar | NO | - |
| correo | varchar | NO | - |
| clave_hash | varchar | NO | - |
| estado | varchar | NO | - |
| creado_en | timestamptz | NO | - |
| username | varchar | NO | - |
| telefono | varchar | NO | - |
| fecha_nacimiento | date | NO | - |
| intentos_fallidos | int2 | NO | - |
| bloqueado_hasta | timestamptz | YES | - |

Restricciones:

- `ck_usuario_cedula`: `CHECK (((cedula)::text ~ '^[0-9]{10}$'::text))`.
- `ck_usuario_estado`: `CHECK (((estado)::text = ANY ((ARRAY['ACTIVA'::character varying, 'SUSPENDIDA'::character varying, 'DESACTIVADA'::character varying])::text[])))`.
- `ck_usuario_intentos`: `CHECK ((intentos_fallidos >= 0))`.
- `ck_usuario_nacimiento`: `CHECK (((fecha_nacimiento <= CURRENT_DATE) AND (fecha_nacimiento >= '1900-01-01'::date)))`.
- `ck_usuario_telefono`: `CHECK (((telefono)::text ~ '^[0-9+]{7,15}$'::text))`.
- `usuario_apellido_not_null`: `NOT NULL apellido`.
- `usuario_cedula_key`: `UNIQUE (cedula)`.
- `usuario_cedula_not_null`: `NOT NULL cedula`.
- `usuario_clave_hash_not_null`: `NOT NULL clave_hash`.
- `usuario_correo_not_null`: `NOT NULL correo`.
- `usuario_creado_en_not_null`: `NOT NULL creado_en`.
- `usuario_estado_not_null`: `NOT NULL estado`.
- `usuario_fecha_nacimiento_not_null`: `NOT NULL fecha_nacimiento`.
- `usuario_id_usuario_not_null`: `NOT NULL id_usuario`.
- `usuario_intentos_fallidos_not_null`: `NOT NULL intentos_fallidos`.
- `usuario_nombre_not_null`: `NOT NULL nombre`.
- `usuario_pkey`: `PRIMARY KEY (id_usuario)`.
- `usuario_telefono_not_null`: `NOT NULL telefono`.
- `usuario_username_not_null`: `NOT NULL username`.

Índices:

- `uq_usuario_correo_ci`: `CREATE UNIQUE INDEX uq_usuario_correo_ci ON public.usuario USING btree (lower((correo)::text))`.
- `uq_usuario_correo_normalizado`: `CREATE UNIQUE INDEX uq_usuario_correo_normalizado ON public.usuario USING btree (lower(btrim((correo)::text)))`.
- `uq_usuario_username_ci`: `CREATE UNIQUE INDEX uq_usuario_username_ci ON public.usuario USING btree (lower((username)::text))`.
- `uq_usuario_username_normalizado`: `CREATE UNIQUE INDEX uq_usuario_username_normalizado ON public.usuario USING btree (lower(btrim((username)::text)))`.
- `usuario_cedula_key`: `CREATE UNIQUE INDEX usuario_cedula_key ON public.usuario USING btree (cedula)`.
- `usuario_pkey`: `CREATE UNIQUE INDEX usuario_pkey ON public.usuario USING btree (id_usuario)`.

## socio

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_usuario | int8 | NO | FK, PK |
| codigo_socio | varchar | NO | - |
| validado_en | timestamptz | YES | - |

Restricciones:

- `socio_codigo_socio_key`: `UNIQUE (codigo_socio)`.
- `socio_codigo_socio_not_null`: `NOT NULL codigo_socio`.
- `socio_id_usuario_fkey`: `FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)`.
- `socio_id_usuario_not_null`: `NOT NULL id_usuario`.
- `socio_pkey`: `PRIMARY KEY (id_usuario)`.

Índices:

- `socio_codigo_socio_key`: `CREATE UNIQUE INDEX socio_codigo_socio_key ON public.socio USING btree (codigo_socio)`.
- `socio_pkey`: `CREATE UNIQUE INDEX socio_pkey ON public.socio USING btree (id_usuario)`.

## padron_prueba

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| cedula | varchar | NO | PK |
| activo | bool | NO | - |

Restricciones:

- `ck_padron_cedula`: `CHECK (((cedula)::text ~ '^[0-9]{10}$'::text))`.
- `padron_prueba_activo_not_null`: `NOT NULL activo`.
- `padron_prueba_cedula_not_null`: `NOT NULL cedula`.
- `padron_prueba_pkey`: `PRIMARY KEY (cedula)`.

Índices:

- `padron_prueba_pkey`: `CREATE UNIQUE INDEX padron_prueba_pkey ON public.padron_prueba USING btree (cedula)`.

## rol

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_rol | int8 | NO | PK |
| nombre | varchar | NO | - |

Restricciones:

- `rol_id_rol_not_null`: `NOT NULL id_rol`.
- `rol_nombre_key`: `UNIQUE (nombre)`.
- `rol_nombre_not_null`: `NOT NULL nombre`.
- `rol_pkey`: `PRIMARY KEY (id_rol)`.

Índices:

- `rol_nombre_key`: `CREATE UNIQUE INDEX rol_nombre_key ON public.rol USING btree (nombre)`.
- `rol_pkey`: `CREATE UNIQUE INDEX rol_pkey ON public.rol USING btree (id_rol)`.

## usuario_rol

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_usuario_rol | int8 | NO | PK |
| id_usuario | int8 | NO | FK |
| id_rol | int8 | NO | FK |

Restricciones:

- `uq_usuario_rol`: `UNIQUE (id_usuario, id_rol)`.
- `usuario_rol_id_rol_fkey`: `FOREIGN KEY (id_rol) REFERENCES rol(id_rol)`.
- `usuario_rol_id_rol_not_null`: `NOT NULL id_rol`.
- `usuario_rol_id_usuario_fkey`: `FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)`.
- `usuario_rol_id_usuario_not_null`: `NOT NULL id_usuario`.
- `usuario_rol_id_usuario_rol_not_null`: `NOT NULL id_usuario_rol`.
- `usuario_rol_pkey`: `PRIMARY KEY (id_usuario_rol)`.

Índices:

- `ix_usuario_rol_rol`: `CREATE INDEX ix_usuario_rol_rol ON public.usuario_rol USING btree (id_rol)`.
- `uq_usuario_rol`: `CREATE UNIQUE INDEX uq_usuario_rol ON public.usuario_rol USING btree (id_usuario, id_rol)`.
- `usuario_rol_pkey`: `CREATE UNIQUE INDEX usuario_rol_pkey ON public.usuario_rol USING btree (id_usuario_rol)`.

## permiso

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_permiso | int8 | NO | PK |
| modulo | varchar | NO | - |
| accion | varchar | NO | - |

Restricciones:

- `permiso_accion_not_null`: `NOT NULL accion`.
- `permiso_id_permiso_not_null`: `NOT NULL id_permiso`.
- `permiso_modulo_not_null`: `NOT NULL modulo`.
- `permiso_pkey`: `PRIMARY KEY (id_permiso)`.
- `uq_permiso`: `UNIQUE (modulo, accion)`.

Índices:

- `permiso_pkey`: `CREATE UNIQUE INDEX permiso_pkey ON public.permiso USING btree (id_permiso)`.
- `uq_permiso`: `CREATE UNIQUE INDEX uq_permiso ON public.permiso USING btree (modulo, accion)`.

## rol_permiso

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_rol_permiso | int8 | NO | PK |
| id_rol | int8 | NO | FK |
| id_permiso | int8 | NO | FK |

Restricciones:

- `rol_permiso_id_permiso_fkey`: `FOREIGN KEY (id_permiso) REFERENCES permiso(id_permiso)`.
- `rol_permiso_id_permiso_not_null`: `NOT NULL id_permiso`.
- `rol_permiso_id_rol_fkey`: `FOREIGN KEY (id_rol) REFERENCES rol(id_rol)`.
- `rol_permiso_id_rol_not_null`: `NOT NULL id_rol`.
- `rol_permiso_id_rol_permiso_not_null`: `NOT NULL id_rol_permiso`.
- `rol_permiso_pkey`: `PRIMARY KEY (id_rol_permiso)`.
- `uq_rol_permiso`: `UNIQUE (id_rol, id_permiso)`.

Índices:

- `ix_rol_permiso_permiso`: `CREATE INDEX ix_rol_permiso_permiso ON public.rol_permiso USING btree (id_permiso)`.
- `rol_permiso_pkey`: `CREATE UNIQUE INDEX rol_permiso_pkey ON public.rol_permiso USING btree (id_rol_permiso)`.
- `uq_rol_permiso`: `CREATE UNIQUE INDEX uq_rol_permiso ON public.rol_permiso USING btree (id_rol, id_permiso)`.

## consentimiento

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_consentimiento | int8 | NO | PK |
| id_usuario | int8 | NO | FK |
| version | varchar | NO | - |
| fecha_aceptacion | timestamptz | NO | - |

Restricciones:

- `consentimiento_fecha_aceptacion_not_null`: `NOT NULL fecha_aceptacion`.
- `consentimiento_id_consentimiento_not_null`: `NOT NULL id_consentimiento`.
- `consentimiento_id_usuario_fkey`: `FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)`.
- `consentimiento_id_usuario_not_null`: `NOT NULL id_usuario`.
- `consentimiento_pkey`: `PRIMARY KEY (id_consentimiento)`.
- `consentimiento_version_not_null`: `NOT NULL version`.

Índices:

- `consentimiento_pkey`: `CREATE UNIQUE INDEX consentimiento_pkey ON public.consentimiento USING btree (id_consentimiento)`.
- `ix_consentimiento_usuario`: `CREATE INDEX ix_consentimiento_usuario ON public.consentimiento USING btree (id_usuario)`.

## sesion

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_sesion | int8 | NO | PK |
| id_usuario | int8 | NO | FK |
| vence_en | timestamptz | NO | - |
| revocada_en | timestamptz | YES | - |
| ultimo_uso | timestamptz | YES | - |

Restricciones:

- `sesion_id_sesion_not_null`: `NOT NULL id_sesion`.
- `sesion_id_usuario_fkey`: `FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)`.
- `sesion_id_usuario_not_null`: `NOT NULL id_usuario`.
- `sesion_pkey`: `PRIMARY KEY (id_sesion)`.
- `sesion_vence_en_not_null`: `NOT NULL vence_en`.

Índices:

- `ix_sesion_usuario`: `CREATE INDEX ix_sesion_usuario ON public.sesion USING btree (id_usuario)`.
- `sesion_pkey`: `CREATE UNIQUE INDEX sesion_pkey ON public.sesion USING btree (id_sesion)`.

## auditoria

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_auditoria | int8 | NO | PK |
| id_usuario | int8 | YES | FK |
| entidad | varchar | NO | - |
| registro_id | varchar | YES | - |
| accion | varchar | NO | - |
| fecha | timestamptz | NO | - |
| resultado | varchar | NO | - |
| ip | inet | YES | - |

Restricciones:

- `auditoria_accion_not_null`: `NOT NULL accion`.
- `auditoria_entidad_not_null`: `NOT NULL entidad`.
- `auditoria_fecha_not_null`: `NOT NULL fecha`.
- `auditoria_id_auditoria_not_null`: `NOT NULL id_auditoria`.
- `auditoria_id_usuario_fkey`: `FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)`.
- `auditoria_pkey`: `PRIMARY KEY (id_auditoria)`.
- `auditoria_resultado_not_null`: `NOT NULL resultado`.
- `ck_auditoria_resultado`: `CHECK (((resultado)::text = ANY ((ARRAY['EXITO'::character varying, 'FALLO'::character varying])::text[])))`.

Índices:

- `auditoria_pkey`: `CREATE UNIQUE INDEX auditoria_pkey ON public.auditoria USING btree (id_auditoria)`.
- `ix_auditoria_entidad`: `CREATE INDEX ix_auditoria_entidad ON public.auditoria USING btree (entidad, registro_id)`.
- `ix_auditoria_fecha`: `CREATE INDEX ix_auditoria_fecha ON public.auditoria USING btree (fecha)`.
- `ix_auditoria_usuario`: `CREATE INDEX ix_auditoria_usuario ON public.auditoria USING btree (id_usuario)`.

## token_recuperacion

| Columna | Tipo PostgreSQL | Admite NULL | Clave |
| --- | --- | --- | --- |
| id_token | int8 | NO | PK |
| id_usuario | int8 | NO | FK |
| token_hash | bpchar | NO | - |
| creado_en | timestamptz | NO | - |
| vence_en | timestamptz | NO | - |
| usado_en | timestamptz | YES | - |

Restricciones:

- `ck_token_vigencia`: `CHECK ((vence_en > creado_en))`.
- `token_recuperacion_creado_en_not_null`: `NOT NULL creado_en`.
- `token_recuperacion_id_token_not_null`: `NOT NULL id_token`.
- `token_recuperacion_id_usuario_fkey`: `FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)`.
- `token_recuperacion_id_usuario_not_null`: `NOT NULL id_usuario`.
- `token_recuperacion_pkey`: `PRIMARY KEY (id_token)`.
- `token_recuperacion_token_hash_key`: `UNIQUE (token_hash)`.
- `token_recuperacion_token_hash_not_null`: `NOT NULL token_hash`.
- `token_recuperacion_vence_en_not_null`: `NOT NULL vence_en`.

Índices:

- `ix_token_recuperacion_usuario`: `CREATE INDEX ix_token_recuperacion_usuario ON public.token_recuperacion USING btree (id_usuario, creado_en)`.
- `token_recuperacion_pkey`: `CREATE UNIQUE INDEX token_recuperacion_pkey ON public.token_recuperacion USING btree (id_token)`.
- `token_recuperacion_token_hash_key`: `CREATE UNIQUE INDEX token_recuperacion_token_hash_key ON public.token_recuperacion USING btree (token_hash)`.

