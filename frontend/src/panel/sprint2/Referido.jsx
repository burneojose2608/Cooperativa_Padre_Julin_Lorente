import { useState } from "react";
import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { Aviso } from "./comunes";
import { useOperacion } from "./operaciones";

export default function Referido() {
  const r = useRecurso("/plataforma/referidos/codigo/"); const op = useOperacion(); const [manual, setManual] = useState("");
  async function copiar(texto) {
    await op.ejecutar(async () => {
      try { await navigator.clipboard.writeText(texto); setManual(""); }
      catch { setManual(texto); throw new Error("Tu navegador bloqueó el portapapeles. Selecciona el texto del campo y cópialo manualmente."); }
    }, "Copiado al portapapeles.");
  }
  async function compartir() {
    if (!navigator.share) return copiar(r.datos.enlace);
    await op.ejecutar(async () => {
      try { await navigator.share({ title: "Cooperativa Padre Julián Lorente", text: "Te invito a conocer nuestra plataforma", url: r.datos.enlace }); }
      catch (e) { if (e.name !== "AbortError") { await navigator.clipboard.writeText(r.datos.enlace); } }
    }, "La acción de compartir terminó.");
  }
  return <><TituloPagina titulo="Mi código de referido" sub="Comparte tu invitación a la plataforma." /><Aviso error={r.error} />
    {r.datos && <Tarjeta titulo="Tu invitación"><div className="s2-form"><strong className="s2-codigo">{r.datos.codigo}</strong>
      <a className="s2-enlace" href={r.datos.enlace} target="_blank" rel="noreferrer">{r.datos.enlace}</a>
      <div className="s2-acciones"><button className="boton" onClick={() => copiar(r.datos.codigo)}>Copiar código</button>
        <button className="boton boton--claro" onClick={() => copiar(r.datos.enlace)}>Copiar enlace</button>
        <button className="boton boton--claro" onClick={compartir}>Compartir</button></div>
      <Aviso {...op} />{manual && <input aria-label="Texto para copiar manualmente" readOnly value={manual} onFocus={(e) => e.target.select()} />}
      <p>Este enlace presenta una invitación. La gestión de personas referidas y la acreditación de puntos se habilitarán con sus módulos.</p>
    </div></Tarjeta>}
  </>;
}
