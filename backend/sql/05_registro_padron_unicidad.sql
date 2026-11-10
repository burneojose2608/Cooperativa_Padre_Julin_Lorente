-- HU-006/HU-008 y dependencia HU-001. Aplicar después de 01–04.
-- Transaccional: datos incompatibles abortan sin corregirlos ni borrarlos.
BEGIN;
DO $$
BEGIN
  IF current_database() IN ('postgres', 'template0', 'template1') THEN
    RAISE EXCEPTION 'Seleccione una base de la aplicación.';
  END IF;
END $$;
SET LOCAL search_path TO public;

CREATE TABLE padron_prueba (
  cedula varchar(10) PRIMARY KEY,
  activo boolean NOT NULL,
  CONSTRAINT ck_padron_cedula CHECK (cedula ~ '^[0-9]{10}$')
);

-- Se conservan las restricciones existentes. Estos índices cubren además
-- espacios exteriores en escrituras directas que no pasan por el servicio.
CREATE UNIQUE INDEX uq_usuario_correo_normalizado ON usuario (lower(btrim(correo)));
CREATE UNIQUE INDEX uq_usuario_username_normalizado ON usuario (lower(btrim(username)));
ALTER TABLE usuario DROP CONSTRAINT ck_usuario_cedula;
ALTER TABLE usuario ADD CONSTRAINT ck_usuario_cedula CHECK (cedula ~ '^[0-9]{10}$');
COMMIT;
