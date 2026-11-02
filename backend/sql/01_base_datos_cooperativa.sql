-- =====================================================================
--  BASE DE DATOS: Plataforma de referidos y gamificación
--  COAC Padre Julián Lorente  ·  PostgreSQL
--  Implementa el modelo entidad-relación propuesto (47 tablas, 8 módulos).
--
--  Cómo ejecutarlo:  pgAdmin -> clic derecho en la base "cooperativa_db"
--  -> Query Tool -> abrir este archivo -> botón ▶ (F5).
--  Debe ejecutarse UNA vez sobre una base vacía.
-- =====================================================================

-- ---------------------------------------------------------------------
--  Validación de cédula ecuatoriana (RF-01-1): 10 dígitos, provincia
--  01-24 o 30, tercer dígito < 6 y dígito verificador (módulo 10).
--  Comprueba que el número sea matemáticamente válido, no que exista.
-- ---------------------------------------------------------------------
CREATE FUNCTION cedula_ec_valida(c text) RETURNS boolean
LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE
  coef int[] := ARRAY[2,1,2,1,2,1,2,1,2];
  total int := 0; prod int; i int;
BEGIN
  IF c IS NULL OR c !~ '^[0-9]{10}$' THEN RETURN false; END IF;
  IF NOT (substr(c,1,2)::int BETWEEN 1 AND 24 OR substr(c,1,2)::int = 30) THEN RETURN false; END IF;
  IF substr(c,3,1)::int >= 6 THEN RETURN false; END IF;
  FOR i IN 1..9 LOOP
    prod := substr(c,i,1)::int * coef[i];
    IF prod >= 10 THEN prod := prod - 9; END IF;
    total := total + prod;
  END LOOP;
  RETURN ((10 - total % 10) % 10) = substr(c,10,1)::int;
END $$;

-- Tablas de solo inserción (auditoría y libro de puntos): RNF-06, RF-05-6
CREATE FUNCTION bloquear_modificacion() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'La tabla % es de solo inserción: no se permite % de registros.', TG_TABLE_NAME, TG_OP;
END $$;

-- =====================================================================
--  1. IDENTIDAD Y ACCESO
-- =====================================================================
CREATE TABLE usuario (
  id_usuario   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  cedula       varchar(10)  NOT NULL UNIQUE,
  nombre       varchar(100) NOT NULL,
  apellido     varchar(100) NOT NULL,
  correo       varchar(254) NOT NULL,
  clave_hash   varchar(255) NOT NULL,              -- contraseña cifrada, nunca en texto plano
  estado       varchar(12)  NOT NULL DEFAULT 'ACTIVA',
  creado_en    timestamptz  NOT NULL DEFAULT now(),
  CONSTRAINT ck_usuario_cedula CHECK (cedula_ec_valida(cedula)),
  CONSTRAINT ck_usuario_estado CHECK (estado IN ('ACTIVA','SUSPENDIDA','DESACTIVADA'))
);
-- Correo único sin distinguir mayúsculas (RF-01-8)
CREATE UNIQUE INDEX uq_usuario_correo_ci ON usuario (lower(correo));

CREATE TABLE socio (
  id_usuario   bigint PRIMARY KEY REFERENCES usuario(id_usuario),   -- 1 usuario : 0..1 socio
  codigo_socio varchar(20) NOT NULL UNIQUE,
  validado_en  timestamptz                                           -- vacío = aún no validado en el padrón
);

CREATE TABLE rol (
  id_rol  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nombre  varchar(60) NOT NULL UNIQUE
);

CREATE TABLE usuario_rol (
  id_usuario_rol bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_usuario     bigint NOT NULL REFERENCES usuario(id_usuario),
  id_rol         bigint NOT NULL REFERENCES rol(id_rol),
  CONSTRAINT uq_usuario_rol UNIQUE (id_usuario, id_rol)
);

CREATE TABLE permiso (
  id_permiso bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  modulo     varchar(50) NOT NULL,
  accion     varchar(50) NOT NULL,
  CONSTRAINT uq_permiso UNIQUE (modulo, accion)
);

