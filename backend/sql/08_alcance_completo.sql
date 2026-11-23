-- Evolución aditiva para los módulos de los sprints 3 a 5.
BEGIN;
SELECT pg_advisory_xact_lock(20261120, 8);
DO $$ BEGIN
 IF current_database() IN ('postgres','template0','template1') THEN
  RAISE EXCEPTION 'Seleccione una base de proyecto o de pruebas';
 END IF;
END $$;
ALTER TABLE socio ADD COLUMN IF NOT EXISTS alias varchar(60) NOT NULL DEFAULT '';
ALTER TABLE socio ADD COLUMN IF NOT EXISTS ranking_publico boolean NOT NULL DEFAULT false;
ALTER TABLE socio ADD COLUMN IF NOT EXISTS segmento jsonb NOT NULL DEFAULT '{}';
ALTER TABLE campana ADD COLUMN IF NOT EXISTS condiciones text NOT NULL DEFAULT '';
ALTER TABLE campana ADD COLUMN IF NOT EXISTS segmentacion jsonb NOT NULL DEFAULT '{}';
ALTER TABLE prospecto ADD COLUMN IF NOT EXISTS producto varchar(150) NOT NULL DEFAULT '';
ALTER TABLE prospecto ADD COLUMN IF NOT EXISTS version_politica varchar(40) NOT NULL DEFAULT '1.0';
ALTER TABLE prospecto ADD COLUMN IF NOT EXISTS token_hash varchar(64);
ALTER TABLE prospecto ADD COLUMN IF NOT EXISTS expira_en timestamptz;
ALTER TABLE prospecto ADD COLUMN IF NOT EXISTS token_nonce varchar(100);
CREATE TABLE IF NOT EXISTS solicitud_contacto (
 id_solicitud bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 id_prospecto bigint NOT NULL UNIQUE REFERENCES prospecto(id_prospecto),
 estado varchar(12) NOT NULL DEFAULT 'PENDIENTE', intentos integer NOT NULL DEFAULT 0,
 disponible_en timestamptz NOT NULL DEFAULT now(), reservado_hasta timestamptz, reserva uuid
);
ALTER TABLE conversion ADD COLUMN IF NOT EXISTS monto_captado numeric(18,2) CHECK(monto_captado>=0);
ALTER TABLE conversion DROP CONSTRAINT IF EXISTS ck_conversion_tipo;
ALTER TABLE conversion ADD CONSTRAINT ck_conversion_tipo CHECK(tipo_evento IN ('APERTURA_CUENTA','PRODUCTO_CREDITICIO','TARJETA_ENTREGADA','SEGURO_CONTRATADO'));
CREATE TABLE IF NOT EXISTS gasto_campana (
 id_gasto bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 id_campana bigint NOT NULL REFERENCES campana(id_campana),
 fecha date NOT NULL, concepto varchar(300) NOT NULL, importe numeric(18,2) NOT NULL CHECK(importe>=0)
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_prospecto_correo ON prospecto(lower(correo)) WHERE correo IS NOT NULL AND correo<>'';
CREATE UNIQUE INDEX IF NOT EXISTS uq_prospecto_telefono ON prospecto(telefono) WHERE telefono IS NOT NULL AND telefono<>'';
CREATE TABLE IF NOT EXISTS actividad_validada (
 id_actividad bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 id_socio bigint NOT NULL REFERENCES socio(id_usuario),
 origen_tipo varchar(20) NOT NULL, origen_id bigint NOT NULL,
 validada_en timestamptz NOT NULL DEFAULT now(), UNIQUE(origen_tipo,origen_id)
);
ALTER TABLE movimiento_puntos ADD COLUMN IF NOT EXISTS motivo text NOT NULL DEFAULT '';
CREATE UNIQUE INDEX IF NOT EXISTS uq_reverso_origen ON movimiento_puntos(origen_tipo,origen_id,tipo) WHERE tipo='REVERSO';
ALTER TABLE insignia ADD COLUMN IF NOT EXISTS umbral integer NOT NULL DEFAULT 1 CHECK(umbral>0);
ALTER TABLE insignia ADD COLUMN IF NOT EXISTS icono varchar(100) NOT NULL DEFAULT '';
ALTER TABLE capacitacion ADD COLUMN IF NOT EXISTS descripcion text NOT NULL DEFAULT '';
ALTER TABLE capacitacion ADD COLUMN IF NOT EXISTS duracion integer NOT NULL DEFAULT 1 CHECK(duracion>0);
ALTER TABLE capacitacion ADD COLUMN IF NOT EXISTS requisitos text NOT NULL DEFAULT '';
ALTER TABLE evaluacion ADD COLUMN IF NOT EXISTS max_intentos integer NOT NULL DEFAULT 3 CHECK(max_intentos>0);
ALTER TABLE evaluacion ADD COLUMN IF NOT EXISTS preguntas jsonb NOT NULL DEFAULT '[]';
ALTER TABLE intento_evaluacion ADD COLUMN IF NOT EXISTS respuestas jsonb NOT NULL DEFAULT '[]';
ALTER TABLE taller ADD COLUMN IF NOT EXISTS modalidad varchar(20) NOT NULL DEFAULT 'PRESENCIAL';
ALTER TABLE taller ADD COLUMN IF NOT EXISTS lugar varchar(500) NOT NULL DEFAULT '';
ALTER TABLE taller ADD COLUMN IF NOT EXISTS duracion integer NOT NULL DEFAULT 1 CHECK(duracion>0);
ALTER TABLE beneficio ADD COLUMN IF NOT EXISTS descripcion text NOT NULL DEFAULT '';
ALTER TABLE beneficio ADD COLUMN IF NOT EXISTS condiciones text NOT NULL DEFAULT '';
ALTER TABLE beneficio ADD COLUMN IF NOT EXISTS desde date NOT NULL DEFAULT CURRENT_DATE;
ALTER TABLE beneficio ADD COLUMN IF NOT EXISTS hasta date;
ALTER TABLE beneficio ADD COLUMN IF NOT EXISTS activo boolean NOT NULL DEFAULT true;
ALTER TABLE canje ADD COLUMN IF NOT EXISTS clave uuid;
CREATE UNIQUE INDEX IF NOT EXISTS uq_canje_clave ON canje(id_socio,clave) WHERE clave IS NOT NULL;
ALTER TABLE convenio ADD COLUMN IF NOT EXISTS descripcion text NOT NULL DEFAULT '';
ALTER TABLE convenio ADD COLUMN IF NOT EXISTS condiciones text NOT NULL DEFAULT '';
ALTER TABLE convenio ADD COLUMN IF NOT EXISTS beneficio text NOT NULL DEFAULT '';
ALTER TABLE sorteo ADD COLUMN IF NOT EXISTS nombre varchar(150) NOT NULL DEFAULT '';
ALTER TABLE sorteo ADD COLUMN IF NOT EXISTS condiciones text NOT NULL DEFAULT '';
ALTER TABLE sorteo ADD COLUMN IF NOT EXISTS origen varchar(20) NOT NULL DEFAULT 'CONVERSION';
ALTER TABLE sorteo ADD COLUMN IF NOT EXISTS evidencia jsonb NOT NULL DEFAULT '{}';
ALTER TABLE juego ADD COLUMN IF NOT EXISTS instrucciones text NOT NULL DEFAULT '';
ALTER TABLE juego ADD COLUMN IF NOT EXISTS preguntas jsonb NOT NULL DEFAULT '[]';
ALTER TABLE juego ADD COLUMN IF NOT EXISTS nota_minima integer NOT NULL DEFAULT 60 CHECK(nota_minima BETWEEN 0 AND 100);
ALTER TABLE partida ADD COLUMN IF NOT EXISTS respuestas jsonb NOT NULL DEFAULT '[]';
ALTER TABLE reto ADD COLUMN IF NOT EXISTS actividad varchar(30) NOT NULL DEFAULT 'CAPACITACION';
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS aprobador_id bigint REFERENCES usuario(id_usuario);
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS aprobado_en timestamptz;
ALTER TABLE plantilla_notificacion ADD COLUMN IF NOT EXISTS canal varchar(8) NOT NULL DEFAULT 'TODOS' CHECK(canal IN ('TODOS','INTERNA','CORREO'));
ALTER TABLE notificacion ADD COLUMN IF NOT EXISTS mensaje_base text NOT NULL DEFAULT '';
ALTER TABLE publicacion ADD COLUMN IF NOT EXISTS imagen varchar(500) NOT NULL DEFAULT '';
CREATE TABLE IF NOT EXISTS reporte_comunidad (
 id_reporte bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 id_publicacion bigint REFERENCES publicacion(id_publicacion),
 id_comentario bigint REFERENCES comentario(id_comentario),
 id_usuario bigint NOT NULL REFERENCES usuario(id_usuario),
 motivo text NOT NULL, creado_en timestamptz NOT NULL DEFAULT now(),
 resuelto_en timestamptz, resolucion text NOT NULL DEFAULT '',
 CHECK ((id_publicacion IS NULL) <> (id_comentario IS NULL))
);
CREATE TABLE IF NOT EXISTS suspension_comunidad (
 id_suspension bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 id_socio bigint NOT NULL REFERENCES socio(id_usuario),
 hasta timestamptz NOT NULL, motivo text NOT NULL, responsable_id bigint NOT NULL REFERENCES usuario(id_usuario)
);
DO $$ BEGIN
 IF NOT EXISTS (SELECT 1 FROM version_esquema WHERE version='alcance-3-5') THEN
  INSERT INTO permiso(modulo,accion,descripcion)
  SELECT m,'gestionar','Gestionar '||m FROM unnest(ARRAY['referidos','campanas','gamificacion','formacion','sorteos','recompensas','bienestar','juegos','comunidad','reportes','notificaciones']) AS m
  ON CONFLICT DO NOTHING;
  INSERT INTO permiso(modulo,accion,descripcion)
  SELECT m,'participar','Participar en '||m FROM unnest(ARRAY['referidos','campanas','gamificacion','formacion','sorteos','recompensas','bienestar','juegos','comunidad']) AS m
  ON CONFLICT DO NOTHING;
  INSERT INTO rol_permiso(id_rol,id_permiso)
  SELECT r.id_rol,p.id_permiso FROM rol r CROSS JOIN permiso p WHERE
   (r.nombre='Administrador' AND p.accion='gestionar' AND p.modulo IN ('referidos','campanas','gamificacion','formacion','sorteos','recompensas','bienestar','juegos','comunidad','reportes','notificaciones')) OR
   (r.nombre='Socio' AND p.accion='participar') OR
   (r.nombre='Responsable de Marketing' AND p.accion='gestionar' AND p.modulo IN ('referidos','campanas','sorteos','recompensas','reportes','juegos')) OR
   (r.nombre='Responsable de Responsabilidad Social' AND p.accion='gestionar' AND p.modulo IN ('campanas','formacion','bienestar','reportes')) OR
   (r.nombre='Gestor de contenidos' AND p.accion='gestionar' AND p.modulo IN ('formacion','juegos','comunidad','bienestar'))
  ON CONFLICT DO NOTHING;
  INSERT INTO version_esquema(version) VALUES('alcance-3-5');
 END IF;
END $$;
COMMIT;
