-- =====================================================================
--  AJUSTES RECOMENDADOS (opcional pero aconsejado)
--  Ejecutar DESPUÉS de 01_base_datos_cooperativa.sql, UNA sola vez,
--  con la base aún sin usuarios registrados.
--  Solo AGREGA columnas y tablas; no borra ni cambia nada existente.
-- =====================================================================
BEGIN;

-- 1. USUARIO: datos que pide el registro (HU-001, RF-01) y el bloqueo por intentos (RF-02)
ALTER TABLE usuario
  ADD COLUMN username          varchar(50) NOT NULL,
  ADD COLUMN telefono          varchar(15) NOT NULL,
  ADD COLUMN fecha_nacimiento  date        NOT NULL,
  ADD COLUMN intentos_fallidos smallint    NOT NULL DEFAULT 0,
  ADD COLUMN bloqueado_hasta   timestamptz,
  ADD CONSTRAINT ck_usuario_telefono CHECK (telefono ~ '^[0-9+]{7,15}$'),
  ADD CONSTRAINT ck_usuario_nacimiento CHECK (fecha_nacimiento <= current_date AND fecha_nacimiento >= DATE '1900-01-01'),
  ADD CONSTRAINT ck_usuario_intentos CHECK (intentos_fallidos >= 0);
CREATE UNIQUE INDEX uq_usuario_username_ci ON usuario (lower(username));

-- 2. SESIÓN y AUDITORÍA
ALTER TABLE sesion ADD COLUMN ultimo_uso timestamptz;
-- (auditoria es de solo inserción: agregar una columna no la modifica)
ALTER TABLE auditoria ADD COLUMN ip inet;

-- 3. PROSPECTO: contacto separado, consentimiento y confirmación (RF-03-5, RF-03-8, RNF-02, RNF-25)
ALTER TABLE prospecto
  ADD COLUMN nombre           varchar(150),
  ADD COLUMN telefono         varchar(15),
  ADD COLUMN correo           varchar(254),
  ADD COLUMN consentimiento_en timestamptz,   -- cuándo aceptó que lo contacten
  ADD COLUMN confirmado_en     timestamptz;   -- cuándo confirmó el referido

-- 4. HISTORIAL DE ESTADOS (RNF-13): quién cambió qué estado y cuándo. Solo inserción.
CREATE TABLE historial_estado (
  id_historial    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  entidad         varchar(40) NOT NULL,              -- 'referido', 'campana', 'canje'...
  registro_id     bigint      NOT NULL,
  estado_anterior varchar(20),
  estado_nuevo    varchar(20) NOT NULL,
  id_usuario      bigint REFERENCES usuario(id_usuario),
  fecha           timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX ix_historial_entidad ON historial_estado (entidad, registro_id);
CREATE INDEX ix_historial_usuario ON historial_estado (id_usuario);
CREATE TRIGGER trg_historial_solo_insercion
  BEFORE UPDATE OR DELETE ON historial_estado
  FOR EACH ROW EXECUTE FUNCTION bloquear_modificacion();

-- 5. TALLERES (RF-06-8, RF-06-9)
CREATE TABLE taller (
  id_taller   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  titulo      varchar(200) NOT NULL,
  fecha       timestamptz  NOT NULL,
  cupo        integer,                               -- vacío = sin límite
  estado      varchar(12)  NOT NULL DEFAULT 'PROGRAMADO',
  CONSTRAINT ck_taller_cupo CHECK (cupo IS NULL OR cupo > 0),
  CONSTRAINT ck_taller_estado CHECK (estado IN ('PROGRAMADO','REALIZADO','CANCELADO'))
);
CREATE TABLE asistencia_taller (
  id_asistencia bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_taller     bigint NOT NULL REFERENCES taller(id_taller),
  id_socio      bigint NOT NULL REFERENCES socio(id_usuario),
  asistio       boolean NOT NULL DEFAULT false,
  registrado_en timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_asistencia UNIQUE (id_taller, id_socio)
);
CREATE INDEX ix_asistencia_socio ON asistencia_taller (id_socio);

-- 6. CAMPAÑA: tipo, objetivo, meta e incentivos
ALTER TABLE campana
  ADD COLUMN tipo        varchar(30),
  ADD COLUMN objetivo    varchar(300),
  ADD COLUMN meta        integer,
  ADD COLUMN incentivos  text,
  ADD CONSTRAINT ck_campana_meta CHECK (meta IS NULL OR meta > 0);

-- 7. SORTEO: cantidad de ganadores/suplentes y varios premios
ALTER TABLE sorteo
  ADD COLUMN num_ganadores smallint NOT NULL DEFAULT 1,
  ADD COLUMN num_suplentes smallint NOT NULL DEFAULT 0,
  ADD CONSTRAINT ck_sorteo_ganadores CHECK (num_ganadores > 0 AND num_suplentes >= 0);
ALTER TABLE ganador ADD COLUMN es_suplente boolean NOT NULL DEFAULT false;
CREATE TABLE premio_sorteo (
  id_premio   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_sorteo   bigint NOT NULL REFERENCES sorteo(id_sorteo),
  posicion    smallint NOT NULL,
  descripcion varchar(200) NOT NULL,
  CONSTRAINT ck_premio_posicion CHECK (posicion > 0),
  CONSTRAINT uq_premio_posicion UNIQUE (id_sorteo, posicion)
);

-- 8. CANJE: puntos descontados
ALTER TABLE canje ADD COLUMN puntos integer, ADD CONSTRAINT ck_canje_puntos CHECK (puntos IS NULL OR puntos > 0);

-- 9. CONTENIDO: texto y vigencia
ALTER TABLE contenido
  ADD COLUMN cuerpo         text,
  ADD COLUMN vigente_desde  date,
  ADD COLUMN vigente_hasta  date,
  ADD CONSTRAINT ck_contenido_vigencia CHECK (vigente_hasta IS NULL OR vigente_desde IS NULL OR vigente_hasta >= vigente_desde);

-- 10. BANCO DE PREGUNTAS (evaluaciones y juegos)
CREATE TABLE pregunta (
  id_pregunta   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_evaluacion bigint REFERENCES evaluacion(id_evaluacion),
  id_juego      bigint REFERENCES juego(id_juego),
  enunciado     text NOT NULL,
  -- la pregunta pertenece a una evaluación O a un juego, nunca a ambos ni a ninguno
  CONSTRAINT ck_pregunta_dueno CHECK ((id_evaluacion IS NOT NULL) <> (id_juego IS NOT NULL))
);
CREATE INDEX ix_pregunta_evaluacion ON pregunta (id_evaluacion);
CREATE INDEX ix_pregunta_juego ON pregunta (id_juego);
CREATE TABLE opcion_pregunta (
  id_opcion   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_pregunta bigint NOT NULL REFERENCES pregunta(id_pregunta),
  texto       varchar(300) NOT NULL,
  es_correcta boolean NOT NULL DEFAULT false
);
CREATE INDEX ix_opcion_pregunta ON opcion_pregunta (id_pregunta);
CREATE UNIQUE INDEX uq_una_correcta ON opcion_pregunta (id_pregunta) WHERE es_correcta;

COMMIT;
