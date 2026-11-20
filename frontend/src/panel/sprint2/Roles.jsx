import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { PIAlerta, PICampanas, PICapacitacion, PIContenidos, PICupon, PIGuardar, PIModulos, PIOk, PIReferidos, PIRoles, PIBeneficios } from "../IconosPanel";
import { Aviso } from "./comunes";
import { useOperacion } from "./operaciones";
import "./usuarios.css";
import "./roles.css";

// Textos de apoyo y colores por rol (solo presentación; los permisos reales vienen del servidor).
const ROLES = [
  [/socio/i, "azul", PIReferidos, "Accede a sus beneficios, contenidos, campañas y programas."],
  [/admin/i, "ambar", PIRoles, "Gestión total del sistema, usuarios, parámetros y seguridad."],
  [/marketing/i, "morado", PICampanas, "Administra campañas, promociones y comunicación institucional."],
  [/social/i, "verde", PIBeneficios, "Gestiona programas, actividades y contenidos sociales."],
  [/contenido/i, "celeste", PIModulos, "Administra y publica el contenido educativo, informativo e institucional."],
];
const estiloRol = (nombre) => ROLES.find(([re]) => re.test(nombre)) ?? [null, "azul", PIRoles, ""];
const ICONOS = { "contenidos.gestionar": PIContenidos, "contenidos.publicar": PICampanas, "materiales.gestionar": PICapacitacion, "puntos.configurar": PIModulos, "referidos.compartir": PICupon };

function PermisosRol({ rol, permisos, recargar }) {
  const [ids, setIds] = useState(rol.permisos); const op = useOperacion(recargar);
  const [, color, Icono, descripcion] = estiloRol(rol.nombre);
  return <article className={`rp-rol rp-rol--${color}`}>
    <header className="rp-rol__cab"><span className="rp-rol__ico"><Icono /></span><div><h2>{rol.nombre}</h2>{descripcion && <p>{descripcion}</p>}</div></header>
    <form onSubmit={(e) => { e.preventDefault(); op.ejecutar(() => api.putProtegido(`/auth/administracion/roles/${rol.id}/permisos/`, { permisos: ids }), "Cambios guardados."); }}>
      <h3>Permisos del rol</h3>
      <ul className="rp-lista">{permisos.map((p) => { const I = ICONOS[p.codigo] ?? PIRoles; const activo = ids.includes(p.id);
        return <li key={p.id}><label title={p.codigo}><I className="rp-lista__ico" /><span>{p.descripcion || p.codigo}</span>
          <input type="checkbox" role="switch" aria-label={p.descripcion || p.codigo} checked={activo} onChange={(e) => setIds(e.target.checked ? [...ids, p.id] : ids.filter((id) => id !== p.id))} /><i className="rp-sw" aria-hidden="true" /></label></li>; })}</ul>
      <div className="rp-estado">{op.error ? <p className="alerta alerta--error" role="alert">{op.error}</p> : op.mensaje ? <p className="rp-ok" role="status"><PIOk aria-hidden="true" />{op.mensaje}</p> : null}</div>
      <button className="boton boton--azul rp-guardar" disabled={op.ocupado}><PIGuardar className="boton__ico" />{op.ocupado ? "Guardando…" : "Guardar permisos"}</button>
    </form></article>;
}
export default function Roles() {
  const r = useRecurso("/auth/administracion/roles/");
  return <div className="us rp">
    <div className="us-cab"><span className="us-cab__ico"><PIRoles /></span><div className="us-cab__txt"><h1>Roles y permisos</h1><p>Define los roles del sistema y gestiona los permisos asociados a cada uno.</p></div></div>
    <p className="us-nota"><PIAlerta aria-hidden="true" />La administración de cuentas y de permisos está reservada al Administrador. Los permisos controlan las operaciones disponibles en cada módulo. Los cambios se aplican desde la siguiente petición; asigna los roles a cada cuenta en Usuarios.</p>
    <Aviso error={r.error} />
    <div className="rp-grid">{r.datos?.roles.map((rol) => <PermisosRol key={rol.id} rol={rol} permisos={r.datos.permisos} recargar={r.recargar} />)}</div>
  </div>;
}
