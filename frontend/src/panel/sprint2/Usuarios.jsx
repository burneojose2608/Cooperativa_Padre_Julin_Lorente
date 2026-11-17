import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Modal, Tarjeta, TituloPagina } from "../ui";
import { Aviso, CampoPanel } from "./comunes";
import { useOperacion } from "./operaciones";

function CrearCuenta({ roles, alCerrar, recargar }) {
  const [datos, setDatos] = useState({ nombre: "", apellido: "", cedula: "", username: "", correo: "", telefono: "", fecha_nacimiento: "", clave: "", rol: "" });
  const op = useOperacion(recargar);
  const campos = [["nombre", "Nombres"], ["apellido", "Apellidos"], ["cedula", "Cédula"], ["username", "Usuario"],
    ["correo", "Correo electrónico", "email"], ["telefono", "Teléfono"], ["fecha_nacimiento", "Fecha de nacimiento", "date"], ["clave", "Contraseña inicial", "password"]];
  async function enviar(e) {
    e.preventDefault();
    if (await op.ejecutar(() => api.postProtegido("/auth/administracion/usuarios/", datos), "Cuenta creada.")) alCerrar();
  }
  return <Modal titulo="Crear cuenta interna" alCerrar={alCerrar}><form className="s2-form" onSubmit={enviar}>
    {campos.map(([clave, etiqueta, tipo]) => <CampoPanel key={clave} etiqueta={etiqueta} type={tipo || "text"} required
      value={datos[clave]} onChange={(e) => setDatos({ ...datos, [clave]: e.target.value })} />)}
    <CampoPanel etiqueta="Rol"><select required value={datos.rol} onChange={(e) => setDatos({ ...datos, rol: e.target.value })}>
      <option value="">Selecciona un rol interno</option>{roles.filter((r) => r.nombre !== "Socio").map((r) => <option key={r.id}>{r.nombre}</option>)}
    </select></CampoPanel><Aviso {...op} /><button className="boton" disabled={op.ocupado}>Crear cuenta</button>
  </form></Modal>;
}

