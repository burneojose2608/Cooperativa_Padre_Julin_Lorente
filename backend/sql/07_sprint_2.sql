-- Sprint 2: actualización aditiva, transaccional y repetible sobre una base existente.
BEGIN;
SELECT pg_advisory_xact_lock(20261117, 2);
DO $$ BEGIN
  IF current_database() IN ('postgres','template0','template1') THEN
    RAISE EXCEPTION 'Selecciona la base de la cooperativa antes de actualizar.';
  END IF;
END $$;
CREATE TABLE IF NOT EXISTS version_esquema (version varchar(60) PRIMARY KEY, aplicada_en timestamptz DEFAULT now());
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS foto varchar(500) NOT NULL DEFAULT '';
ALTER TABLE auditoria ADD COLUMN IF NOT EXISTS detalle jsonb NOT NULL DEFAULT '{}';
ALTER TABLE historial_estado ADD COLUMN IF NOT EXISTS motivo text NOT NULL DEFAULT '';
ALTER TABLE permiso ADD COLUMN IF NOT EXISTS descripcion varchar(200) NOT NULL DEFAULT '';
ALTER TABLE regla_puntos ADD COLUMN IF NOT EXISTS limite_periodo integer NOT NULL DEFAULT 1 CHECK (limite_periodo > 0);
ALTER TABLE regla_puntos ADD COLUMN IF NOT EXISTS periodo varchar(10) NOT NULL DEFAULT 'DIA' CHECK (periodo IN ('DIA','MES','ANIO'));
ALTER TABLE regla_puntos ADD COLUMN IF NOT EXISTS version varchar(40) NOT NULL DEFAULT 'inicial';
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS cuerpo text NOT NULL DEFAULT '';
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS categoria varchar(100) NOT NULL DEFAULT '';
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS desde date;
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS hasta date;
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS requiere_aprobacion boolean NOT NULL DEFAULT false;
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS actualizado_en timestamptz NOT NULL DEFAULT now();
ALTER TABLE contenido ADD COLUMN IF NOT EXISTS motivo_retiro text NOT NULL DEFAULT '';
ALTER TABLE material ALTER COLUMN id_contenido DROP NOT NULL;
ALTER TABLE material ADD COLUMN IF NOT EXISTS titulo varchar(200) NOT NULL DEFAULT '';
ALTER TABLE material ADD COLUMN IF NOT EXISTS categoria varchar(100) NOT NULL DEFAULT '';
ALTER TABLE material ADD COLUMN IF NOT EXISTS tamano_bytes integer NOT NULL DEFAULT 0;
ALTER TABLE material ADD COLUMN IF NOT EXISTS autor_id bigint REFERENCES usuario(id_usuario);
CREATE TABLE IF NOT EXISTS material_modulo (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_material bigint NOT NULL REFERENCES material(id_material) ON DELETE CASCADE,
  id_unidad bigint NOT NULL REFERENCES unidad(id_unidad), UNIQUE(id_material,id_unidad)
);
ALTER TABLE notificacion ADD COLUMN IF NOT EXISTS evento varchar(40) NOT NULL DEFAULT '';
ALTER TABLE notificacion ADD COLUMN IF NOT EXISTS titulo varchar(150) NOT NULL DEFAULT '';
ALTER TABLE notificacion ADD COLUMN IF NOT EXISTS mensaje text NOT NULL DEFAULT '';
ALTER TABLE notificacion ADD COLUMN IF NOT EXISTS leida_en timestamptz;
ALTER TABLE notificacion ADD COLUMN IF NOT EXISTS clave_evento varchar(160);
CREATE UNIQUE INDEX IF NOT EXISTS uq_notificacion_evento ON notificacion(id_usuario,clave_evento) WHERE clave_evento IS NOT NULL;
CREATE TABLE IF NOT EXISTS envio_notificacion (
  id_envio bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_notificacion bigint NOT NULL REFERENCES notificacion(id_notificacion),
  canal varchar(8) NOT NULL CHECK (canal IN ('INTERNA','CORREO')),
  estado varchar(12) NOT NULL DEFAULT 'PENDIENTE',
  intentos integer NOT NULL DEFAULT 0,
  enviada_en timestamptz, ultimo_error text NOT NULL DEFAULT '',
  disponible_en timestamptz NOT NULL DEFAULT now(),
  reservado_hasta timestamptz, reserva uuid,
  UNIQUE(id_notificacion,canal)
);
CREATE INDEX IF NOT EXISTS ix_envio_pendiente ON envio_notificacion(estado,disponible_en);
CREATE TABLE IF NOT EXISTS aviso_contenido (
  id_aviso bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_contenido bigint NOT NULL REFERENCES contenido(id_contenido),
  version timestamptz NOT NULL,
  disponible_en timestamptz NOT NULL,
  procesado_en timestamptz,
  UNIQUE(id_contenido,version)
);
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM version_esquema WHERE version='sprint-2') THEN
    INSERT INTO permiso(modulo,accion,descripcion) VALUES
      ('referidos','compartir','Obtener y compartir el código de referido'),
      ('puntos','configurar','Configurar versiones de reglas de puntos'),
      ('contenidos','gestionar','Crear y actualizar contenidos institucionales'),
      ('contenidos','publicar','Publicar, programar y retirar contenidos'),
      ('materiales','gestionar','Gestionar y reutilizar material educativo')
    ON CONFLICT (modulo,accion) DO UPDATE SET descripcion=EXCLUDED.descripcion;
    INSERT INTO rol_permiso(id_rol,id_permiso)
    SELECT r.id_rol,p.id_permiso FROM rol r CROSS JOIN permiso p WHERE
      (r.nombre='Socio' AND p.modulo='referidos' AND p.accion='compartir') OR
      (r.nombre='Administrador' AND p.modulo='puntos' AND p.accion='configurar') OR
      (r.nombre='Gestor de contenidos' AND p.modulo IN ('contenidos','materiales')) OR
      (r.nombre='Responsable de Responsabilidad Social' AND p.modulo='materiales')
    ON CONFLICT DO NOTHING;
    INSERT INTO version_esquema(version) VALUES ('sprint-2');
  END IF;
END $$;
COMMIT;
