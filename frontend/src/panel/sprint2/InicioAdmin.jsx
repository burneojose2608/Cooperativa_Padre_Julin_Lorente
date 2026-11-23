import { Link } from "react-router-dom";
import useRecurso from "../../hooks/useRecurso";
import { PIChevron, PIHistorial, PIEscudo, PIParametros, PIPulso, PIUsuarios, PIValidar, PIOk } from "../IconosPanel";
import "./inicioadmin.css";

const DIAS = 7;
const mismoDia = (a, b) => a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
const humanizar = (t = "") => { const s = t.replace(/_/g, " ").toLowerCase(); return s.charAt(0).toUpperCase() + s.slice(1); };
function hace(iso) {
  const min = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
  if (Number.isNaN(min)) return "";
  if (min < 1) return "Ahora"; if (min < 60) return `Hace ${min} min`;
  const h = Math.round(min / 60); if (h < 24) return `Hace ${h} h`;
  const d = Math.round(h / 24); return d < 30 ? `Hace ${d} ${d === 1 ? "día" : "días"}` : new Date(iso).toLocaleDateString("es-EC", { day: "2-digit", month: "short", year: "numeric" });
}

/** Un número real del backend; si falla o aún carga, muestra «—». */
const Kpi = ({ icono: Ico, valor, etq, tono }) => (
  <div className={`ia-kpi ia-kpi--${tono}`}><span className="ia-kpi__ico"><Ico /></span>
    <div><strong>{valor ?? "—"}</strong><span>{etq}</span></div></div>
);

function Grafico({ eventos }) {
  const hoy = new Date();
  const dias = Array.from({ length: DIAS }, (_, i) => { const d = new Date(hoy); d.setDate(hoy.getDate() - (DIAS - 1 - i)); return d; });
  const cuentas = dias.map((d) => eventos.filter((e) => mismoDia(new Date(e.fecha), d)).length);
  const max = Math.max(1, ...cuentas);
  const resumen = dias.map((d, i) => `${d.toLocaleDateString("es-EC", { weekday: "long" })}: ${cuentas[i]}`).join(", ");
  return <div className="ia-grafico" role="img" aria-label={`Eventos de los últimos 7 días. ${resumen}`}>
    {dias.map((d, i) => <div className="ia-barra" key={i} title={`${cuentas[i]} eventos`}>
      <span className="ia-barra__n">{cuentas[i]}</span>
      <span className="ia-barra__col" style={{ height: `${Math.max(4, (cuentas[i] / max) * 100)}%` }} />
      <span className="ia-barra__dia">{d.toLocaleDateString("es-EC", { weekday: "short" }).replace(".", "")}</span></div>)}
  </div>;
}

const ACCESOS = [["Usuarios", "usuarios", PIUsuarios], ["Validar socios", "validar-socios", PIValidar], ["Roles y permisos", "roles", PIEscudo], ["Parámetros", "parametros", PIParametros]];

export default function InicioAdmin({ base }) {
  const u = useRecurso("/auth/administracion/usuarios/?estado=ACTIVA");
  const v = useRecurso("/auth/administracion/cuentas-generales/");
  const ro = useRecurso("/auth/administracion/roles/");
  const au = useRecurso("/auth/administracion/auditoria/");
  const eventos = Array.isArray(au.datos) ? au.datos : [];
  const hoy = new Date(); const deHoy = eventos.filter((e) => mismoDia(new Date(e.fecha), hoy)).length;
  return (
    <div className="ia">
      <section className="ia-hero" aria-label="Bienvenida">
        <div><p className="ia-hero__etq">Cooperativa Padre Julián Lorente</p><h1>Control claro para una comunidad confiable</h1>
          <p className="ia-hero__txt">Supervisa cuentas, permisos y actividad de la plataforma desde un solo lugar.</p></div>
        <div className="ia-hero__arte" aria-hidden="true"><span className="ia-hero__aro" /><span className="ia-hero__circulo"><PIPulso /></span></div>
      </section>
      {(u.error || au.error) && <p className="ini-error" role="alert">{u.error || au.error}</p>}
      <div className="ia-kpis">
        <Kpi icono={PIUsuarios} valor={u.datos?.total} etq="Usuarios activos" tono="azul" />
        <Kpi icono={PIValidar} valor={v.datos?.count} etq="Socios por validar" tono="amarillo" />
        <Kpi icono={PIEscudo} valor={ro.datos?.roles?.length} etq="Roles base" tono="verde" />
        <Kpi icono={PIHistorial} valor={au.datos ? (deHoy >= 100 ? "100+" : deHoy) : undefined} etq="Eventos hoy" tono="morado" />
      </div>
      <div className="ia-fila">
        <section className="ia-tarjeta" aria-label="Actividad del período"><header><div><h2>Actividad del período</h2>
          <p>Eventos registrados en los últimos 7 días (sobre las últimas 100 acciones).</p></div>
          {au.datos && <span className="ia-estado"><i />Actualizado</span>}</header>
          {au.datos ? <Grafico eventos={eventos} /> : <p className="ia-vacio">{au.error ? "No se pudo cargar la actividad." : "Cargando…"}</p>}</section>
        <section className="ia-tarjeta" aria-label="Accesos rápidos"><header><div><h2>Accesos rápidos</h2><p>Continúa con una tarea frecuente.</p></div></header>
          <div className="ia-accesos">{ACCESOS.map(([etq, ruta, Ico]) => <Link key={ruta} className="ia-acceso" to={`${base}/${ruta}`}>
            <span className="ia-acceso__ico"><Ico /></span><strong>{etq}</strong><PIChevron className="ia-acceso__flecha" /></Link>)}</div></section>
      </div>
      <section className="ia-tarjeta" aria-label="Últimos eventos"><header><div><h2>Últimos eventos</h2><p>Actividad registrada en la bitácora de auditoría.</p></div>
        <Link className="ia-ver" to={`${base}/auditoria`}>Ver todo<PIChevron /></Link></header>
        {eventos.length > 0 ? <ul className="ia-eventos">{eventos.slice(0, 5).map((e) => <li key={e.id_auditoria}>
          <span className="ia-eventos__ico" aria-hidden="true"><PIOk /></span>
          <div><strong>{humanizar(e.accion)}</strong><small>{e.usuario_id ? `Usuario #${e.usuario_id}` : "Anónimo"} · {hace(e.fecha)}</small></div></li>)}</ul>
          : <p className="ia-vacio">{au.datos ? "Aún no hay eventos registrados." : au.error ? "No se pudo cargar." : "Cargando…"}</p>}</section>
    </div>
  );
}
