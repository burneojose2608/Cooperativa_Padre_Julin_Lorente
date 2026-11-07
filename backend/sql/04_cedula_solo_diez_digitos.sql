-- =====================================================================
--  04 · La cédula solo debe tener 10 dígitos (sin cálculo del verificador)
--  La unicidad ya la garantiza la restricción UNIQUE de usuario.cedula.
--  Ejecutar UNA sola vez en pgAdmin, sobre la base cooperativa_db.
-- =====================================================================
BEGIN;

ALTER TABLE usuario DROP CONSTRAINT IF EXISTS ck_usuario_cedula;
ALTER TABLE usuario ADD CONSTRAINT ck_usuario_cedula CHECK (cedula ~ '^[0-9]{10}$');

COMMIT;
