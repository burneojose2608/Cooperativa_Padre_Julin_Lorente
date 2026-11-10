-- Decisión posterior del usuario: solo diez dígitos, sin provincia/verificador.
-- Actualiza instalaciones que ya aplicaron la versión anterior de SQL 05.
-- No altera valores ni elimina filas. Aplicable nuevamente sin pérdida de datos.
BEGIN;
DO $$
BEGIN
  IF current_database() IN ('postgres', 'template0', 'template1') THEN
    RAISE EXCEPTION 'Seleccione una base de la aplicación.';
  END IF;
END $$;
SET LOCAL search_path TO public;
ALTER TABLE usuario DROP CONSTRAINT ck_usuario_cedula;
ALTER TABLE usuario ADD CONSTRAINT ck_usuario_cedula CHECK (cedula ~ '^[0-9]{10}$');
ALTER TABLE padron_prueba DROP CONSTRAINT ck_padron_cedula;
ALTER TABLE padron_prueba ADD CONSTRAINT ck_padron_cedula CHECK (cedula ~ '^[0-9]{10}$');
COMMIT;
