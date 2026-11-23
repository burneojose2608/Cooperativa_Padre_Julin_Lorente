import { PICompartir, PIConvertido, PICopiar, PIEnlace, PIInvitar, PIOk, PIPuntos, PIReferidos, PIReloj, PIBuscar } from "../IconosPanel";
import { Aviso } from "./comunes";
import useCodigoReferido from "./compartir";
import { Arte2 } from "./Referido";
import "./referido.css";
import "./referidos.css";

const KPIS = [[PIReferidos, "Referidos registrados", "azul"], [PIReloj, "En seguimiento", "amarillo"], [PIConvertido, "Convertidos", "verde"], [PIPuntos, "Puntos por conversiones", "morado"]];
const COLUMNAS = ["Referido", "Fecha", "Campaña", "Consentimiento", "Estado", "Puntos", "Acción"];

/** Pantalla «Mis referidos». Hoy el backend solo entrega el código y el enlace; la lista llegará con su módulo. */
export default function Referidos({ children }) {
  const { r, op, manual, copiado, copiar, compartir } = useCodigoReferido(); const d = r.datos;
  return <div className="rs">
    <div className="rs-cab"><span className="rs-cab__ico"><PIReferidos /></span>
      <div className="rs-cab__txt"><h1>Mis referidos</h1><p>Invita a nuevas personas y consulta su avance sin exponer datos sensibles.</p></div>
      <button type="button" className="boton boton--amarillo" disabled={!d} onClick={compartir}><PIInvitar className="boton__ico" />Invitar referido</button></div>
    <div className="rs-estado"><Aviso error={r.error || op.error} mensaje={op.mensaje} /></div>
    {!children && <div className="rs-kpis">{KPIS.map(([Ico, etq, tono]) => <div key={etq} className={`rs-kpi rs-kpi--${tono}`}><span className="rs-kpi__ico"><Ico /></span>
      <div><strong aria-label="Sin datos todavía">—</strong><span>{etq}</span><small>Próximamente</small></div></div>)}</div>}
    <section className="rs-tarjeta rs-codigo" aria-label="Tu código de referido">
      <div className="rs-codigo__dato"><span>Tu código de referido</span><strong>{d ? d.codigo : "…"}</strong>
        {d && <a href={d.enlace} target="_blank" rel="noreferrer">{d.enlace}</a>}</div>
      <div className="rs-codigo__acc">
        <button type="button" disabled={!d} className={`boton boton--claro${copiado === "codigo" ? " rf-hecho" : ""}`} onClick={() => copiar(d.codigo, "codigo")}>
          {copiado === "codigo" ? <><PIOk className="boton__ico" />¡Copiado!</> : <><PICopiar className="boton__ico" />Copiar código</>}</button>
        <button type="button" disabled={!d} className={`boton boton--claro${copiado === "enlace" ? " rf-hecho" : ""}`} onClick={() => copiar(d.enlace, "enlace")}>
          {copiado === "enlace" ? <><PIOk className="boton__ico" />¡Copiado!</> : <><PIEnlace className="boton__ico" />Copiar enlace</>}</button>
        <button type="button" disabled={!d} className="boton boton--amarillo" onClick={compartir}><PICompartir className="boton__ico" />Compartir</button></div>
      {manual && <input className="rf-manual rs-manual" aria-label="Texto para copiar manualmente" readOnly value={manual} onFocus={(e) => e.target.select()} />}
    </section>
    {children || <section className="rs-tarjeta" aria-label="Lista de referidos">
      <div className="rs-filtros">
        <label className="rs-buscar"><PIBuscar aria-hidden="true" /><input type="search" disabled placeholder="Buscar por alias o campaña…" aria-label="Buscar por alias o campaña" /></label>
        <select disabled aria-label="Filtrar por estado"><option>Todos</option></select></div>
      <div className="rs-tabla"><table><thead><tr>{COLUMNAS.map((c) => <th key={c} scope="col">{c}</th>)}</tr></thead></table>
        <div className="rs-vacio"><div className="rs-vacio__arte"><Arte2 /></div>
          <h2>Aquí verás a las personas que invites</h2>
          <p>Cuando se habilite el módulo de referidos, esta tabla mostrará a cada persona con su fecha, campaña, estado y puntos. Mientras tanto, comparte tu código o tu enlace.</p>
          <small className="rs-prox">Próximamente</small></div></div>
    </section>}
  </div>;
}
