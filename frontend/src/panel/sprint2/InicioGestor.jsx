import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import useRecurso from "../../hooks/useRecurso";
import { PIAlerta, PICapacitacion, PIChevron, PIContenidos, PIInicio, PIModulos, PINotificaciones, PIOk, PIPulso, PIReloj } from "../IconosPanel";
import "./usuarios.css";
import "./inicioadmin.css";

const hoyLocal = () => new Date().toLocaleDateString("sv-SE");
const MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
function hace(iso) {
  const min = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
  if (Number.isNaN(min)) return "";
  if (min < 1) return "Ahora"; if (min < 60) return `Hace ${min} min`;
  const h = Math.round(min / 60); if (h < 24) return `Hace ${h} h`;
  const d = Math.round(h / 24); return d < 30 ? `Hace ${d} ${d === 1 ? "día" : "días"}` : new Date(iso).toLocaleDateString("es-EC", { day: "2-digit", month: "short", year: "numeric" });
}
const Kpi = ({ icono: Ico, valor, etq, tono, proximo }) => (
  <div className={`ia-kpi ia-kpi--${tono}`}><span className="ia-kpi__ico"><Ico /></span>
    <div><strong aria-label={proximo ? "Sin datos todavía" : undefined}>{valor ?? "—"}</strong><span>{etq}</span>{proximo && <small className="ig-prox">Próximamente</small>}</div></div>
);
/** Contenidos por mes del año actual, según su fecha de inicio (dato real). */
function Grafico({ lista }) {
  const anio = new Date().getFullYear();
  const cuentas = MESES.map((_, m) => lista.filter((c) => { const d = c.desde ? new Date(`${c.desde}T00:00:00`) : null; return d && d.getFullYear() === anio && d.getMonth() === m; }).length);
  const max = Math.max(1, ...cuentas);
  return <div className="ia-grafico ig-grafico" role="img" aria-label={`Contenidos por mes en ${anio}. ${MESES.map((m, i) => `${m}: ${cuentas[i]}`).join(", ")}`}>
    {MESES.map((m, i) => <div className="ia-barra" key={m} title={`${cuentas[i]} contenidos`}><span className="ia-barra__n">{cuentas[i] || ""}</span>
      <span className="ia-barra__col" style={{ height: `${Math.max(4, (cuentas[i] / max) * 100)}%` }} /><span className="ia-barra__dia">{m}</span></div>)}
  </div>;
}

export default function InicioGestor({ base }) {
  const { usuario } = useAuth();
  const c = useRecurso("/plataforma/contenidos/"); const n = useRecurso("/plataforma/notificaciones/");
  const lista = Array.isArray(c.datos) ? c.datos : null; const hoy = hoyLocal();
  const cuenta = (f) => lista ? lista.filter(f).length : undefined;
  const programados = (x) => x.estado === "PUBLICADO" && !x.visible && x.desde > hoy;
  const eventos = n.datos?.resultados ?? [];
  const ACCESOS = [["Gestionar contenidos", "gestionar", PIContenidos], ["Material educativo", "materiales", PICapacitacion], ["Publicaciones", "contenidos", PIModulos], ["Notificaciones", "notificaciones", PINotificaciones]];
  return <div className="ia">
    <div className="us-cab"><span className="us-cab__ico"><PIInicio /></span><div className="us-cab__txt"><h1>Panel principal</h1><p>Vista de {usuario.roles?.[0] ?? "Gestor de contenidos"}</p></div></div>
    <section className="ia-hero" aria-label="Bienvenida">
      <div><p className="ia-hero__etq">Cooperativa Padre Julián Lorente</p><h1>Historias útiles para nuestra comunidad</h1>
        <p className="ia-hero__txt">Crea, publica y modera contenido educativo y cercano.</p></div>
      <div className="ia-hero__arte" aria-hidden="true"><span className="ia-hero__aro" /><span className="ia-hero__circulo"><PIPulso /></span></div>
    </section>
    {(c.error || n.error) && <p className="ini-error" role="alert">{c.error || n.error}</p>}
    <div className="ia-kpis">
      <Kpi icono={PIContenidos} valor={cuenta((x) => x.estado === "BORRADOR")} etq="Borradores" tono="amarillo" />
      <Kpi icono={PIOk} valor={cuenta((x) => x.estado === "PUBLICADO" && x.visible)} etq="Publicados" tono="verde" />
      <Kpi icono={PIReloj} valor={cuenta(programados)} etq="Programados" tono="azul" />
      <Kpi icono={PIAlerta} valor="—" etq="Reportes pendientes" tono="morado" proximo />
    </div>
    <div className="ia-fila">
      <section className="ia-tarjeta" aria-label="Contenidos por mes"><header><div><h2>Contenidos por mes</h2><p>Según la fecha de inicio de cada contenido, en {new Date().getFullYear()}.</p></div>{lista && <span className="ia-estado"><i />Actualizado</span>}</header>
        {lista ? <Grafico lista={lista} /> : <p className="ia-vacio">{c.error ? "No se pudo cargar." : "Cargando…"}</p>}</section>
      <section className="ia-tarjeta" aria-label="Accesos rápidos"><header><div><h2>Accesos rápidos</h2><p>Continúa con una tarea frecuente.</p></div></header>
        <div className="ia-accesos">{ACCESOS.map(([etq, ruta, Ico]) => <Link key={ruta} className="ia-acceso" to={`${base}/${ruta}`}><span className="ia-acceso__ico"><Ico /></span><strong>{etq}</strong><PIChevron className="ia-acceso__flecha" /></Link>)}</div></section>
    </div>
    <section className="ia-tarjeta" aria-label="Últimos eventos"><header><div><h2>Últimos eventos</h2><p>Tus notificaciones más recientes.</p></div>
      <Link className="ia-ver" to={`${base}/notificaciones`}>Ver todo<PIChevron /></Link></header>
      {eventos.length > 0 ? <ul className="ia-eventos">{eventos.slice(0, 4).map((e) => <li key={e.id}><span className="ia-eventos__ico" aria-hidden="true"><PINotificaciones /></span>
        <div><strong>{e.titulo}</strong><small>{hace(e.creada_en)}</small></div></li>)}</ul>
        : <p className="ia-vacio">{n.datos ? "Aún no tienes actividad reciente." : n.error ? "No se pudo cargar." : "Cargando…"}</p>}</section>
  </div>;
}
