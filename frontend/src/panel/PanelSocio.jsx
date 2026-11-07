import { createContext, useContext, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { socioDemo } from "../datos/demo";
import { PICapacitacion, PICompartir, PICopa, PICopiar, PIJuegos, PIOk, PIPuntos, PIReferidos, PIBeneficios, PIMas } from "./IconosPanel";
import { Estado, Kpi, Modal, Proximamente, Tarjeta, TituloPagina } from "./ui";

const SocioCtx = createContext(null);
const useSocio = () => useContext(SocioCtx);

export function SocioProvider({ children }) {
  const [puntos, setPuntos] = useState(socioDemo.puntos);
  const [movs, setMovs] = useState(socioDemo.movimientos);
  const canjear = (b) => { setPuntos((p) => p - b.puntos);
    setMovs((m) => [{ fecha: new Date().toLocaleDateString("es-EC"), detalle: `Canje: ${b.nombre}`, puntos: -b.puntos }, ...m]); };
  return <SocioCtx.Provider value={{ puntos, movs, canjear }}>{children}</SocioCtx.Provider>;
}

function CodigoReferido() {
  const [copiado, setCopiado] = useState(false);
  const enlace = `${window.location.origin}/registro?ref=${socioDemo.codigo}`;
  const copiar = async () => { try { await navigator.clipboard.writeText(enlace); setCopiado(true); setTimeout(() => setCopiado(false), 1800); } catch { /* sin permiso */ } };
  const wa = `https://wa.me/?text=${encodeURIComponent(`Únete a la Cooperativa Padre Julián Lorente con mi código ${socioDemo.codigo}: ${enlace}`)}`;
  return (
    <Tarjeta titulo="Tu código de referido">
      <p className="codigo">{socioDemo.codigo}</p>
      <div className="fila-botones">
        <button className="boton boton--claro" onClick={copiar}>{copiado ? <PIOk className="boton__ico" /> : <PICopiar className="boton__ico" />}{copiado ? "¡Copiado!" : "Copiar enlace"}</button>
        <a className="boton boton--amarillo" href={wa} target="_blank" rel="noreferrer"><PICompartir className="boton__ico" />Compartir</a>
      </div>
    </Tarjeta>
  );
}

function Nivel() {
  const { puntos } = useSocio(); const n = socioDemo.nivel;
  const pct = Math.min(100, Math.max(0, ((puntos - n.desde) / (n.hasta - n.desde)) * 100));
  return (
    <Tarjeta titulo={`Nivel ${n.nombre}`}>
      <div className="progreso" role="progressbar" aria-valuenow={Math.round(pct)} aria-valuemin={0} aria-valuemax={100}><span style={{ width: `${pct}%` }} /></div>
      <p className="nota">Te faltan <strong>{Math.max(0, n.hasta - puntos).toLocaleString("es-EC")}</strong> puntos para llegar a nivel {n.siguiente}.</p>
    </Tarjeta>
  );
}

function Inicio() {
  const { usuario } = useAuth(); const { puntos } = useSocio();
  const enProceso = socioDemo.referidos.filter((r) => r.estado === "En proceso").length;
  return (
    <>
      <div className="saludo">
        <div><h1>¡Hola, {usuario.nombre}!</h1><p>Socio(a) de la Cooperativa</p></div>
        <div className="puntos-chip"><PIPuntos /><div><strong>{puntos.toLocaleString("es-EC")}</strong><span>puntos</span></div></div>
      </div>
      <div className="kpis">
        <Kpi icono={PIReferidos} valor={enProceso} etiqueta="Referidos en proceso" />
        <Kpi icono={PICapacitacion} valor={socioDemo.capacitaciones.filter((c) => c.estado === "Disponible").length} etiqueta="Capacitaciones disponibles" />
        <Kpi icono={PIJuegos} valor={2} etiqueta="Juegos activos" />
        <Kpi icono={PIBeneficios} valor={socioDemo.beneficios.filter((b) => b.puntos <= puntos).length} etiqueta="Beneficios que puedes canjear" tono="amarillo" />
      </div>
      <div className="rejilla-2">
        <CodigoReferido /><Nivel />
      </div>
      <div className="banner">
        <PICopa className="banner__ico" />
        <div><small>Campaña activa</small><h2>{socioDemo.campana.nombre}</h2><p>{socioDemo.campana.texto}</p></div>
        <Link className="boton boton--amarillo" to="/panel/referidos">Ver mis referidos</Link>
      </div>
    </>
  );
}

function Referidos() {
  const [lista, setLista] = useState(socioDemo.referidos);
  const [abierto, setAbierto] = useState(false);
  const [nombre, setNombre] = useState("");
  const agregar = (e) => { e.preventDefault(); if (!nombre.trim()) return;
    setLista([{ nombre: nombre.trim(), fecha: new Date().toLocaleDateString("es-EC"), estado: "En proceso", puntos: 0 }, ...lista]); setNombre(""); setAbierto(false); };
  return (
    <>
      <TituloPagina titulo="Mis referidos" sub="Personas que invitaste a la cooperativa.">
        <button className="boton boton--amarillo" onClick={() => setAbierto(true)}><PIMas className="boton__ico" />Registrar prospecto</button>
      </TituloPagina>
      <CodigoReferido />
      <Tarjeta titulo="Seguimiento">
        <div className="tabla-caja"><table className="tabla">
          <thead><tr><th>Nombre</th><th>Fecha</th><th>Estado</th><th className="der">Puntos</th></tr></thead>
          <tbody>{lista.map((r, i) => <tr key={i}><td>{r.nombre}</td><td>{r.fecha}</td><td><Estado texto={r.estado} /></td><td className="der">{r.puntos}</td></tr>)}</tbody>
        </table></div>
      </Tarjeta>
      {abierto && (
        <Modal titulo="Registrar prospecto" alCerrar={() => setAbierto(false)}>
          <form onSubmit={agregar} className="form-modal">
            <label>Nombre completo<input value={nombre} onChange={(e) => setNombre(e.target.value)} autoFocus required /></label>
            <button className="boton boton--azul" type="submit">Guardar</button>
          </form>
        </Modal>
      )}
    </>
  );
}

function Puntos() {
  const { puntos, movs } = useSocio();
  return (
    <>
      <TituloPagina titulo="Mis puntos" sub="Saldo y movimientos." />
      <div className="rejilla-2"><Tarjeta titulo="Saldo actual"><p className="gran">{puntos.toLocaleString("es-EC")} <small>puntos</small></p></Tarjeta><Nivel /></div>
      <Tarjeta titulo="Movimientos">
        <div className="tabla-caja"><table className="tabla"><thead><tr><th>Fecha</th><th>Detalle</th><th className="der">Puntos</th></tr></thead>
          <tbody>{movs.map((m, i) => <tr key={i}><td>{m.fecha}</td><td>{m.detalle}</td><td className={`der ${m.puntos < 0 ? "neg" : "pos"}`}>{m.puntos > 0 ? "+" : ""}{m.puntos}</td></tr>)}</tbody></table></div>
      </Tarjeta>
    </>
  );
}

function Capacitaciones() {
  const [tab, setTab] = useState("Disponible");
  const TABS = [["Disponible", "Disponibles"], ["En curso", "En curso"], ["Completada", "Completadas"]];
  const lista = socioDemo.capacitaciones.filter((c) => c.estado === tab);
  return (
    <>
      <TituloPagina titulo="Capacitaciones" sub="Aprende y gana puntos al completarlas." />
      <div className="pestanas" role="tablist">{TABS.map(([k, e]) => <button key={k} role="tab" aria-selected={tab === k} className={tab === k ? "on" : ""} onClick={() => setTab(k)}>{e}</button>)}</div>
      <div className="lista-tarjetas">
        {lista.length === 0 && <p className="vacio">No hay capacitaciones en esta sección.</p>}
        {lista.map((c) => (
          <article key={c.id} className="curso">
            <span className="curso__ico"><PICapacitacion /></span>
            <div><h3>{c.titulo}</h3><p>{c.detalle}</p><small>{c.horas} horas · {c.modalidad}</small>
              {c.avance != null && <div className="progreso"><span style={{ width: `${c.avance}%` }} /></div>}</div>
            <button className="boton boton--amarillo">{c.estado === "Disponible" ? "Inscribirse" : c.estado === "En curso" ? "Continuar" : "Ver certificado"}</button>
          </article>
        ))}
      </div>
    </>
  );
}

function Beneficios() {
  const { puntos, canjear } = useSocio();
  const [tab, setTab] = useState("disp"); const [elegido, setElegido] = useState(null); const [mios, setMios] = useState([]);
  const confirmar = () => { canjear(elegido); setMios([{ ...elegido, estado: "En proceso" }, ...mios]); setElegido(null); };
  return (
    <>
      <TituloPagina titulo="Canje de beneficios" sub={`Tienes ${puntos.toLocaleString("es-EC")} puntos.`} />
      <div className="pestanas" role="tablist">
        <button role="tab" aria-selected={tab === "disp"} className={tab === "disp" ? "on" : ""} onClick={() => setTab("disp")}>Disponibles</button>
        <button role="tab" aria-selected={tab === "mios"} className={tab === "mios" ? "on" : ""} onClick={() => setTab("mios")}>Mis canjes</button>
      </div>
      <div className="lista-tarjetas">
        {tab === "disp" && socioDemo.beneficios.map((b) => (
          <article key={b.id} className="curso">
            <span className="curso__ico"><PIBeneficios /></span>
            <div><h3>{b.nombre}</h3><p className="pts">{b.puntos.toLocaleString("es-EC")} puntos</p></div>
            <button className="boton boton--amarillo" disabled={b.puntos > puntos} onClick={() => setElegido(b)}>{b.puntos > puntos ? "Puntos insuficientes" : "Canjear"}</button>
          </article>))}
        {tab === "mios" && (mios.length === 0 ? <p className="vacio">Aún no has canjeado beneficios.</p> : mios.map((b, i) => (
          <article key={i} className="curso"><span className="curso__ico"><PIBeneficios /></span><div><h3>{b.nombre}</h3><p className="pts">{b.puntos} puntos</p></div><Estado texto={b.estado} /></article>)))}
      </div>
      {elegido && (
        <Modal titulo="Confirmar canje" alCerrar={() => setElegido(null)}>
          <div className="form-modal"><p>¿Canjear <strong>{elegido.nombre}</strong> por {elegido.puntos.toLocaleString("es-EC")} puntos?</p>
            <p className="nota">La entrega queda sujeta a aprobación del administrador.</p>
            <div className="fila-botones"><button className="boton boton--claro" onClick={() => setElegido(null)}>Cancelar</button><button className="boton boton--azul" onClick={confirmar}>Confirmar</button></div></div>
        </Modal>
      )}
    </>
  );
}

export const RUTAS_SOCIO = {
  "": <Inicio />, referidos: <Referidos />, puntos: <Puntos />, capacitaciones: <Capacitaciones />, beneficios: <Beneficios />,
  juegos: <Proximamente titulo="Juegos" />, sorteos: <Proximamente titulo="Sorteos" />,
  contenidos: <Proximamente titulo="Contenidos" />, notificaciones: <Proximamente titulo="Notificaciones" />,
};
