import { useEffect, useState } from "react";
import { api } from "../../api/cliente";
import { FotoCuentaAdministrada } from "../../components/FotoPerfil";
import useRecurso from "../../hooks/useRecurso";
import { PIAlerta, PIBuscar, PIGuardar, PIInvitar, PIOk, PIUsuarios, PIValidar } from "../IconosPanel";
import { Aviso } from "./comunes";
import Lateral from "./Lateral";
import { useOperacion } from "./operaciones";
import "./usuarios.css";

const ESTADOS = ["ACTIVA", "SUSPENDIDA", "DESACTIVADA"];
const ETIQUETA = { ACTIVA: "Activa", SUSPENDIDA: "Suspendida", DESACTIVADA: "Desactivada" };

const Campo = ({ etiqueta, ayuda, ancho, children, ...props }) => (
  <label className={ancho ? "us-campo us-campo--ancho" : "us-campo"}><span>{etiqueta}</span>{children || <input {...props} />}{ayuda && <small>{ayuda}</small>}</label>
);
const Insignia = ({ estado }) => <span className={`us-estado us-estado--${estado.toLowerCase()}`}>{ETIQUETA[estado] ?? estado}</span>;

function CrearCuenta({ roles, alCerrar, recargar }) {
  const [datos, setDatos] = useState({ nombre: "", apellido: "", cedula: "", username: "", correo: "", telefono: "", fecha_nacimiento: "", clave: "", rol: "" });
  const op = useOperacion(recargar);
  const poner = (k) => (e) => setDatos({ ...datos, [k]: e.target.value });
  async function enviar(e) {
    e.preventDefault();
    if (await op.ejecutar(() => api.postProtegido("/auth/administracion/usuarios/", datos), "Cuenta creada.")) alCerrar();
  }
  return <Lateral titulo="Crear cuenta interna" subtitulo="Para el personal de la cooperativa. El socio se registra por su cuenta." alCerrar={alCerrar}
    cabeza={<span className="us-cab-ico"><PIInvitar /></span>}
    pie={<><button type="button" className="boton boton--claro" onClick={alCerrar}>Cancelar</button>
      <button form="form-crear" className="boton boton--amarillo" disabled={op.ocupado}><PIOk className="boton__ico" />Crear cuenta</button></>}>
    <form id="form-crear" className="us-form" onSubmit={enviar} autoComplete="off">
      <div className="us-rejilla">
        <Campo etiqueta="Nombres" name="nombre" autoComplete="off" required value={datos.nombre} onChange={poner("nombre")} />
        <Campo etiqueta="Apellidos" name="apellido" autoComplete="off" required value={datos.apellido} onChange={poner("apellido")} />
        <Campo etiqueta="Cédula" name="cedula" inputMode="numeric" autoComplete="off" required value={datos.cedula} onChange={poner("cedula")} />
        <Campo etiqueta="Fecha de nacimiento" name="fecha_nacimiento" type="date" autoComplete="off" required value={datos.fecha_nacimiento} onChange={poner("fecha_nacimiento")} />
        <Campo etiqueta="Correo electrónico" name="correo" type="email" autoComplete="off" required value={datos.correo} onChange={poner("correo")} />
        <Campo etiqueta="Teléfono" name="telefono" inputMode="tel" autoComplete="off" required value={datos.telefono} onChange={poner("telefono")} />
      </div>
      <h3 className="us-sub">Acceso a la plataforma</h3>
      <div className="us-rejilla">
        <Campo etiqueta="Usuario" name="nuevo_usuario" autoComplete="off" required value={datos.username} onChange={poner("username")} />
        <Campo etiqueta="Contraseña inicial" name="nueva_clave" type="password" autoComplete="new-password" required value={datos.clave} onChange={poner("clave")} />
        <Campo etiqueta="Rol" ancho><select required value={datos.rol} onChange={poner("rol")}>
          <option value="">Selecciona un rol interno</option>{roles.filter((r) => r.nombre !== "Socio").map((r) => <option key={r.id}>{r.nombre}</option>)}</select></Campo>
      </div>
      <Aviso {...op} />
    </form>
  </Lateral>;
}

const PESTANAS = [["contacto", "Contacto"], ["roles", "Roles"], ["estado", "Estado"]];

