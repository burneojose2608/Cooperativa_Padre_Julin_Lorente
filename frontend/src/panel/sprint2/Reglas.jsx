import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { PICalendario, PICerrar, PICupon, PIGuardar, PIMas, PIModulos, PIOk, PIOperaciones, PIPuntos } from "../IconosPanel";
import { Aviso } from "./comunes";
import { useOperacion } from "./operaciones";
import "./usuarios.css";
import "./reglas.css";

const hoyLocal = () => new Date().toLocaleDateString("sv-SE");
const INICIAL = () => ({ tipo_actividad: "CONVERSION_REFERIDO", puntos: 10, limite_periodo: 1, periodo: "DIA", vigente_desde: hoyLocal(), vigente_hasta: "" });
const PERIODOS = { DIA: "Día", MES: "Mes", ANIO: "Año" };
const fecha = (iso) => iso ? new Date(`${iso}T00:00:00`).toLocaleDateString("es-EC", { day: "2-digit", month: "short", year: "numeric" }).replace(".", "") : "";
function estado(v) {
  if (v.actual) return ["Vigente", "vigente"];
  if (v.vigente_desde > hoyLocal()) return ["Programada", "programada"];
  return ["Finalizada", "finalizada"];
}
function Campo({ etiqueta, requerido, icono: Icono, children }) {
  return <label className="rg-campo"><span>{etiqueta}{requerido && <b aria-hidden="true"> *</b>}</span><div className="rg-input">{Icono && <Icono aria-hidden="true" />}{children}</div></label>;
}

export default function Reglas() {
  const r = useRecurso("/plataforma/reglas-puntos/"); const op = useOperacion(r.recargar);
  const [datos, setDatos] = useState(INICIAL);
  const cambiar = (campo) => (e) => setDatos({ ...datos, [campo]: e.target.value });
  const reglas = r.datos?.reglas ?? [];
  return <div className="us rg">
    <div className="us-cab"><span className="us-cab__ico"><PIPuntos /></span><div className="us-cab__txt"><h1>Reglas de puntos</h1><p>Configura las condiciones para futuras actividades. Cada cambio crea una versión y conserva el historial.</p></div></div>
    <Aviso error={r.error} />
    <div className="rg-grid">
      <section className="us-tarjeta rg-form" aria-label="Nueva versión">
        <header className="rg-tit"><span className="rg-tit__ico rg-tit__ico--azul"><PIMas /></span><div><h2>Nueva versión</h2><p>Define una regla de puntos para una actividad.</p></div></header>
        <form onSubmit={(e) => { e.preventDefault(); op.ejecutar(() => api.postProtegido("/plataforma/reglas-puntos/", { ...datos, puntos: Number(datos.puntos), limite_periodo: Number(datos.limite_periodo), vigente_hasta: datos.vigente_hasta || null })); }}>
          <Campo etiqueta="Actividad" requerido icono={PICupon}><select value={datos.tipo_actividad} onChange={cambiar("tipo_actividad")}>{r.datos?.actividades.map((a) => <option key={a}>{a}</option>)}</select></Campo>
          <Campo etiqueta="Puntos por actividad" requerido icono={PIPuntos}><input type="number" required min="1" max="1000000" value={datos.puntos} onChange={cambiar("puntos")} /></Campo>
          <Campo etiqueta="Máximo de actividades por período" requerido icono={PIOperaciones}><input type="number" required min="1" max="1000000" value={datos.limite_periodo} onChange={cambiar("limite_periodo")} /></Campo>
          <Campo etiqueta="Período" requerido icono={PICalendario}><select value={datos.periodo} onChange={cambiar("periodo")}>{Object.keys(PERIODOS).map((p) => <option key={p} value={p}>{PERIODOS[p]}</option>)}</select></Campo>
          <div className="rg-fechas">
            <Campo etiqueta="Vigente desde" requerido icono={PICalendario}><input type="date" required min={hoyLocal()} value={datos.vigente_desde} onChange={cambiar("vigente_desde")} /></Campo>
            <Campo etiqueta="Vigente hasta (opcional)" icono={PICalendario}><input type="date" min={datos.vigente_desde} value={datos.vigente_hasta} onChange={cambiar("vigente_hasta")} /></Campo>
          </div>
          <div className="rg-estado">{op.error ? <p className="alerta alerta--error" role="alert">{op.error}</p> : op.mensaje ? <p className="rg-ok" role="status"><PIOk aria-hidden="true" />{op.mensaje}</p> : null}</div>
          <div className="rg-botones">
            <button type="button" className="boton boton--claro" disabled={op.ocupado} onClick={() => setDatos(INICIAL())}><PICerrar className="boton__ico" />Cancelar</button>
            <button className="boton boton--amarillo" disabled={op.ocupado}><PIGuardar className="boton__ico" />{op.ocupado ? "Creando…" : "Crear versión"}</button>
          </div>
        </form>
      </section>
      <section className="us-tarjeta rg-lista" aria-label="Versiones registradas">
        <header className="rg-tit"><span className="rg-tit__ico"><PIModulos /></span><div><h2>Versiones registradas</h2><p>Historial de reglas de puntos creadas.</p></div></header>
        {!r.datos ? <p className="us-vacio" role="status">Cargando reglas…</p> : reglas.length === 0 ? <p className="us-vacio">Todavía no hay reglas.</p> : <>
          <div className="us-tabla rg-tabla"><table>
            <thead><tr><th scope="col">Versión</th><th scope="col">Actividad</th><th scope="col">Puntos</th><th scope="col">Límite por período</th><th scope="col">Vigencia</th><th scope="col">Estado</th></tr></thead>
            <tbody>{reglas.map((v) => { const [etq, clase] = estado(v); return <tr key={v.id}>
              <td data-etq="Versión"><span className="rg-ver">v{v.version}</span></td>
              <td data-etq="Actividad" className="rg-act">{v.tipo_actividad}</td>
              <td data-etq="Puntos"><strong>{v.puntos}</strong></td>
              <td data-etq="Límite por período">{v.limite_periodo} por {(PERIODOS[v.periodo] ?? v.periodo).toLowerCase()}</td>
              <td data-etq="Vigencia">{fecha(v.vigente_desde)}<small>{v.vigente_hasta ? `hasta ${fecha(v.vigente_hasta)}` : "Sin fecha de fin"}</small></td>
              <td data-etq="Estado"><span className={`us-estado rg-est rg-est--${clase}`}>{etq}</span></td>
            </tr>; })}</tbody></table></div>
          <div className="us-pie"><span>Mostrando {reglas.length} {reglas.length === 1 ? "versión" : "versiones"}</span></div></>}
      </section>
    </div>
  </div>;
}