function EditarCuenta({ cuenta, roles, alCerrar, recargar }) {
  const [correo, setCorreo] = useState(cuenta.correo); const [telefono, setTelefono] = useState(cuenta.telefono);
  const [estado, setEstado] = useState(cuenta.estado); const [motivo, setMotivo] = useState("");
  const [seleccionados, setSeleccionados] = useState(roles.filter((r) => cuenta.roles.includes(r.nombre)).map((r) => r.id));
  const op = useOperacion(recargar);
  const detalle = useRecurso(`/auth/administracion/usuarios/${cuenta.id}/`);
  return <Modal titulo={`Administrar a ${cuenta.username}`} alCerrar={alCerrar}>
    <Aviso {...op} />
    <form className="s2-form" onSubmit={(e) => { e.preventDefault(); op.ejecutar(() => api.patchProtegido(`/auth/administracion/usuarios/${cuenta.id}/`, { correo, telefono })); }}>
      <p>{cuenta.nombre} {cuenta.apellido} · Cédula {cuenta.cedula}</p>
      <CampoPanel etiqueta="Correo electrónico" type="email" required value={correo} onChange={(e) => setCorreo(e.target.value)} />
      <CampoPanel etiqueta="Teléfono" required value={telefono} onChange={(e) => setTelefono(e.target.value)} />
      <button className="boton" disabled={op.ocupado}>Guardar contacto</button>
    </form>
    <form className="s2-form" onSubmit={(e) => { e.preventDefault(); op.ejecutar(() => api.putProtegido(`/auth/administracion/usuarios/${cuenta.id}/roles/`, { roles: seleccionados })); }}>
      <fieldset><legend>Roles de la cuenta</legend>{roles.map((r) => <label className="s2-check" key={r.id}>
        <input type="checkbox" checked={seleccionados.includes(r.id)} onChange={(e) => setSeleccionados(e.target.checked ? [...seleccionados, r.id] : seleccionados.filter((id) => id !== r.id))} />{r.nombre}
      </label>)}</fieldset><p>El rol Socio requiere una validación previa en «Validar socios».</p>
      <button className="boton" disabled={op.ocupado}>Guardar roles</button>
    </form>
    <form className="s2-form" onSubmit={(e) => { e.preventDefault(); op.ejecutar(async () => {
      await api.postProtegido(`/auth/administracion/usuarios/${cuenta.id}/estado/`, { estado, motivo }); detalle.recargar();
    }); }}>
      <CampoPanel etiqueta="Estado"><select value={estado} onChange={(e) => setEstado(e.target.value)}>
        {["ACTIVA", "SUSPENDIDA", "DESACTIVADA"].map((v) => <option key={v}>{v}</option>)}</select></CampoPanel>
      <CampoPanel etiqueta="Motivo del cambio" required maxLength={1000} value={motivo} onChange={(e) => setMotivo(e.target.value)} />
      <button className="boton" disabled={op.ocupado}>Aplicar estado</button>
      <p>Suspender o desactivar cierra las sesiones activas de la cuenta.</p>
    </form>
    <section className="s2-form"><h3>Historial de estados</h3><Aviso error={detalle.error} />
      {detalle.datos?.historial.map((h) => <p key={h.fecha}>{new Date(h.fecha).toLocaleString("es-EC")} · {h.estado_anterior} → {h.estado_nuevo} · {h.motivo} · Responsable #{h.usuario_id}</p>)}
      {!detalle.datos?.historial.length && <p>Sin cambios de estado registrados.</p>}
    </section>
  </Modal>;
}

export default function Usuarios() {
  const [q, setQ] = useState(""); const [filtro, setFiltro] = useState(""); const [estado, setEstado] = useState(""); const [rol, setRol] = useState("");
  const [pagina, setPagina] = useState(1); const [editar, setEditar] = useState(null); const [crear, setCrear] = useState(false);
  const catalogo = useRecurso("/auth/administracion/roles/");
  const recurso = useRecurso(`/auth/administracion/usuarios/?q=${encodeURIComponent(filtro)}&estado=${estado}&rol=${encodeURIComponent(rol)}&pagina=${pagina}`);
  const roles = catalogo.datos?.roles || [];
  return <><TituloPagina titulo="Usuarios" sub="Gestiona cuentas, contacto, estados y roles."><button className="boton" onClick={() => setCrear(true)}>Crear cuenta interna</button></TituloPagina>
    <Aviso error={recurso.error || catalogo.error} />
    <form className="s2-acciones" onSubmit={(e) => { e.preventDefault(); setFiltro(q); setPagina(1); }}>
      <CampoPanel etiqueta="Buscar cuenta" value={q} onChange={(e) => setQ(e.target.value)} /><button className="boton">Buscar</button>
      <CampoPanel etiqueta="Estado"><select value={estado} onChange={(e) => { setEstado(e.target.value); setPagina(1); }}><option value="">Todos</option>{["ACTIVA", "SUSPENDIDA", "DESACTIVADA"].map((v) => <option key={v}>{v}</option>)}</select></CampoPanel>
      <CampoPanel etiqueta="Rol"><select value={rol} onChange={(e) => { setRol(e.target.value); setPagina(1); }}><option value="">Todos</option>{roles.map((r) => <option key={r.id}>{r.nombre}</option>)}</select></CampoPanel>
    </form>
    <Tarjeta><div className="s2-tabla"><table><thead><tr><th>Usuario</th><th>Nombre</th><th>Contacto</th><th>Roles</th><th>Estado</th><th>Acciones</th></tr></thead>
      <tbody>{recurso.datos?.resultados.map((u) => <tr key={u.id}><td>{u.username}<br />{u.cedula}</td><td>{u.nombre} {u.apellido}</td><td>{u.correo}<br />{u.telefono}</td><td>{u.roles.join(", ") || "Usuario general"}</td><td>{u.estado}</td><td><button className="boton boton--claro" onClick={() => setEditar(u)}>Administrar</button></td></tr>)}</tbody></table></div>
      {recurso.datos?.total === 0 && <p className="vacio">No se encontraron cuentas.</p>}
      <div className="s2-acciones"><button className="boton boton--claro" disabled={pagina <= 1} onClick={() => setPagina(pagina - 1)}>Anterior</button>
        <span>Página {pagina} · {recurso.datos?.total ?? 0} cuentas</span><button className="boton boton--claro" disabled={!recurso.datos || pagina * 20 >= recurso.datos.total} onClick={() => setPagina(pagina + 1)}>Siguiente</button></div>
    </Tarjeta>
    {crear && <CrearCuenta roles={roles} alCerrar={() => setCrear(false)} recargar={recurso.recargar} />}
    {editar && <EditarCuenta cuenta={editar} roles={roles} alCerrar={() => setEditar(null)} recargar={recurso.recargar} />}
  </>;
}
