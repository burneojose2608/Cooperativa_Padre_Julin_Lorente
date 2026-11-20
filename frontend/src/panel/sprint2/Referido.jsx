import useCodigoReferido from "./compartir";
import { PICompartir, PICopiar, PICupon, PIEnlace, PIInfo, PIOk, PIReferidos } from "../IconosPanel";
import { Aviso } from "./comunes";
import "./referido.css";

/** Ilustración decorativa: regalo y megáfono (propia, sin imágenes externas). */
const Arte = () => (
  <svg className="rf-arte" viewBox="0 0 260 220" aria-hidden="true">
    <path d="M0 190c50-38 110-10 160-30s70-30 100-12V220H0Z" fill="#dbe8fb" />
    <g stroke="#ffc72c" strokeWidth="5" strokeLinecap="round"><path d="M96 30l-8-12M132 22v-14M168 30l9-12M70 58l-13-5M196 56l13-6" /></g>
    <rect x="96" y="82" width="108" height="86" rx="6" fill="#1556bd" /><rect x="86" y="68" width="128" height="26" rx="6" fill="#1f6fe0" />
    <rect x="138" y="68" width="24" height="100" fill="#ffc72c" /><path d="M150 68c-22-30-52-18-34 0M150 68c22-30 52-18 34 0" fill="none" stroke="#ffc72c" strokeWidth="9" strokeLinecap="round" />
    <path d="M40 138 82 112v70l-42-22Z" fill="#ffc72c" /><rect x="26" y="134" width="20" height="30" rx="6" fill="#e0a500" /><path d="M58 172l8 26" stroke="#e0a500" strokeWidth="9" strokeLinecap="round" />
    <rect x="150" y="140" width="92" height="64" rx="10" fill="#fff" stroke="#e1e9f6" /><g fill="none" stroke="#1556bd" strokeWidth="5" strokeLinecap="round">
      <circle cx="196" cy="162" r="9" /><circle cx="176" cy="172" r="7" /><circle cx="216" cy="172" r="7" /><path d="M164 192c2-9 8-12 14-12M228 192c-2-9-8-12-14-12M184 190c3-8 9-10 12-10s9 2 12 10" /></g>
  </svg>
);

export function Arte2() { return <Arte />; }

export default function Referido() {
  const { r, op, manual, copiado, copiar, compartir } = useCodigoReferido();
  return <section className="rf" aria-label="Mi código de referido">
    <div className="rf-cab"><span className="rf-cab__ico"><PIReferidos /></span>
      <div><h2>Mi código de referido</h2><p>Comparte tu invitación a la plataforma.</p></div></div>
    <Aviso error={r.error} />
    {r.datos && <div className="rf-tarjeta">
      <div className="rf-cuerpo">
        <Arte />
        <div className="rf-datos">
          <div className="rf-bloque"><h3>Tu código de referido</h3>
            <div className="rf-codigo"><PICupon aria-hidden="true" /><strong>{r.datos.codigo}</strong>
              <button type="button" className="rf-icono rf-icono--solido" aria-label="Copiar el código" onClick={() => copiar(r.datos.codigo, "codigo")}>{copiado === "codigo" ? <PIOk /> : <PICopiar />}</button></div></div>
          <div className="rf-bloque"><h3>Enlace de invitación</h3>
            <div className="rf-enlace"><PIEnlace aria-hidden="true" />
              <a href={r.datos.enlace} target="_blank" rel="noreferrer">{r.datos.enlace}</a>
              <button type="button" className="rf-icono" aria-label="Copiar el enlace de invitación" onClick={() => copiar(r.datos.enlace, "enlace")}>{copiado === "enlace" ? <PIOk /> : <PICopiar />}</button></div></div>
          <div className="rf-botones">
            <button className={`boton boton--azul${copiado === "codigo" ? " rf-hecho" : ""}`} onClick={() => copiar(r.datos.codigo, "codigo")}>{copiado === "codigo" ? <><PIOk className="boton__ico" />¡Copiado!</> : <><PICopiar className="boton__ico" />Copiar código</>}</button>
            <button className={`boton boton--claro${copiado === "enlace" ? " rf-hecho" : ""}`} onClick={() => copiar(r.datos.enlace, "enlace")}>{copiado === "enlace" ? <><PIOk className="boton__ico" />¡Copiado!</> : <><PIEnlace className="boton__ico" />Copiar enlace</>}</button>
            <button className="boton boton--claro" onClick={compartir}><PICompartir className="boton__ico" />Compartir</button>
          </div>
          <div className="rf-estado"><Aviso {...op} /></div>
          {manual && <input className="rf-manual" aria-label="Texto para copiar manualmente" readOnly value={manual} onFocus={(e) => e.target.select()} />}
        </div>
      </div>
      <p className="rf-info"><PIInfo aria-hidden="true" />Comparte tu código o enlace con tus amigos. Cuando se habiliten los módulos de referidos y puntos, aquí verás tus beneficios.</p>
    </div>}
  </section>;
}
