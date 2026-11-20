import { useEffect, useState } from "react";
import { convertirCuentaASocio, listarCuentasGenerales } from "../api/administracion";
import { PIAlerta, PIBuscar, PIOk, PIValidar } from "./IconosPanel";
import Lateral from "./sprint2/Lateral";
import "./sprint2/usuarios.css";
import "./validarsocios.css";

const PADRON = { activo: ["Activo", "activo"], inactivo: ["Inactivo", "inactivo"], no_encontrado: ["Sin validar", "sin"] };
const iniciales = (c) => `${c.nombre?.[0] ?? ""}${c.apellido?.[0] ?? ""}`.toUpperCase() || "U";
const PASOS = [["Busca la cuenta", "Por usuario, nombre o cédula."], ["Revisa el padrón", "Comprueba que la persona sea socia activa."], ["Acepta como socio", "Se habilitan sus funciones de socio y queda en auditoría."]];

export default function ValidarSocios() {
  const [busqueda, setBusqueda] = useState("");
  const [filtro, setFiltro] = useState("");
  const [pagina, setPagina] = useState(1);
  const [revision, setRevision] = useState(0);
  const [datos, setDatos] = useState({ results: [], count: 0 });
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [aviso, setAviso] = useState("");
  const [seleccion, setSeleccion] = useState(null);
  const [confirmado, setConfirmado] = useState(false);
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    let vigente = true;
    listarCuentasGenerales(filtro, pagina)
      .then((respuesta) => { if (vigente) setDatos(respuesta); })
      .catch((err) => { if (vigente) setError(err.message); })
      .finally(() => { if (vigente) setCargando(false); });
    return () => { vigente = false; };
  }, [filtro, pagina, revision]);

  // La búsqueda se aplica sola al escribir (con una pequeña pausa) o al pulsar Enter.
  useEffect(() => {
    const t = setTimeout(() => {
      const nuevo = busqueda.trim();
      if (nuevo !== filtro) { setCargando(true); setError(""); setPagina(1); setFiltro(nuevo); }
    }, 350);
    return () => clearTimeout(t);
  }, [busqueda, filtro]);

  function cambiarPagina(nuevaPagina) { setCargando(true); setError(""); setPagina(nuevaPagina); }

  async function convertir(e) {
    e.preventDefault();
    if (!confirmado || guardando || !seleccion) return;
    setGuardando(true);
    setError("");
    try {
      const resultado = await convertirCuentaASocio(seleccion.id);
      setAviso(`${seleccion.username}: ${resultado.mensaje} Código: ${resultado.codigo_socio}.`);
      setSeleccion(null);
      setCargando(true);
      setPagina(1);
      setRevision((r) => r + 1);
    } catch (err) {
      setError(err.message);
    } finally {
      setGuardando(false);
    }
  }

  return (
    <div className="us vs">
      <div className="us-cab"><span className="us-cab__ico"><PIValidar /></span>
        <div className="us-cab__txt"><h1>Validar socios</h1><p>Proceso temporal de validación manual de cuentas generales.</p></div>
        <div className="vs-total"><strong>{cargando && !datos.count ? "—" : datos.count}</strong><span>{datos.count === 1 ? "cuenta pendiente" : "cuentas pendientes"}</span></div></div>
      <ol className="vs-pasos" aria-label="Cómo validar a un socio">
        {PASOS.map(([t, d], i) => <li key={t}><span className="vs-pasos__n">{i + 1}</span><div><strong>{t}</strong><small>{d}</small></div></li>)}</ol>
      <p className="us-nota"><PIAlerta aria-hidden="true" />Confirma la condición de socio activo antes de habilitar sus funciones. La conversión conserva el usuario y la contraseña.</p>
      {aviso && <p className="vs-exito" role="status"><PIOk aria-hidden="true" /><span>{aviso}</span><button type="button" aria-label="Cerrar aviso" onClick={() => setAviso("")}>×</button></p>}
      {!seleccion && error && <div className="alerta alerta--error" role="alert">{error}</div>}
      <section className="us-tarjeta" aria-label="Cuentas generales">
        <form className="us-filtros" onSubmit={(e) => { e.preventDefault(); setCargando(true); setError(""); setPagina(1); setFiltro(busqueda.trim()); setRevision((r) => r + 1); }}>
          <label className="us-buscar"><PIBuscar aria-hidden="true" />
            <input type="search" placeholder="Buscar por usuario, nombre o cédula" aria-label="Buscar por usuario, nombre o cédula" value={busqueda} maxLength={100} onChange={(e) => setBusqueda(e.target.value)} /></label>
          <button className="boton boton--azul" type="submit" disabled={cargando}>Buscar</button></form>
        {cargando ? <p className="us-vacio" role="status">Cargando cuentas…</p> : !error && (
          <>
            <div className="us-tabla"><table>
              <thead><tr><th scope="col">Persona</th><th scope="col">Cédula</th><th scope="col">Cuenta</th><th scope="col">Padrón</th><th scope="col">Acción</th></tr></thead>
              <tbody>{datos.results.map((cuenta) => {
                const [etqPadron, clasePadron] = PADRON[cuenta.estado_padron] ?? [cuenta.estado_padron, "sin"];
                const bloqueada = cuenta.estado !== "ACTIVA" || cuenta.estado_padron === "inactivo";
                return <tr key={cuenta.id}>
                  <td><div className="us-persona"><span className="us-avatar" aria-hidden="true">{iniciales(cuenta)}</span>
                    <div><strong>{cuenta.nombre} {cuenta.apellido}</strong><small>@{cuenta.username}</small></div></div></td>
                  <td>{cuenta.cedula}</td>
                  <td><span className={`us-estado us-estado--${cuenta.estado === "ACTIVA" ? "activa" : "desactivada"}`}>{cuenta.estado === "ACTIVA" ? "Activa" : cuenta.estado}</span></td>
                  <td><span className={`us-estado vs-padron vs-padron--${clasePadron}`}>{etqPadron}</span></td>
                  <td><button type="button" className="vs-revisar" disabled={bloqueada} title={bloqueada ? "Esta cuenta no se puede validar" : undefined}
                    onClick={() => { setSeleccion(cuenta); setConfirmado(false); setError(""); }}>Validar socio</button></td>
                </tr>;
              })}</tbody>
            </table>
            {!datos.results.length && <div className="vs-vacio"><span><PIValidar /></span><h2>No hay cuentas por validar</h2>
              <p>{filtro ? "Ninguna cuenta general coincide con tu búsqueda." : "Cuando alguien se registre con una cuenta general, aparecerá aquí."}</p></div>}</div>
            <div className="us-pie"><span>{datos.count} {datos.count === 1 ? "cuenta" : "cuentas"} · Página {pagina}</span>
              <div><button type="button" className="boton boton--claro" disabled={!datos.previous} onClick={() => cambiarPagina(pagina - 1)}>Anterior</button>
                <button type="button" className="boton boton--claro" disabled={!datos.next} onClick={() => cambiarPagina(pagina + 1)}>Siguiente</button></div></div>
          </>
        )}
      </section>
      {seleccion && <Lateral titulo="Confirmar condición de socio" subtitulo="Revisa los datos antes de aceptarla como socia." alCerrar={() => { if (!guardando) setSeleccion(null); }}
        cabeza={<span className="us-avatar us-avatar--grande" aria-hidden="true">{iniciales(seleccion)}</span>}
        pie={<><button type="button" className="boton boton--claro" disabled={guardando} onClick={() => setSeleccion(null)}>Cancelar</button>
          <button form="form-validar" className="boton boton--amarillo" type="submit" disabled={!confirmado || guardando}>
            <PIOk className="boton__ico" />{guardando ? "Validando…" : "Confirmar que es socio"}</button></>}>
        <form id="form-validar" className="us-form" onSubmit={convertir}>
          <dl className="vs-ficha">
            <div><dt>Persona</dt><dd><strong>{seleccion.nombre} {seleccion.apellido}</strong></dd></div>
            <div><dt>Usuario</dt><dd>@{seleccion.username}</dd></div>
            <div><dt>Cédula</dt><dd>{seleccion.cedula}</dd></div>
            <div><dt>Padrón</dt><dd><span className={`us-estado vs-padron vs-padron--${(PADRON[seleccion.estado_padron] ?? ["", "sin"])[1]}`}>{(PADRON[seleccion.estado_padron] ?? [seleccion.estado_padron])[0]}</span></dd></div>
          </dl>
          <p className="us-nota"><PIAlerta aria-hidden="true" />Esta aprobación temporal registrará su condición activa en el padrón y habilitará las funciones de socio. Quedará registrada en auditoría.</p>
          <label className="us-rol"><input type="checkbox" checked={confirmado} disabled={guardando} onChange={(e) => setConfirmado(e.target.checked)} />
            <span>Confirmo que revisé esta cuenta y que la persona es socia activa.</span></label>
          {error && <div className="alerta alerta--error" role="alert">{error}</div>}
        </form>
      </Lateral>}
    </div>
  );
}
