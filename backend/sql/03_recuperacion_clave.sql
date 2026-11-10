-- =====================================================================
--  RECUPERAR CONTRASEÑA (RF-01)
--  Ejecutar UNA vez sobre cooperativa_db, después de 01 y 02.
--  Guarda los enlaces de recuperación: solo se guarda la HUELLA (hash) del
--  token, nunca el token, así que nadie puede usarlo leyendo la base.
-- =====================================================================
BEGIN;

DO $$
BEGIN
  IF current_database() IN ('postgres', 'template0', 'template1') THEN
    RAISE EXCEPTION 'Base incorrecta: %. Conectate a cooperativa_db antes de ejecutar los scripts.', current_database();
  END IF;
END $$;
SET LOCAL search_path TO public;

CREATE TABLE token_recuperacion (
  id_token    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_usuario  bigint      NOT NULL REFERENCES usuario(id_usuario),
  token_hash  char(64)    NOT NULL UNIQUE,            -- SHA-256 del token enviado por correo
  creado_en   timestamptz NOT NULL DEFAULT now(),
  vence_en    timestamptz NOT NULL,
  usado_en    timestamptz,                            -- se llena al usarlo: un solo uso
  CONSTRAINT ck_token_vigencia CHECK (vence_en > creado_en)
);
CREATE INDEX ix_token_recuperacion_usuario ON token_recuperacion (id_usuario, creado_en);

COMMIT;
