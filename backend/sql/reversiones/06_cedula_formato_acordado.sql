-- Reversión a la validación matemática de la versión anterior de SQL 05.
-- Si hay cédulas incompatibles, ABORTA sin borrar ni corregir datos.
BEGIN;
DO $$
BEGIN
  IF current_database() IN ('postgres', 'template0', 'template1') THEN
    RAISE EXCEPTION 'Seleccione una base de la aplicación.';
  END IF;
END $$;
SET LOCAL search_path TO public;
ALTER TABLE usuario DROP CONSTRAINT ck_usuario_cedula;
ALTER TABLE usuario ADD CONSTRAINT ck_usuario_cedula CHECK (cedula_ec_valida(cedula));
ALTER TABLE padron_prueba DROP CONSTRAINT ck_padron_cedula;
ALTER TABLE padron_prueba ADD CONSTRAINT ck_padron_cedula CHECK (cedula_ec_valida(cedula));
COMMIT;
