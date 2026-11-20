import { useMemo, useState } from "react";
import useRecurso from "../../hooks/useRecurso";
import { PIActualizar, PIAlerta, PIAuditoria, PIBuscar, PIChevron, PIHistorial, PIOk, PIUsuarios } from "../IconosPanel";
import Lateral from "./Lateral";
import "./usuarios.css";
import "./inicioadmin.css";
import "./auditoria.css";

const POR_PAGINA = 10;
const humanizar = (t = "") => { const s = String(t).replace(/_/g, " ").toLowerCase(); return s.charAt(0).toUpperCase() + s.slice(1); };
const tono = (res = "") => /exit|ok|correct|permit|aprob/i.test(res) ? "ok" : /fall|err|deneg|rechaz|bloq|invalid/i.test(res) ? "mal" : "neutro";
const mismoDia = (a, b) => a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
const fechaHora = (iso) => { const d = new Date(iso); return Number.isNaN(d.getTime()) ? ["", ""] : [d.toLocaleDateString("es-EC", { day: "2-digit", month: "short", year: "numeric" }).replace(".", ""), d.toLocaleTimeString("es-EC", { hour: "2-digit", minute: "2-digit" })]; };
const valor = (v) => v !== null && typeof v === "object" ? JSON.stringify(v) : String(v);

const Kpi = ({ icono: Ico, valor: v, etq, tono: t }) => <div className={`ia-kpi ia-kpi--${t}`}><span className="ia-kpi__ico"><Ico /></span><div><strong>{v ?? "—"}</strong><span>{etq}</span></div></div>;

