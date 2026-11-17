import { useCallback, useEffect, useState } from "react";
import { api } from "../api/cliente";

export default function useRecurso(ruta) {
  const [datos, setDatos] = useState(null);
  const [error, setError] = useState("");
  const [version, setVersion] = useState(0);
  const recargar = useCallback(() => setVersion((v) => v + 1), []);
  useEffect(() => {
    let vigente = true;
    api.getProtegido(ruta).then((r) => { if (vigente) { setDatos(r); setError(""); } })
      .catch((e) => { if (vigente) setError(e.message); });
    return () => { vigente = false; };
  }, [ruta, version]);
  return { datos, error, recargar };
}