CREATE TABLE rol_permiso (
  id_rol_permiso bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_rol         bigint NOT NULL REFERENCES rol(id_rol),
  id_permiso     bigint NOT NULL REFERENCES permiso(id_permiso),
  CONSTRAINT uq_rol_permiso UNIQUE (id_rol, id_permiso)
);

CREATE TABLE consentimiento (
  id_consentimiento bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_usuario        bigint NOT NULL REFERENCES usuario(id_usuario),
  version           varchar(20) NOT NULL,           -- versión de la política aceptada (RNF-02)
  fecha_aceptacion  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE sesion (
  id_sesion    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_usuario   bigint NOT NULL REFERENCES usuario(id_usuario),
  vence_en     timestamptz NOT NULL,
  revocada_en  timestamptz                            -- se llena al cerrar sesión (RF-02-7)
);

-- =====================================================================
--  2. NOTIFICACIONES Y AUDITORÍA
-- =====================================================================
CREATE TABLE auditoria (
  id_auditoria bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_usuario   bigint REFERENCES usuario(id_usuario), -- vacío en intentos de acceso anónimos
  entidad      varchar(60) NOT NULL,
  registro_id  varchar(40),
  accion       varchar(60) NOT NULL,
  fecha        timestamptz NOT NULL DEFAULT now(),
  resultado    varchar(6)  NOT NULL,
  CONSTRAINT ck_auditoria_resultado CHECK (resultado IN ('EXITO','FALLO'))
);
CREATE TRIGGER trg_auditoria_solo_insercion
  BEFORE UPDATE OR DELETE ON auditoria
  FOR EACH ROW EXECUTE FUNCTION bloquear_modificacion();

CREATE TABLE plantilla_notificacion (
  id_plantilla bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  evento       varchar(40)  NOT NULL,
  asunto       varchar(150) NOT NULL,
  cuerpo       text         NOT NULL
);

CREATE TABLE notificacion (
  id_notificacion bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_usuario      bigint NOT NULL REFERENCES usuario(id_usuario),
  id_plantilla    bigint NOT NULL REFERENCES plantilla_notificacion(id_plantilla),
  canal           varchar(8)  NOT NULL,
  estado          varchar(12) NOT NULL DEFAULT 'PENDIENTE',
  enviada_en      timestamptz,
  creado_en       timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT ck_notificacion_canal CHECK (canal IN ('INTERNA','CORREO'))
);

CREATE TABLE preferencia_notificacion (
  id_preferencia bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_usuario     bigint NOT NULL REFERENCES usuario(id_usuario),
  evento         varchar(40) NOT NULL,
  canal          varchar(8)  NOT NULL,
  habilitada     boolean     NOT NULL DEFAULT true,
  CONSTRAINT ck_preferencia_canal CHECK (canal IN ('INTERNA','CORREO')),
  CONSTRAINT uq_preferencia UNIQUE (id_usuario, evento, canal)
);

-- =====================================================================
--  3. CONVENIOS, CAMPAÑAS Y SEGMENTOS
-- =====================================================================
CREATE TABLE convenio (
  id_convenio bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  entidad     varchar(150) NOT NULL,
  tipo        varchar(40)  NOT NULL,
  vigencia    date                                     -- vigente hasta; vacío = sin fecha de fin
);

CREATE TABLE campana (
  id_campana bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nombre     varchar(150) NOT NULL,
  inicio     date NOT NULL,
  fin        date NOT NULL,
  estado     varchar(12) NOT NULL DEFAULT 'BORRADOR',
  creado_por bigint NOT NULL REFERENCES usuario(id_usuario),
  creado_en  timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT ck_campana_estado CHECK (estado IN ('BORRADOR','ACTIVA','SUSPENDIDA','FINALIZADA')),
  CONSTRAINT ck_campana_fechas CHECK (fin >= inicio)
);

CREATE TABLE segmento (
  id_segmento bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  criterio    varchar(20)  NOT NULL,
  valor       varchar(100) NOT NULL,
  CONSTRAINT ck_segmento_criterio CHECK (criterio IN ('RANGO_EDAD','TIPO_SOCIO','PRODUCTO','AGENCIA'))
);

CREATE TABLE campana_segmento (
  id_campana_segmento bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_campana          bigint NOT NULL REFERENCES campana(id_campana),
  id_segmento         bigint NOT NULL REFERENCES segmento(id_segmento),
  CONSTRAINT uq_campana_segmento UNIQUE (id_campana, id_segmento)
);

-- =====================================================================
--  4. REFERIDOS
-- =====================================================================
CREATE TABLE codigo_referido (
  id_codigo bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_socio  bigint NOT NULL REFERENCES socio(id_usuario),
  codigo    varchar(16) NOT NULL UNIQUE,               -- aleatorio, no secuencial
  estado    varchar(10) NOT NULL DEFAULT 'ACTIVO',
  CONSTRAINT ck_codigo_estado CHECK (estado IN ('ACTIVO','INACTIVO'))
);
-- Un socio puede tener varios códigos en el tiempo, pero solo uno activo
CREATE UNIQUE INDEX uq_codigo_activo_por_socio ON codigo_referido (id_socio) WHERE estado = 'ACTIVO';

CREATE TABLE prospecto (
  id_prospecto        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  identificacion_hash varchar(64),                      -- huella (SHA-256) de la cédula; no se guarda la cédula
  contacto            varchar(254) NOT NULL,            -- teléfono o correo
  estado              varchar(20)  NOT NULL DEFAULT 'REGISTRADO',
  creado_en           timestamptz  NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX uq_prospecto_identificacion ON prospecto (identificacion_hash) WHERE identificacion_hash IS NOT NULL;

CREATE TABLE referido (
  id_referido  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_codigo    bigint NOT NULL REFERENCES codigo_referido(id_codigo),
  id_prospecto bigint NOT NULL REFERENCES prospecto(id_prospecto),
  id_campana   bigint REFERENCES campana(id_campana),   -- opcional: "cuando corresponda" (RF-03-2)
  estado       varchar(15) NOT NULL DEFAULT 'REGISTRADO',
  creado_en    timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT ck_referido_estado CHECK (estado IN
    ('REGISTRADO','CONFIRMADO','EN_SEGUIMIENTO','CONVERTIDO','RECHAZADO','EXPIRADO'))
);
-- Un prospecto no puede tener dos referidos activos a la vez (RF-03-5)
CREATE UNIQUE INDEX uq_referido_prospecto_activo ON referido (id_prospecto)
  WHERE estado IN ('REGISTRADO','CONFIRMADO','EN_SEGUIMIENTO','CONVERTIDO');

CREATE TABLE conversion (
  id_conversion    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_referido      bigint NOT NULL UNIQUE REFERENCES referido(id_referido),  -- una sola conversión por referido (RF-03-3)
  tipo_evento      varchar(25) NOT NULL,
  fecha_validacion timestamptz NOT NULL DEFAULT now(),
  validado_por     bigint NOT NULL REFERENCES usuario(id_usuario),
  CONSTRAINT ck_conversion_tipo CHECK (tipo_evento IN ('APERTURA_CUENTA','PRODUCTO_CREDITICIO'))
);

-- =====================================================================
--  5. GAMIFICACIÓN
-- =====================================================================
CREATE TABLE regla_puntos (
  id_regla      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  accion        varchar(30) NOT NULL,
  puntos        integer     NOT NULL,
  vigente_desde date        NOT NULL,
  vigente_hasta date,
  CONSTRAINT ck_regla_accion CHECK (accion IN
    ('CONVERSION_REFERIDO','CAPACITACION_APROBADA','ASISTENCIA_TALLER','JUEGO','RETO')),
  CONSTRAINT ck_regla_puntos CHECK (puntos > 0),
  CONSTRAINT ck_regla_fechas CHECK (vigente_hasta IS NULL OR vigente_hasta >= vigente_desde)
);

-- Libro de movimientos: inmutable. El saldo se calcula sumando movimientos (RF-05-6).
CREATE TABLE movimiento_puntos (
  id_movimiento bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_socio      bigint NOT NULL REFERENCES socio(id_usuario),
  id_regla      bigint REFERENCES regla_puntos(id_regla),   -- vacío en canjes y ajustes
  tipo          varchar(12) NOT NULL,
  cantidad      integer     NOT NULL,
  origen_tipo   varchar(12) NOT NULL,
  origen_id     bigint      NOT NULL,
  creado_en     timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT ck_movimiento_tipo CHECK (tipo IN ('ACREDITACION','RESERVA','DESCUENTO','LIBERACION','REVERSO')),
  CONSTRAINT ck_movimiento_cantidad CHECK (cantidad > 0),
  CONSTRAINT ck_movimiento_origen CHECK (origen_tipo IN
    ('CONVERSION','CAPACITACION','TALLER','JUEGO','RETO','CANJE','AJUSTE'))
);
-- UQ parcial (RF-05-2, RNF-12): una misma acción no puede acreditarse, reservarse,
-- descontarse ni liberarse dos veces. Los reversos y ajustes quedan fuera.
CREATE UNIQUE INDEX uq_movimiento_origen ON movimiento_puntos (origen_tipo, origen_id, tipo)
  WHERE tipo IN ('ACREDITACION','RESERVA','DESCUENTO','LIBERACION');
CREATE INDEX ix_movimiento_socio ON movimiento_puntos (id_socio, creado_en);
CREATE TRIGGER trg_movimiento_solo_insercion
  BEFORE UPDATE OR DELETE ON movimiento_puntos
  FOR EACH ROW EXECUTE FUNCTION bloquear_modificacion();

CREATE TABLE nivel (
  id_nivel      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nombre        varchar(60) NOT NULL UNIQUE,
  umbral_puntos integer     NOT NULL UNIQUE,
  CONSTRAINT ck_nivel_umbral CHECK (umbral_puntos >= 0)
);

CREATE TABLE insignia (
  id_insignia bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nombre      varchar(80)  NOT NULL UNIQUE,
  criterio    varchar(300) NOT NULL
);

CREATE TABLE socio_insignia (
  id_socio_insignia bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_socio          bigint NOT NULL REFERENCES socio(id_usuario),
  id_insignia       bigint NOT NULL REFERENCES insignia(id_insignia),
  fecha_obtencion   timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_socio_insignia UNIQUE (id_socio, id_insignia)
);

-- =====================================================================
--  6. FORMACIÓN (CAPACITACIONES Y CERTIFICADOS)
-- =====================================================================
CREATE TABLE capacitacion (
  id_capacitacion bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  titulo          varchar(200) NOT NULL,
  modalidad       varchar(20)  NOT NULL,
  estado          varchar(12)  NOT NULL DEFAULT 'BORRADOR'
);

CREATE TABLE unidad (
  id_unidad       bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_capacitacion bigint NOT NULL REFERENCES capacitacion(id_capacitacion),
  orden           smallint NOT NULL,
  titulo          varchar(200) NOT NULL,
  CONSTRAINT uq_unidad_orden UNIQUE (id_capacitacion, orden)
);

CREATE TABLE inscripcion (
  id_inscripcion  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_socio        bigint NOT NULL REFERENCES socio(id_usuario),
  id_capacitacion bigint NOT NULL REFERENCES capacitacion(id_capacitacion),
  estado          varchar(12) NOT NULL DEFAULT 'INSCRITO',
  creado_en       timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_inscripcion UNIQUE (id_socio, id_capacitacion)
);

CREATE TABLE progreso (
  id_progreso    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_inscripcion bigint NOT NULL REFERENCES inscripcion(id_inscripcion),
  id_unidad      bigint NOT NULL REFERENCES unidad(id_unidad),
  porcentaje     numeric(5,2) NOT NULL DEFAULT 0,
  CONSTRAINT ck_progreso_porcentaje CHECK (porcentaje BETWEEN 0 AND 100),
  CONSTRAINT uq_progreso UNIQUE (id_inscripcion, id_unidad)
);

CREATE TABLE evaluacion (
  id_evaluacion   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_capacitacion bigint NOT NULL REFERENCES capacitacion(id_capacitacion),
  nota_minima     numeric(5,2) NOT NULL,
  CONSTRAINT ck_evaluacion_nota CHECK (nota_minima >= 0)
);

CREATE TABLE intento_evaluacion (
  id_intento     bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_inscripcion bigint NOT NULL REFERENCES inscripcion(id_inscripcion),
  id_evaluacion  bigint NOT NULL REFERENCES evaluacion(id_evaluacion),
  nota           numeric(5,2),                          -- vacía hasta que termina el intento
  aprobado       boolean,
  CONSTRAINT ck_intento_nota CHECK (nota IS NULL OR nota >= 0)
);

CREATE TABLE certificado (
  id_certificado      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_inscripcion      bigint NOT NULL UNIQUE REFERENCES inscripcion(id_inscripcion),  -- 0..1 por inscripción
  codigo_verificacion varchar(32) NOT NULL UNIQUE,      -- único y no secuencial (RNF-16)
  emitido_en          timestamptz NOT NULL DEFAULT now()
);

-- =====================================================================
--  7. SORTEOS Y CANJES
-- =====================================================================
CREATE TABLE sorteo (
  id_sorteo  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_campana bigint NOT NULL REFERENCES campana(id_campana),
  premio     varchar(200) NOT NULL,
  fecha      timestamptz  NOT NULL,
  estado     varchar(12)  NOT NULL DEFAULT 'BORRADOR'
);

CREATE TABLE participacion_sorteo (
  id_participacion bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_sorteo        bigint NOT NULL REFERENCES sorteo(id_sorteo),
  id_socio         bigint NOT NULL REFERENCES socio(id_usuario),
  origen_tipo      varchar(20) NOT NULL,
  origen_id        bigint      NOT NULL,
  creado_en        timestamptz NOT NULL DEFAULT now(),
  -- sin duplicados por la misma actividad (RF-07-2)
  CONSTRAINT uq_participacion_origen UNIQUE (id_sorteo, origen_tipo, origen_id),
  -- permite que ganador verifique que la participación es de su mismo sorteo
  CONSTRAINT uq_participacion_sorteo UNIQUE (id_participacion, id_sorteo)
);

CREATE TABLE ganador (
  id_ganador       bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_sorteo        bigint NOT NULL REFERENCES sorteo(id_sorteo),
  id_participacion bigint NOT NULL UNIQUE,              -- 0..1 ganador por participación
  posicion         smallint NOT NULL,
  fecha            timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT fk_ganador_participacion FOREIGN KEY (id_participacion, id_sorteo)
    REFERENCES participacion_sorteo (id_participacion, id_sorteo),
  CONSTRAINT uq_ganador_posicion UNIQUE (id_sorteo, posicion),
  CONSTRAINT ck_ganador_posicion CHECK (posicion > 0)
);

CREATE TABLE beneficio (
  id_beneficio bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_convenio  bigint REFERENCES convenio(id_convenio),  -- opcional
  nombre       varchar(150) NOT NULL,
  costo_puntos integer NOT NULL,
  stock        integer,                                  -- vacío = ilimitado
  CONSTRAINT ck_beneficio_costo CHECK (costo_puntos > 0),
  CONSTRAINT ck_beneficio_stock CHECK (stock IS NULL OR stock >= 0)
);

CREATE TABLE canje (
  id_canje      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_socio      bigint NOT NULL REFERENCES socio(id_usuario),
  id_beneficio  bigint NOT NULL REFERENCES beneficio(id_beneficio),
  estado        varchar(10) NOT NULL DEFAULT 'PENDIENTE',
  aprobado_por  bigint REFERENCES usuario(id_usuario),   -- vacío mientras esté pendiente
  fecha_entrega timestamptz,
  creado_en     timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT ck_canje_estado CHECK (estado IN ('PENDIENTE','APROBADA','RECHAZADA','ENTREGADA'))
);

-- =====================================================================
--  8. CONTENIDO, COMUNIDAD Y BIENESTAR
-- =====================================================================
CREATE TABLE contenido (
  id_contenido bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  autor_id     bigint NOT NULL REFERENCES usuario(id_usuario),
  tipo         varchar(20)  NOT NULL,
  titulo       varchar(200) NOT NULL,
  estado       varchar(12)  NOT NULL DEFAULT 'BORRADOR'
);

CREATE TABLE material (
  id_material  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_contenido bigint NOT NULL REFERENCES contenido(id_contenido),
  ruta_archivo varchar(500) NOT NULL,
  tipo_archivo varchar(100) NOT NULL
);

CREATE TABLE publicacion (
  id_publicacion     bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_usuario         bigint NOT NULL REFERENCES usuario(id_usuario),
  texto              text NOT NULL,
  estado_moderacion  varchar(12) NOT NULL DEFAULT 'VISIBLE',
  creado_en          timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE comentario (
  id_comentario  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_publicacion bigint NOT NULL REFERENCES publicacion(id_publicacion),
  id_usuario     bigint NOT NULL REFERENCES usuario(id_usuario),
  texto          text NOT NULL,
  estado         varchar(12) NOT NULL DEFAULT 'VISIBLE',
  creado_en      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE reaccion (
  id_reaccion    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_publicacion bigint NOT NULL REFERENCES publicacion(id_publicacion),
  id_usuario     bigint NOT NULL REFERENCES usuario(id_usuario),
  tipo           varchar(20) NOT NULL,
  CONSTRAINT uq_reaccion UNIQUE (id_publicacion, id_usuario)   -- una reacción por persona
);

CREATE TABLE recurso_bienestar (
  id_recurso   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_convenio  bigint REFERENCES convenio(id_convenio),   -- opcional
  titulo       varchar(200) NOT NULL,
  categoria    varchar(60)  NOT NULL,
  id_contenido bigint NOT NULL REFERENCES contenido(id_contenido)
);

-- =====================================================================
--  9. JUEGOS Y RETOS
-- =====================================================================
CREATE TABLE juego (
  id_juego     bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nombre       varchar(150) NOT NULL,
  tipo         varchar(16)  NOT NULL,
  estado       varchar(10)  NOT NULL DEFAULT 'INACTIVO',
  max_intentos smallint     NOT NULL,
  CONSTRAINT ck_juego_tipo CHECK (tipo IN ('TRIVIA','VERDADERO_FALSO','EMPAREJAR')),
  CONSTRAINT ck_juego_estado CHECK (estado IN ('ACTIVO','INACTIVO')),
  CONSTRAINT ck_juego_intentos CHECK (max_intentos > 0)
);

CREATE TABLE partida (
  id_partida    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_juego      bigint NOT NULL REFERENCES juego(id_juego),
  id_socio      bigint NOT NULL REFERENCES socio(id_usuario),
  puntuacion    numeric(6,2),                             -- vacía hasta que termina
  finalizada_en timestamptz
);

CREATE TABLE reto (
  id_reto  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  objetivo varchar(200) NOT NULL,
  meta     integer NOT NULL,
  inicio   date NOT NULL,
  fin      date NOT NULL,
  CONSTRAINT ck_reto_meta CHECK (meta > 0),
  CONSTRAINT ck_reto_fechas CHECK (fin >= inicio)
);

CREATE TABLE progreso_reto (
  id_progreso_reto bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_reto          bigint NOT NULL REFERENCES reto(id_reto),
  id_socio         bigint NOT NULL REFERENCES socio(id_usuario),
  avance           integer NOT NULL DEFAULT 0,
  completado_en    timestamptz,
  CONSTRAINT ck_progreso_reto_avance CHECK (avance >= 0),
  CONSTRAINT uq_progreso_reto UNIQUE (id_reto, id_socio)
);

-- =====================================================================
--  ÍNDICES sobre las claves foráneas (acelera las consultas y los JOIN)
-- =====================================================================
CREATE INDEX ix_usuario_rol_rol          ON usuario_rol (id_rol);
CREATE INDEX ix_rol_permiso_permiso      ON rol_permiso (id_permiso);
CREATE INDEX ix_consentimiento_usuario   ON consentimiento (id_usuario);
CREATE INDEX ix_sesion_usuario           ON sesion (id_usuario);
CREATE INDEX ix_auditoria_usuario        ON auditoria (id_usuario);
CREATE INDEX ix_auditoria_entidad        ON auditoria (entidad, registro_id);
CREATE INDEX ix_auditoria_fecha          ON auditoria (fecha);
CREATE INDEX ix_notificacion_usuario     ON notificacion (id_usuario, creado_en);
CREATE INDEX ix_notificacion_plantilla   ON notificacion (id_plantilla);
CREATE INDEX ix_campana_creado_por       ON campana (creado_por);
CREATE INDEX ix_campana_segmento_seg     ON campana_segmento (id_segmento);
CREATE INDEX ix_codigo_socio             ON codigo_referido (id_socio);
CREATE INDEX ix_referido_codigo          ON referido (id_codigo);
CREATE INDEX ix_referido_campana         ON referido (id_campana);
CREATE INDEX ix_movimiento_regla         ON movimiento_puntos (id_regla);
CREATE INDEX ix_socio_insignia_insignia  ON socio_insignia (id_insignia);
CREATE INDEX ix_inscripcion_capacitacion ON inscripcion (id_capacitacion);
CREATE INDEX ix_progreso_unidad          ON progreso (id_unidad);
CREATE INDEX ix_evaluacion_capacitacion  ON evaluacion (id_capacitacion);
CREATE INDEX ix_intento_inscripcion      ON intento_evaluacion (id_inscripcion);
CREATE INDEX ix_intento_evaluacion       ON intento_evaluacion (id_evaluacion);
CREATE INDEX ix_sorteo_campana           ON sorteo (id_campana);
CREATE INDEX ix_participacion_socio      ON participacion_sorteo (id_socio);
CREATE INDEX ix_beneficio_convenio       ON beneficio (id_convenio);
CREATE INDEX ix_canje_socio              ON canje (id_socio);
CREATE INDEX ix_canje_beneficio          ON canje (id_beneficio);
CREATE INDEX ix_canje_aprobado_por       ON canje (aprobado_por);
CREATE INDEX ix_contenido_autor          ON contenido (autor_id);
CREATE INDEX ix_material_contenido       ON material (id_contenido);
CREATE INDEX ix_publicacion_usuario      ON publicacion (id_usuario);
CREATE INDEX ix_comentario_publicacion   ON comentario (id_publicacion);
CREATE INDEX ix_comentario_usuario       ON comentario (id_usuario);
CREATE INDEX ix_reaccion_usuario         ON reaccion (id_usuario);
CREATE INDEX ix_recurso_convenio         ON recurso_bienestar (id_convenio);
CREATE INDEX ix_recurso_contenido        ON recurso_bienestar (id_contenido);
CREATE INDEX ix_partida_juego            ON partida (id_juego);
CREATE INDEX ix_partida_socio            ON partida (id_socio);
CREATE INDEX ix_progreso_reto_socio      ON progreso_reto (id_socio);
CREATE INDEX ix_conversion_validado_por  ON conversion (validado_por);

-- =====================================================================
--  DATOS INICIALES: roles base definidos en RF-02-5
-- =====================================================================
INSERT INTO rol (nombre) VALUES
  ('Socio'),
  ('Administrador'),
  ('Responsable de Marketing'),
  ('Responsable de Responsabilidad Social'),
  ('Gestor de contenidos');