export default function Auditoria() {
  const r = useRecurso("/auth/administracion/auditoria/");
  const eventos = useMemo(() => Array.isArray(r.datos) ? r.datos : [], [r.datos]);
  const [q, setQ] = useState(""); const [res, setRes] = useState(""); const [pagina, setPagina] = useState(1); const [sel, setSel] = useState(null);
  const resultados = [...new Set(eventos.map((e) => e.resultado).filter(Boolean))];
  const vista = eventos.filter((e) => (!res || e.resultado === res) && `${e.accion} ${e.entidad} ${e.registro_id} ${e.usuario_id ?? "anonimo"}`.toLowerCase().includes(q.trim().toLowerCase()));
  const paginas = Math.max(1, Math.ceil(vista.length / POR_PAGINA)); const actual = Math.min(pagina, paginas);
  const fila = vista.slice((actual - 1) * POR_PAGINA, actual * POR_PAGINA);
  const hoy = new Date(); const cargado = Array.isArray(r.datos);
  const detalle = sel?.detalle && typeof sel.detalle === "object" ? Object.entries(sel.detalle) : [];
  return <div className="us au">
    <div className="us-cab"><span className="us-cab__ico"><PIAuditoria /></span><div className="us-cab__txt"><h1>Auditoría</h1><p>Últimas 100 acciones registradas. La base conserva esta bitácora sin permitir modificaciones.</p></div>
      <button className="boton boton--claro" onClick={r.recargar}><PIActualizar className="boton__ico" />Actualizar</button></div>
    {r.error && <p className="alerta alerta--error" role="alert">{r.error}</p>}
    <div className="ia-kpis">
      <Kpi icono={PIHistorial} valor={cargado ? eventos.length : undefined} etq="Eventos mostrados" tono="azul" />
      <Kpi icono={PIOk} valor={cargado ? eventos.filter((e) => tono(e.resultado) === "ok").length : undefined} etq="Exitosos" tono="verde" />
      <Kpi icono={PIAlerta} valor={cargado ? eventos.filter((e) => tono(e.resultado) === "mal").length : undefined} etq="Con error o rechazados" tono="amarillo" />
      <Kpi icono={PIUsuarios} valor={cargado ? eventos.filter((e) => mismoDia(new Date(e.fecha), hoy)).length : undefined} etq="Eventos hoy" tono="morado" />
    </div>
    <section className="us-tarjeta" aria-label="Bitácora de auditoría">
      <div className="us-filtros"><label className="us-buscar"><PIBuscar aria-hidden="true" /><input type="search" placeholder="Buscar por acción, registro o usuario" aria-label="Buscar por acción, registro o usuario" value={q} onChange={(e) => { setQ(e.target.value); setPagina(1); }} /></label>
        <select aria-label="Filtrar por resultado" value={res} onChange={(e) => { setRes(e.target.value); setPagina(1); }}><option value="">Todos los resultados</option>{resultados.map((x) => <option key={x} value={x}>{humanizar(x)}</option>)}</select></div>
      {!cargado && !r.error ? <p className="us-vacio" role="status">Cargando bitácora…</p> : cargado && (
        <>
          <div className="us-tabla au-tabla"><table>
            <thead><tr><th scope="col">Fecha</th><th scope="col">Responsable</th><th scope="col">Acción</th><th scope="col">Registro</th><th scope="col">Resultado</th><th scope="col">Detalle</th></tr></thead>
            <tbody>{fila.map((e) => { const [d, h] = fechaHora(e.fecha); return <tr key={e.id_auditoria}>
              <td data-etq="Fecha">{d}<small>{h}</small></td>
              <td data-etq="Responsable">{e.usuario_id ? `Usuario #${e.usuario_id}` : "Anónimo"}</td>
              <td data-etq="Acción"><strong>{humanizar(e.accion)}</strong></td>
              <td data-etq="Registro">{humanizar(e.entidad)}<small>#{e.registro_id}</small></td>
              <td data-etq="Resultado"><span className={`us-estado au-res au-res--${tono(e.resultado)}`}>{humanizar(e.resultado)}</span></td>
              <td data-etq="Detalle"><button type="button" className="au-ver" onClick={() => setSel(e)}>Ver detalle<PIChevron /></button></td></tr>; })}</tbody></table>
            {!fila.length && <p className="us-vacio">{eventos.length ? "Ningún evento coincide con tu búsqueda." : "Aún no hay eventos registrados."}</p>}</div>
          <div className="us-pie"><span>{vista.length} {vista.length === 1 ? "evento" : "eventos"} · Página {actual} de {paginas}</span>
            <div><button type="button" className="boton boton--claro" disabled={actual <= 1} onClick={() => setPagina(actual - 1)}>Anterior</button>
              <button type="button" className="boton boton--claro" disabled={actual >= paginas} onClick={() => setPagina(actual + 1)}>Siguiente</button></div></div>
        </>)}
    </section>
    {sel && <Lateral titulo={humanizar(sel.accion)} subtitulo={fechaHora(sel.fecha).join(" · ")} alCerrar={() => setSel(null)} cabeza={<span className="us-cab-ico"><PIAuditoria /></span>}
      pie={<button type="button" className="boton boton--claro" onClick={() => setSel(null)}>Cerrar</button>}>
      <dl className="vs-ficha">
        <div><dt>Responsable</dt><dd>{sel.usuario_id ? `Usuario #${sel.usuario_id}` : "Anónimo"}</dd></div>
        <div><dt>Registro</dt><dd>{humanizar(sel.entidad)} #{sel.registro_id}</dd></div>
        <div><dt>Resultado</dt><dd><span className={`us-estado au-res au-res--${tono(sel.resultado)}`}>{humanizar(sel.resultado)}</span></dd></div>
      </dl>
      <h3 className="au-sub">Detalle técnico</h3>
      {detalle.length ? <dl className="vs-ficha">{detalle.map(([k, v]) => <div key={k}><dt>{humanizar(k)}</dt><dd>{valor(v)}</dd></div>)}</dl> : <p className="au-vacio">Este evento no tiene detalle adicional.</p>}
    </Lateral>}
  </div>;
}
