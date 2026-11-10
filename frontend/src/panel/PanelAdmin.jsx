import { useState } from "react";
import { adminDemo, ROLES } from "../datos/demo";
import { PIBorrar, PIEditar, PIMas, PIModulos, PIOperaciones, PIRoles, PIUsuarios } from "./IconosPanel";
import { Estado, Kpi, Linea, Modal, Proximamente, Tarjeta, TituloPagina } from "./ui";
import ValidarSocios from "./ValidarSocios";

function Inicio() {
  const k = adminDemo.kpis;
  return (
    <>
      <TituloPagina titulo="Inicio · Administración" sub="Estado general de la plataforma." />
      <div className="kpis">
        <Kpi icono={PIUsuarios} valor={k.usuarios} etiqueta="Usuarios" />
        <Kpi icono={PIRoles} valor={k.roles} etiqueta="Roles" />
        <Kpi icono={PIModulos} valor={k.modulos} etiqueta="Módulos" />
        <Kpi icono={PIOperaciones} valor={k.operaciones} etiqueta="Operaciones" tono="amarillo" />
      </div>
      <div className="rejilla-2">
        <Tarjeta titulo="Actividad del sistema"><Linea valores={adminDemo.actividad} etiquetas={adminDemo.meses} /></Tarjeta>
        <Tarjeta titulo="Últimos eventos">
          <ul className="eventos">{adminDemo.auditoria.slice(0, 4).map((e, i) => (
            <li key={i}><div><strong>{e.accion}</strong><small>{e.usuario} · {e.fecha}</small></div><Estado texto={e.resultado} /></li>))}</ul>
        </Tarjeta>
      </div>
    </>
  );
}

function Usuarios() {
  const [lista, setLista] = useState(adminDemo.usuarios);
  const [abierto, setAbierto] = useState(false);
  const [f, setF] = useState({ nombre: "", rol: "Socio" });
  const crear = (e) => { e.preventDefault(); setLista([...lista, { id: Date.now(), nombre: f.nombre.trim(), rol: f.rol, estado: "Activo" }]); setAbierto(false); setF({ nombre: "", rol: "Socio" }); };
  const alternar = (id) => setLista(lista.map((u) => u.id === id ? { ...u, estado: u.estado === "Activo" ? "Inactivo" : "Activo" } : u));
  return (
    <>
      <TituloPagina titulo="Usuarios" sub="Cuentas internas y sus roles.">
        <button className="boton boton--amarillo" onClick={() => setAbierto(true)}><PIMas className="boton__ico" />Nuevo usuario</button>
      </TituloPagina>
      <Tarjeta>
        <div className="tabla-caja"><table className="tabla">
          <thead><tr><th>Nombre</th><th>Rol</th><th>Estado</th><th className="der">Acciones</th></tr></thead>
          <tbody>{lista.map((u) => (
            <tr key={u.id}><td>{u.nombre}</td><td>{u.rol}</td><td><Estado texto={u.estado} /></td>
              <td className="der acciones">
                <button className="icono-btn" title="Activar / desactivar" aria-label={`Activar o desactivar ${u.nombre}`} onClick={() => alternar(u.id)}><PIEditar /></button>
                <button className="icono-btn icono-btn--rojo" aria-label={`Quitar ${u.nombre}`} onClick={() => setLista(lista.filter((x) => x.id !== u.id))}><PIBorrar /></button>
              </td></tr>))}</tbody>
        </table></div>
      </Tarjeta>
      {abierto && (
        <Modal titulo="Nuevo usuario interno" alCerrar={() => setAbierto(false)}>
          <form className="form-modal" onSubmit={crear}>
            <label>Nombre completo<input value={f.nombre} onChange={(e) => setF({ ...f, nombre: e.target.value })} required autoFocus /></label>
            <label>Rol<select value={f.rol} onChange={(e) => setF({ ...f, rol: e.target.value })}>{ROLES.map((r) => <option key={r}>{r}</option>)}</select></label>
            <button className="boton boton--azul" type="submit">Crear usuario</button>
          </form>
        </Modal>
      )}
    </>
  );
}

function Auditoria() {
  return (
    <>
      <TituloPagina titulo="Auditoría" sub="Registro de acciones. Solo se puede consultar, no modificar." />
      <Tarjeta><div className="tabla-caja"><table className="tabla">
        <thead><tr><th>Fecha</th><th>Usuario</th><th>Acción</th><th>Resultado</th></tr></thead>
        <tbody>{adminDemo.auditoria.map((e, i) => <tr key={i}><td>{e.fecha}</td><td>{e.usuario}</td><td>{e.accion}</td><td><Estado texto={e.resultado} /></td></tr>)}</tbody>
      </table></div></Tarjeta>
    </>
  );
}

export const RUTAS_ADMIN = {
  "validar-socios": <ValidarSocios />,
  "": <Inicio />, usuarios: <Usuarios />, auditoria: <Auditoria />,
  roles: <Proximamente titulo="Roles y permisos" />, parametros: <Proximamente titulo="Parámetros" />, reportes: <Proximamente titulo="Reportes" />,
};