function EditarCuenta({ cuenta, roles, alCerrar, recargar }) {
  const [pestana, setPestana] = useState("contacto");
  const [correo, setCorreo] = useState(cuenta.correo); const [telefono, setTelefono] = useState(cuenta.telefono);
  const [estado, setEstado] = useState(cuenta.estado); const [motivo, setMotivo] = useState("");
  const [seleccionados, setSeleccionados] = useState(roles.filter((r) => cuenta.roles.includes(r.nombre)).map((r) => r.id));
  const op = useOperacion(recargar);
  const detalle = useRecurso(`/auth/administracion/usuarios/${cuenta.id}/`);
  const [actual, setActual] = useState(cuenta.estado);
  const guardar = { contacto: "Guardar contacto", roles: "Guardar roles", estado: "Aplicar estado" }[pestana];
  function enviar(e) {
    e.preventDefault();
    if (pestana === "contacto") op.ejecutar(() => api.patchProtegido(`/auth/administracion/usuarios/${cuenta.id}/`, { correo, telefono }), "Contacto guardado.");
    else if (pestana === "roles") op.ejecutar(() => api.putProtegido(`/auth/administracion/usuarios/${cuenta.id}/roles/`, { roles: seleccionados }), "Roles guardados.");
    else op.ejecutar(async () => { await api.postProtegido(`/auth/administracion/usuarios/${cuenta.id}/estado/`, { estado, motivo }); setActual(estado); setMotivo(""); detalle.recargar(); }, "Estado actualizado.");
  }
  return <Lateral titulo={`${cuenta.nombre} ${cuenta.apellido}`} subtitulo={`@${cuenta.username} · Cédula ${cuenta.cedula}`} alCerrar={alCerrar}
    cabeza={<FotoCuentaAdministrada cuenta={cuenta} grande />}
    pie={<><button type="button" className="boton boton--claro" onClick={alCerrar}>Cerrar</button>
      <button form="form-editar" className="boton boton--amarillo" disabled={op.ocupado}><PIGuardar className="boton__ico" />{guardar}</button></>}>
    <div className="us-actual"><span>Estado actual</span><Insignia estado={actual} /></div>
    <div className="us-pestanas" role="tablist" aria-label="Secciones de la cuenta">
      {PESTANAS.map(([k, etq]) => <button key={k} type="button" role="tab" aria-selected={pestana === k} className={pestana === k ? "on" : ""} onClick={() => setPestana(k)}>{etq}</button>)}</div>
    <form id="form-editar" className="us-form" onSubmit={enviar}>
      {pestana === "contacto" && <>
        <Campo etiqueta="Correo electrónico" type="email" required value={correo} onChange={(e) => setCorreo(e.target.value)} />
        <Campo etiqueta="Teléfono" required value={telefono} onChange={(e) => setTelefono(e.target.value)} /></>}
      {pestana === "roles" && <fieldset className="us-roles"><legend>Roles de la cuenta</legend>
        {roles.map((r) => <label className="us-rol" key={r.id}><input type="checkbox" checked={seleccionados.includes(r.id)}
          onChange={(e) => setSeleccionados(e.target.checked ? [...seleccionados, r.id] : seleccionados.filter((id) => id !== r.id))} />{r.nombre}</label>)}
        <p className="us-nota"><PIAlerta aria-hidden="true" />El rol Socio requiere una validación previa en «Validar socios».</p></fieldset>}
      {pestana === "estado" && <>
        <Campo etiqueta="Estado"><select value={estado} onChange={(e) => setEstado(e.target.value)}>{ESTADOS.map((v) => <option key={v} value={v}>{ETIQUETA[v]}</option>)}</select></Campo>
        <Campo etiqueta="Motivo del cambio" required maxLength={1000} value={motivo} onChange={(e) => setMotivo(e.target.value)} />
        <p className="us-nota"><PIAlerta aria-hidden="true" />Suspender o desactivar cierra las sesiones activas de la cuenta.</p></>}
      <Aviso {...op} />
    </form>
    {pestana === "estado" && <section className="us-historial"><h3 className="us-sub">Historial de estados</h3><Aviso error={detalle.error} />
      {detalle.datos?.historial.map((h) => <article key={h.fecha}><strong>{h.estado_anterior} → {h.estado_nuevo}</strong><p>{h.motivo}</p>
        <small>{new Date(h.fecha).toLocaleString("es-EC")} · Responsable #{h.usuario_id}</small></article>)}
      {detalle.datos && !detalle.datos.historial.length && <p className="us-vacio">Sin cambios de estado registrados.</p>}</section>}
  </Lateral>;
}

export default function Usuarios() {
  const [q, setQ] = useState(""); const [filtro, setFiltro] = useState(""); const [estado, setEstado] = useState(""); const [rol, setRol] = useState("");
  const [pagina, setPagina] = useState(1); const [editar, setEditar] = useState(null); const [crear, setCrear] = useState(false);
  useEffect(() => { const t = setTimeout(() => { setFiltro(q.trim()); setPagina(1); }, 350); return () => clearTimeout(t); }, [q]);
  const catalogo = useRecurso("/auth/administracion/roles/");
  const recurso = useRecurso(`/auth/administracion/usuarios/?q=${encodeURIComponent(filtro)}&estado=${estado}&rol=${encodeURIComponent(rol)}&pagina=${pagina}`);
  const recargarLista = recurso.recargar;
  useEffect(() => {
    window.addEventListener("focus", recargarLista);
    return () => window.removeEventListener("focus", recargarLista);
  }, [recargarLista]);
  const kTotal = useRecurso("/auth/administracion/usuarios/?pagina=1");
  const kActivas = useRecurso("/auth/administracion/usuarios/?estado=ACTIVA");
  const kSusp = useRecurso("/auth/administracion/usuarios/?estado=SUSPENDIDA");
  const recargarTodo = () => { recurso.recargar(); kTotal.recargar(); kActivas.recargar(); kSusp.recargar(); };
  const roles = catalogo.datos?.roles || [];
  const total = recurso.datos?.total ?? 0;
  return <div className="us">
    <div className="us-cab"><span className="us-cab__ico"><PIUsuarios /></span>
      <div className="us-cab__txt"><h1>Usuarios</h1><p>Consulta, crea y cambia estados con trazabilidad visible.</p></div>
      <button type="button" className="boton boton--amarillo" onClick={() => setCrear(true)}><PIInvitar className="boton__ico" />Crear cuenta interna</button></div>
    <Aviso error={recurso.error || catalogo.error} />
    <div className="us-kpis">
      <div className="us-kpi us-kpi--azul"><span><PIUsuarios /></span><div><strong>{kTotal.datos?.total ?? "—"}</strong><small>Usuarios</small></div></div>
      <div className="us-kpi us-kpi--verde"><span><PIValidar /></span><div><strong>{kActivas.datos?.total ?? "—"}</strong><small>Activos</small></div></div>
      <div className="us-kpi us-kpi--amarillo"><span><PIAlerta /></span><div><strong>{kSusp.datos?.total ?? "—"}</strong><small>Suspendidos</small></div></div>
    </div>
    <section className="us-tarjeta" aria-label="Lista de usuarios">
      <div className="us-filtros">
        <label className="us-buscar"><PIBuscar aria-hidden="true" /><input type="search" placeholder="Nombre, usuario, cédula o correo" aria-label="Buscar cuenta" value={q} onChange={(e) => setQ(e.target.value)} /></label>
        <select aria-label="Estado" value={estado} onChange={(e) => { setEstado(e.target.value); setPagina(1); }}><option value="">Todos los estados</option>{ESTADOS.map((v) => <option key={v} value={v}>{ETIQUETA[v]}</option>)}</select>
        <select aria-label="Rol" value={rol} onChange={(e) => { setRol(e.target.value); setPagina(1); }}><option value="">Todos los roles</option>{roles.map((r) => <option key={r.id}>{r.nombre}</option>)}</select></div>
      <div className="us-tabla"><table><thead><tr><th scope="col">Usuario</th><th scope="col">Contacto</th><th scope="col">Roles</th><th scope="col">Estado</th><th scope="col">Acciones</th></tr></thead>
        <tbody>{recurso.datos?.resultados.map((u) => <tr key={u.id}>
          <td><div className="us-persona"><FotoCuentaAdministrada cuenta={u} /><div><strong>{u.nombre} {u.apellido}</strong><small>@{u.username} · {u.cedula}</small></div></div></td>
          <td><span className="us-correo">{u.correo}</span><small>{u.telefono}</small></td>
          <td><div className="us-chips">{(u.roles.length ? u.roles : ["Usuario general"]).map((r) => <span key={r} className="us-chip">{r}</span>)}</div></td>
          <td><Insignia estado={u.estado} /></td>
          <td><button type="button" className="us-admin" aria-label={`Administrar a ${u.username}`} onClick={() => setEditar(u)}>Administrar</button></td></tr>)}</tbody></table>
        {recurso.datos && total === 0 && <p className="us-vacio">No se encontraron cuentas.</p>}
        {!recurso.datos && !recurso.error && <p className="us-vacio">Cargando…</p>}</div>
      <div className="us-pie"><span>Página {pagina} · {total} {total === 1 ? "cuenta" : "cuentas"}</span>
        <div><button type="button" className="boton boton--claro" disabled={pagina <= 1} onClick={() => setPagina(pagina - 1)}>Anterior</button>
          <button type="button" className="boton boton--claro" disabled={!recurso.datos || pagina * 20 >= total} onClick={() => setPagina(pagina + 1)}>Siguiente</button></div></div>
    </section>
    {crear && <CrearCuenta roles={roles} alCerrar={() => setCrear(false)} recargar={recargarTodo} />}
    {editar && <EditarCuenta cuenta={recurso.datos?.resultados.find((u) => u.id === editar.id) ?? editar}
      roles={roles} alCerrar={() => { setEditar(null); recargarTodo(); }} recargar={recargarTodo} />}
  </div>;
}
