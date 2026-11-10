-- Reversión MANUAL. Retirar primero la versión del backend que usa padrón.
-- Exportar padron_prueba antes: la reversión elimina únicamente esa tabla.
BEGIN;
DO $$
BEGIN
  IF current_database() IN ('postgres', 'template0', 'template1') THEN
    RAISE EXCEPTION 'Seleccione una base de la aplicación.';
  END IF;
END $$;
SET LOCAL search_path TO public;
DROP TABLE padron_prueba;
DROP INDEX uq_usuario_correo_normalizado;
DROP INDEX uq_usuario_username_normalizado;
ALTER TABLE usuario DROP CONSTRAINT ck_usuario_cedula;
ALTER TABLE usuario ADD CONSTRAINT ck_usuario_cedula CHECK (cedula ~ '^[0-9]{10}$');
COMMIT;
