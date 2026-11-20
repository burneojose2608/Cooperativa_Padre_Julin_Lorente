import { useRef, useState } from "react";
import useRecurso from "../../hooks/useRecurso";
import { useOperacion } from "./operaciones";

/** Código del socio + copiar/compartir con retroalimentación. Lo usan Perfil y Referidos. */
export default function useCodigoReferido() {
  const r = useRecurso("/plataforma/referidos/codigo/"); const op = useOperacion();
  const [manual, setManual] = useState(""); const [copiado, setCopiado] = useState(""); const reloj = useRef();
  const marcar = (cual) => { setCopiado(cual); clearTimeout(reloj.current); reloj.current = setTimeout(() => setCopiado(""), 2000); };
  async function copiar(texto, cual) {
    await op.ejecutar(async () => {
      try { await navigator.clipboard.writeText(texto); setManual(""); marcar(cual); }
      catch { setManual(texto); throw new Error("Tu navegador bloqueó el portapapeles. Selecciona el texto del campo y cópialo manualmente."); }
    }, "Copiado al portapapeles.");
  }
  async function compartir() {
    if (!navigator.share) return copiar(r.datos.enlace, "compartir");
    await op.ejecutar(async () => {
      try { await navigator.share({ title: "Cooperativa Padre Julián Lorente", text: "Te invito a conocer nuestra plataforma", url: r.datos.enlace }); }
      catch (e) { if (e.name !== "AbortError") { await navigator.clipboard.writeText(r.datos.enlace); } }
    }, "La acción de compartir terminó.");
  }
  return { r, op, manual, copiado, copiar, compartir };
}
