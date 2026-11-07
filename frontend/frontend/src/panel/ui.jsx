import { useEffect } from "react";
import { PICerrar } from "./IconosPanel";

export const Tarjeta = ({ titulo, acciones, children, className = "" }) => (
  <section className={`tarjeta ${className}`}>
    {(titulo || acciones) && <header className="tarjeta__cab">{titulo && <h2>{titulo}</h2>}{acciones}</header>}
    {children}
  </section>
);

export const Kpi = ({ icono: Ico, valor, etiqueta, tono = "azul" }) => (
  <div className={`kpi kpi--${tono}`}>
    <span className="kpi__ico"><Ico /></span>
    <strong>{typeof valor === "number" ? valor.toLocaleString("es-EC") : valor}</strong>
    <span>{etiqueta}</span>
  </div>
);

const ESTADOS = { Activa: "ok", Activo: "ok", Concretado: "ok", EXITO: "ok", Completada: "ok",
  Programada: "aviso", "En proceso": "aviso", "En curso": "aviso", Finalizada: "gris", Rechazado: "mal", FALLO: "mal", Inactivo: "gris" };
export const Estado = ({ texto }) => <span className={`estado estado--${ESTADOS[texto] || "gris"}`}>{texto}</span>;

export const TituloPagina = ({ titulo, sub, children }) => (
  <div className="pagina__cab"><div><h1>{titulo}</h1>{sub && <p>{sub}</p>}</div>{children}</div>
);

/** Barras verticales en SVG. El más alto se resalta en amarillo, como en el diseño. */
export function Barras({ datos, alto = 190 }) {
  const max = Math.max(...datos.map((d) => d.valor), 1);
  const tope = Math.ceil(max / 25) * 25;
  const W = 420, pad = { l: 34, r: 8, t: 10, b: 38 }, h = alto - pad.t - pad.b, ancho = (W - pad.l - pad.r) / datos.length;
  return (
    <svg className="grafica" viewBox={`0 0 ${W} ${alto}`} role="img" aria-label="Referidos por campaña">
      {[0, 0.5, 1].map((f) => { const y = pad.t + h - f * h; return (
        <g key={f}><line x1={pad.l} x2={W - pad.r} y1={y} y2={y} stroke="#e3e9f4" /><text x={pad.l - 6} y={y + 4} textAnchor="end" className="grafica__eje">{Math.round(tope * f)}</text></g>); })}
      {datos.map((d, i) => { const bh = (d.valor / tope) * h, x = pad.l + i * ancho + ancho * 0.22;
        return (<g key={d.etq}>
          <rect x={x} y={pad.t + h - bh} width={ancho * 0.56} height={bh} rx="3" fill={d.valor === max ? "#ffc72c" : "#1556bd"} />
          <text x={pad.l + i * ancho + ancho / 2} y={alto - 20} textAnchor="middle" className="grafica__eje">{d.etq.length > 14 ? d.etq.split(" ")[0] : d.etq}</text>
          <text x={pad.l + i * ancho + ancho / 2} y={alto - 8} textAnchor="middle" className="grafica__eje">{d.etq.length > 14 ? d.etq.split(" ").slice(1).join(" ") : ""}</text>
        </g>); })}
    </svg>
  );
}

export function Linea({ valores, etiquetas, alto = 190 }) {
  const W = 420, pad = { l: 40, r: 10, t: 10, b: 26 }, h = alto - pad.t - pad.b, w = W - pad.l - pad.r;
  const tope = Math.ceil(Math.max(...valores) / 250) * 250;
  const pts = valores.map((v, i) => [pad.l + (i / (valores.length - 1)) * w, pad.t + h - (v / tope) * h]);
  const linea = pts.map((p) => p.join(",")).join(" ");
  return (
    <svg className="grafica" viewBox={`0 0 ${W} ${alto}`} role="img" aria-label="Actividad del sistema">
      {[0, 0.5, 1].map((f) => { const y = pad.t + h - f * h; return (
        <g key={f}><line x1={pad.l} x2={W - pad.r} y1={y} y2={y} stroke="#e3e9f4" /><text x={pad.l - 6} y={y + 4} textAnchor="end" className="grafica__eje">{Math.round(tope * f).toLocaleString("es-EC")}</text></g>); })}
      <polygon points={`${pad.l},${pad.t + h} ${linea} ${pad.l + w},${pad.t + h}`} fill="#1556bd" opacity=".12" />
      <polyline points={linea} fill="none" stroke="#1556bd" strokeWidth="2.5" strokeLinejoin="round" />
      {pts.map(([x, y], i) => <circle key={i} cx={x} cy={y} r="3.6" fill="#fff" stroke="#1556bd" strokeWidth="2" />)}
      {etiquetas.map((e, i) => <text key={e} x={pts[i][0]} y={alto - 8} textAnchor="middle" className="grafica__eje">{e}</text>)}
    </svg>
  );
}

export function Modal({ titulo, alCerrar, children }) {
  useEffect(() => { const f = (e) => e.key === "Escape" && alCerrar(); window.addEventListener("keydown", f); return () => window.removeEventListener("keydown", f); }, [alCerrar]);
  return (
    <div className="modal" role="dialog" aria-modal="true" aria-label={titulo} onMouseDown={(e) => e.target === e.currentTarget && alCerrar()}>
      <div className="modal__caja">
        <header><h2>{titulo}</h2><button className="icono-btn" onClick={alCerrar} aria-label="Cerrar"><PICerrar /></button></header>
        {children}
      </div>
    </div>
  );
}

export const Proximamente = ({ titulo }) => (
  <div className="proximamente"><TituloPagina titulo={titulo} /><Tarjeta><p className="vacio">Esta sección se activará cuando se construya su módulo.</p></Tarjeta></div>
);
