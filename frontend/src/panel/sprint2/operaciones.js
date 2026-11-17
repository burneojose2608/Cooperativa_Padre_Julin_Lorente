import { useState } from "react";
import { api } from "../../api/cliente";

export const mensajeError = (e) => [e.message, ...Object.entries(e.campos || {}).map(([k, v]) => `${k}: ${v}`)].join(" ");
export function useOperacion(recargar) {
  const [ocupado, setOcupado] = useState(false);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  async function ejecutar(accion, exito = "Cambios guardados.") {
    setOcupado(true); setError(""); setMensaje("");
    try { await accion(); setMensaje(exito); recargar?.(); return true; }
    catch (e) { setError(mensajeError(e)); return false; }
    finally { setOcupado(false); }
  }
  return { ocupado, error, mensaje, ejecutar };
}
export async function descargar(ruta, nombre) {
  const archivo = await api.archivoProtegido(ruta);
  const extensiones = { "application/pdf": ".pdf", "image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "video/mp4": ".mp4" };
  const url = URL.createObjectURL(archivo);
  const a = document.createElement("a"); a.href = url; a.download = nombre + (extensiones[archivo.type] || ""); a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
