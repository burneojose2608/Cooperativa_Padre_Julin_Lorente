import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { Aviso, CampoPanel } from "./comunes";
import { useOperacion } from "./operaciones";

const hoyLocal = () => new Date().toLocaleDateString("sv-SE");
export default function Reglas() {
  const r = useRecurso("/plataforma/reglas-puntos/"); const op = useOperacion(r.recargar);
  const [datos, setDatos] = useState({ tipo_actividad: "CONVERSION_REFERIDO", puntos: 10, limite_periodo: 1, periodo: "DIA", vigente_desde: hoyLocal(), vigente_hasta: "" });
  const cambiar = (campo) => (e) => setDatos({ ...datos, [campo]: e.target.value });
  return <><TituloPagina titulo="Reglas de puntos" sub="Configura las condiciones para futuras actividades. Cada cambio crea una versión y conserva el historial." />
    <Aviso error={r.error} /><div className="s2-columnas"><Tarjeta titulo="Nueva versión"><form className="s2-form" onSubmit={(e) => { e.preventDefault(); op.ejecutar(() => api.postProtegido("/plataforma/reglas-puntos/", { ...datos, puntos: Number(datos.puntos), limite_periodo: Number(datos.limite_periodo), vigente_hasta: datos.vigente_hasta || null })); }}>
      <CampoPanel etiqueta="Actividad"><select value={datos.tipo_actividad} onChange={cambiar("tipo_actividad")}>{r.datos?.actividades.map((a) => <option key={a}>{a}</option>)}</select></CampoPanel>
      <CampoPanel etiqueta="Puntos por actividad" type="number" required min="1" max="1000000" value={datos.puntos} onChange={cambiar("puntos")} />
      <CampoPanel etiqueta="Máximo de actividades por período" type="number" required min="1" max="1000000" value={datos.limite_periodo} onChange={cambiar("limite_periodo")} />
      <CampoPanel etiqueta="Período"><select value={datos.periodo} onChange={cambiar("periodo")}>{["DIA", "MES", "ANIO"].map((p) => <option key={p}>{p}</option>)}</select></CampoPanel>
      <CampoPanel etiqueta="Vigente desde" type="date" required min={hoyLocal()} value={datos.vigente_desde} onChange={cambiar("vigente_desde")} />
      <CampoPanel etiqueta="Vigente hasta (opcional)" type="date" min={datos.vigente_desde} value={datos.vigente_hasta} onChange={cambiar("vigente_hasta")} />
      <Aviso {...op} /><button className="boton" disabled={op.ocupado}>Crear versión</button>
    </form></Tarjeta><Tarjeta titulo="Versiones registradas"><div className="s2-lista">{r.datos?.reglas.map((v) => <article key={v.id}>
      <h3>{v.tipo_actividad}</h3><p>{v.puntos} puntos · máximo {v.limite_periodo} actividades por {v.periodo}</p>
      <p>{v.vigente_desde} — {v.vigente_hasta || "Sin fecha de fin"} · {v.actual ? "Vigente" : "Histórica o programada"}</p><small>Versión {v.version}</small>
    </article>)}{r.datos?.reglas.length === 0 && <p className="vacio">Todavía no hay reglas.</p>}</div></Tarjeta></div></>;
}
