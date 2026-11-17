import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { Aviso } from "./comunes";
import { useOperacion } from "./operaciones";

function PermisosRol({ rol, permisos, recargar }) {
  const [ids, setIds] = useState(rol.permisos); const op = useOperacion(recargar);
  return <Tarjeta titulo={rol.nombre}><form className="s2-form" onSubmit={(e) => { e.preventDefault(); op.ejecutar(() => api.putProtegido(`/auth/administracion/roles/${rol.id}/permisos/`, { permisos: ids })); }}>
    {permisos.map((p) => <label className="s2-check" key={p.id}><input type="checkbox" checked={ids.includes(p.id)} onChange={(e) => setIds(e.target.checked ? [...ids, p.id] : ids.filter((id) => id !== p.id))} /><span>{p.descripcion || p.codigo}<small> · {p.codigo}</small></span></label>)}
    <Aviso {...op} /><button className="boton" disabled={op.ocupado}>Guardar permisos</button>
  </form></Tarjeta>;
}
export default function Roles() {
  const r = useRecurso("/auth/administracion/roles/");
  return <><TituloPagina titulo="Roles y permisos" sub="Los cambios se aplican en el servidor desde la siguiente petición. Asigna los roles a cada cuenta en Usuarios." />
    <p>La administración de cuentas y de permisos está reservada al Administrador. Los permisos configurables controlan las operaciones de negocio disponibles.</p>
    <Aviso error={r.error} /><div className="s2-columnas">{r.datos?.roles.map((rol) => <PermisosRol key={rol.id} rol={rol} permisos={r.datos.permisos} recargar={r.recargar} />)}</div></>;
}
