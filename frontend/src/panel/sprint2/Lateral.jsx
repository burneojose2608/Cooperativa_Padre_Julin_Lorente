import { useEffect, useRef } from "react";
import { PICerrar } from "../IconosPanel";
import "./lateral.css";

const ENFOCABLES = 'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

/** Panel lateral deslizable: cabecera fija, contenido con su propio scroll y pie fijo para las acciones. */
export default function Lateral({ titulo, subtitulo, cabeza, alCerrar, pie, children }) {
  const caja = useRef(null);
  useEffect(() => {
    const previo = document.activeElement; const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    caja.current?.querySelector(ENFOCABLES)?.focus();
    const teclas = (e) => {
      if (e.key === "Escape") return alCerrar();
      if (e.key !== "Tab") return;
      const lista = [...caja.current.querySelectorAll(ENFOCABLES)]; if (!lista.length) return;
      const primero = lista[0], ultimo = lista[lista.length - 1];
      if (e.shiftKey && document.activeElement === primero) { e.preventDefault(); ultimo.focus(); }
      else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primero.focus(); }
    };
    window.addEventListener("keydown", teclas);
    return () => { window.removeEventListener("keydown", teclas); document.body.style.overflow = overflow; previo?.focus?.(); };
  }, [alCerrar]);
  return (
    <div className="lt" onMouseDown={(e) => e.target === e.currentTarget && alCerrar()}>
      <aside className="lt__caja" ref={caja} role="dialog" aria-modal="true" aria-label={titulo}>
        <header className="lt__cab">{cabeza}<div className="lt__tit"><h2>{titulo}</h2>{subtitulo && <p>{subtitulo}</p>}</div>
          <button type="button" className="lt__cerrar" onClick={alCerrar} aria-label="Cerrar"><PICerrar /></button></header>
        <div className="lt__cuerpo">{children}</div>
        {pie && <footer className="lt__pie">{pie}</footer>}
      </aside>
    </div>
  );
}
