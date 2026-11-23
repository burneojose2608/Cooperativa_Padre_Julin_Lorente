import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { PICampanas, PICapacitacion, PIContenidos, PICupon, PIEditar, PIGuardar, PIModulos, PIOk, PIReferidos, PIRoles, PIBeneficios } from "../IconosPanel";
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

export default function Roles() {
  const r = useRecurso("/auth/administracion/roles/");
  const [seleccion, setSeleccion] = useState(null);
  const [borrador, setBorrador] = useState(null);
  const [confirmados, setConfirmados] = useState({});
  const [ultimoGuardado, setUltimoGuardado] = useState(null);
  const op = useOperacion();
  const roles = r.datos?.roles ?? [];
  const rol = roles.find(({ id }) => id === seleccion) ?? roles[0];
  const asignados = confirmados[rol?.id] ?? rol?.permisos ?? [];
  const editando = borrador !== null;
  const permisos = (r.datos?.permisos ?? []).filter((p) => editando || asignados.includes(p.id));
  const [, color, Icono, descripcion] = estiloRol(rol?.nombre ?? "");

  async function guardar(e) {
    e.preventDefault();
    if (!editando || op.ocupado) return;
    const ids = borrador;
    if (await op.ejecutar(() => api.putProtegido(`/auth/administracion/roles/${rol.id}/permisos/`, { permisos: ids }), "Cambios guardados.")) {
      setConfirmados((anteriores) => ({ ...anteriores, [rol.id]: ids }));
      setUltimoGuardado(rol.id);
      setBorrador(null);
    }
  }

  return <div className="us rp">
    <div className="us-cab"><span className="us-cab__ico"><PIRoles aria-hidden="true" /></span><div className="us-cab__txt"><h1>Roles y permisos</h1><p>Consulta y administra los permisos de cada rol.</p></div></div>
    <Aviso error={r.error} />
    {!r.datos && !r.error && <p role="status">Cargando roles…</p>}
    {r.datos && !rol && <p>No hay roles disponibles.</p>}
    {rol && <>
      <label className="rp-selector">Rol
        <select value={rol.id} disabled={editando} onChange={(e) => setSeleccion(Number(e.target.value))}>
          {roles.map(({ id, nombre }) => <option key={id} value={id}>{nombre}</option>)}
        </select>
      </label>
      <section className={`rp-rol rp-rol--${color}`} aria-labelledby="rol-elegido">
        <header className="rp-rol__cab">
          <span className="rp-rol__ico"><Icono aria-hidden="true" /></span>
          <div><h2 id="rol-elegido">{rol.nombre}</h2>{descripcion && <p>{descripcion}</p>}</div>
          {!editando && <button type="button" className="boton boton--claro rp-editar" onClick={() => setBorrador(asignados)}>
            <PIEditar className="boton__ico" />Editar permisos
          </button>}
        </header>
        <form onSubmit={guardar}>
          <h3>{editando ? "Selecciona los permisos" : "Permisos asignados"}</h3>
          {editando && <p className="rp-ayuda">Los cambios se aplican desde la siguiente petición.</p>}
          {permisos.length ? <ul className="rp-lista">{permisos.map((p) => {
            const I = ICONOS[p.codigo] ?? PIRoles;
            const nombre = p.descripcion || p.codigo;
            return <li key={p.id}>{editando ? <label title={p.codigo}>
              <I className="rp-lista__ico" aria-hidden="true" /><span>{nombre}</span>
              <input type="checkbox" role="switch" aria-label={nombre} disabled={op.ocupado} checked={borrador.includes(p.id)}
                onChange={(e) => setBorrador(e.target.checked ? [...borrador, p.id] : borrador.filter((id) => id !== p.id))} />
              <i className="rp-sw" aria-hidden="true" />
            </label> : <div className="rp-permiso"><PIOk className="rp-lista__ico" aria-hidden="true" /><span>{nombre}</span></div>}</li>;
          })}</ul> : <p className="rp-ayuda">Este rol no tiene permisos asignados.</p>}
          <Aviso error={editando ? op.error : ""} mensaje={!editando && ultimoGuardado === rol.id ? op.mensaje : ""} />
          {editando && <div className="rp-acciones">
            <button type="button" className="boton boton--claro" disabled={op.ocupado} onClick={() => setBorrador(null)}>Cancelar</button>
            <button className="boton boton--azul" disabled={op.ocupado}><PIGuardar className="boton__ico" />{op.ocupado ? "Guardando…" : "Guardar permisos"}</button>
          </div>}
        </form>
      </section>
    </>}
  </div>;
}
