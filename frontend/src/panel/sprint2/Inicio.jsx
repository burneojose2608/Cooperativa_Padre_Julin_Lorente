import { useState } from "react";
import { Link } from "react-router-dom";
import FotoPerfil from "../../components/FotoPerfil";
import { useAuth } from "../../context/AuthContext";
import useRecurso from "../../hooks/useRecurso";
import { RUTA_DE_AREA } from "../../utils/areas";
import { PIAuditoria, PIBeneficios, PICapacitacion, PICompartir, PICopiar, PIEditar, PIJuegos, PINotificaciones, PIOk,
  PICopa, PIParametros, PIPuntos, PIReferidos, PIRoles, PIUsuarios } from "../IconosPanel";
import { MENUS } from "../menus";
import InicioAdmin from "./InicioAdmin";
import InicioGestor from "./InicioGestor";
import "./inicio.css";

const FLECHA = " →";
const fechaCorta = (iso) => { try { return new Date(iso).toLocaleString("es-EC", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" }); } catch { return ""; } };

function MiPerfil({ base, usuario }) {
  const p = useRecurso("/auth/yo/"); const d = p.datos;
  return (
    <section className="ini-tarjeta ini-perfil" aria-label="Mi perfil">
      <header><h2>Mi perfil</h2><Link className="ini-chip" to={`${base}/perfil`}><PIEditar />Editar</Link></header>
      <div className="ini-perfil__id"><FotoPerfil perfil={d ?? usuario} className="ini-foto" claseIniciales="ini-foto ini-foto--ini" alt="Tu foto de perfil" />
        <div><strong>{usuario.nombre} {usuario.apellido}</strong><span className="ini-rol">{usuario.roles?.join(", ")}</span></div></div>
      <dl className="ini-datos">
        {d?.cedula && <><dt>Cédula</dt><dd>{d.cedula}</dd></>}
        {d?.correo && <><dt>Correo</dt><dd>{d.correo}</dd></>}
        {d?.telefono && <><dt>Teléfono</dt><dd>{d.telefono}</dd></>}
        {!d && !p.error && <dd>Cargando…</dd>}
      </dl>
      {p.error && <p className="ini-error" role="alert">{p.error}</p>}
    </section>
  );
}

/** Código real del backend: copiar enlace y compartir. */
function MiCodigo({ base }) {
  const r = useRecurso("/plataforma/referidos/codigo/"); const [aviso, setAviso] = useState("");
  const decir = (t) => { setAviso(t); setTimeout(() => setAviso(""), 2200); };
  const copiar = async () => { try { await navigator.clipboard.writeText(r.datos.enlace); decir("¡Enlace copiado!"); } catch { decir("Tu navegador bloqueó el portapapeles."); } };
  const compartir = async () => {
    if (!navigator.share) return copiar();
    try { await navigator.share({ title: "Cooperativa Padre Julián Lorente", text: "Te invito a conocer nuestra plataforma", url: r.datos.enlace }); }
    catch (e) { if (e.name !== "AbortError") copiar(); }
  };
  return (
    <section className="ini-tarjeta" aria-label="Tu código de referido">
      <header><h2>Tu código de referido</h2></header>
      <p className="ini-sub">Invita a más personas a la plataforma.</p>
      {r.error && <p className="ini-error" role="alert">{r.error}</p>}
      {r.datos ? <>
        <p className="ini-codigo">{r.datos.codigo}</p>
        <div className="ini-botones">
          <button className="boton boton--claro" onClick={copiar}>{aviso.startsWith("¡") ? <PIOk className="boton__ico" /> : <PICopiar className="boton__ico" />}Copiar enlace</button>
          <button className="boton boton--amarillo" onClick={compartir}><PICompartir className="boton__ico" />Compartir</button>
        </div>
        <p className="ini-aviso" role="status">{aviso}</p>
      </> : !r.error && <p className="ini-sub">Cargando…</p>}
      <Link className="ini-enlace" to={`${base}/referidos`}>Ver detalle{FLECHA}</Link>
    </section>
  );
}

const KpiVivo = ({ icono: Ico, valor, etq, tono, sub }) => (
  <div className={`ini-kpi ini-kpi--${tono}`}><span className="ini-kpi__ico"><Ico /></span>
    <div><strong>{valor ?? "—"}</strong><span>{etq}</span>{sub && <small className="ini-kpi__sub">{sub}</small>}</div></div>
);

function Actividad({ lista, base, sinLeer }) {
  return (
    <section className="ini-tarjeta" aria-label="Actividad reciente">
      <header><div><h2>Actividad reciente</h2>{sinLeer > 0 && <p className="ini-sub">{sinLeer} {sinLeer === 1 ? "aviso sin leer" : "avisos sin leer"}</p>}</div><Link className="ini-enlace" to={`${base}/notificaciones`}>Ver todo{FLECHA}</Link></header>
      {lista && lista.length > 0
        ? <ul className="ini-actividad">{lista.slice(0, 4).map((n) => <li key={n.id} className={n.leida_en ? "" : "ini-nueva"}>
            <span className="ini-actividad__ico"><PINotificaciones /></span>
            <div><strong>{n.titulo}</strong><small>{fechaCorta(n.creada_en)}</small></div></li>)}</ul>
        : <p className="ini-sub">{lista ? "Aún no tienes actividad reciente." : "Cargando…"}</p>}
    </section>
  );
}

const ACCESOS = {
  socio: [["Mi perfil", "perfil", PIUsuarios, "azul"], ["Mis puntos", "puntos", PIPuntos, "amarillo"],
    ["Capacitaciones", "capacitaciones", PICapacitacion, "verde"], ["Beneficios", "beneficios", PIBeneficios, "morado"]],
  admin: [["Usuarios", "usuarios", PIUsuarios, "azul"], ["Roles y permisos", "roles", PIRoles, "verde"],
    ["Reglas de puntos", "parametros", PIParametros, "amarillo"], ["Auditoría", "auditoria", PIAuditoria, "rojo"]],
};
function Accesos({ area, base }) {
  const lista = ACCESOS[area] || MENUS[area].filter((m) => m.ruta && m.ruta !== "perfil").slice(0, 4).map((m, i) => [m.etq, m.ruta, m.ico, ["azul", "verde", "amarillo", "morado"][i]]);
  return (
    <section className="ini-tarjeta" aria-label="Accesos rápidos"><header><div><h2>Accesos rápidos</h2><p className="ini-sub">Todo lo que necesitas, a un clic.</p></div></header>
      <div className="ini-accesos">{lista.map(([etq, ruta, Ico, tono]) => (
        <Link key={ruta} className={`ini-acceso ini-acceso--${tono}`} to={`${base}/${ruta}`}><Ico /><span>{etq}</span></Link>))}</div>
    </section>
  );
}

function InicioGeneral({ area }) {
  const { usuario } = useAuth(); const base = RUTA_DE_AREA[area]; const n = useRecurso("/plataforma/notificaciones/");
  const esSocio = area === "socio";
  const puntos = useRecurso(esSocio ? "/plataforma/negocio/puntos/" : null);
  const referidos = useRecurso(esSocio ? "/plataforma/negocio/referidos/" : null);
  const cursos = useRecurso(esSocio ? "/plataforma/negocio/capacitaciones/" : null);
  const juegos = useRecurso(esSocio ? "/plataforma/negocio/juegos/" : null);
  const beneficios = useRecurso(esSocio ? "/plataforma/negocio/beneficios/" : null);
  const referidosActivos = referidos.datos?.resultados?.filter((r) => !["RECHAZADO", "EXPIRADO"].includes(r.estado)).length;
  const subtituloArea = {
    marketing: "Gestiona campañas, seguimiento comercial, sorteos y reportes de captación.",
    rse: "Administra capacitaciones, talleres, convenios de bienestar e impacto social.",
  }[area] || "Cooperativa de Ahorro y Crédito Padre Julián Lorente.";
  const accionArea = {
    socio: [`${base}/referidos`, <><PICopiar className="boton__ico" />Compartir mi código</>],
    marketing: [`${base}/campanas`, "Gestionar campañas"],
    rse: [`${base}/capacitaciones`, "Gestionar formación"],
  }[area] || [`${base}/perfil`, "Consultar mi perfil"];
  return (
    <div className="ini">
      <section className="ini-hero" aria-label="Bienvenida">
        <div><p className="ini-hero__etq">{esSocio ? "Tu comunidad cooperativa" : "Tu espacio de trabajo"}</p>
          <h1>¡Hola, {usuario.nombre}!</h1>
          <p className="ini-hero__txt">{esSocio ? "Consulta tus puntos, comparte tu código de referido y participa en formación y recompensas." : subtituloArea}</p>
          <Link className="boton boton--amarillo" to={accionArea[0]}>{accionArea[1]}</Link></div>
        <svg className="ini-hero__arte" viewBox="40 0 240 200" aria-hidden="true"><circle cx="175" cy="105" r="78" fill="none" stroke="#ffc72c" strokeWidth="26" opacity=".95" /><circle cx="130" cy="95" r="62" fill="#1556bd" />
          <circle cx="82" cy="52" r="9" fill="#ffc72c" /><path d="M110 62h42v26c0 12-9 20-21 20s-21-8-21-20Zm-1 8H98c0 12 6 18 14 19M153 70h11c0 12-6 18-14 19M131 108v14M118 124h26" fill="none" stroke="#ffc72c" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </section>
      {n.error && <p className="ini-error" role="alert">{n.error}</p>}
      {esSocio && <div className="ini-kpis">
        <KpiVivo icono={PIReferidos} valor={referidosActivos} etq="Referidos activos" tono="azul" />
        <KpiVivo icono={PICapacitacion} valor={cursos.datos?.resultados?.length} etq="Capacitaciones" tono="morado" />
        <KpiVivo icono={PIJuegos} valor={juegos.datos?.resultados?.length} etq="Juegos activos" tono="verde" />
        <KpiVivo icono={PIBeneficios} valor={beneficios.datos?.resultados?.length} etq="Beneficios" tono="amarillo" />
      </div>}
      <div className="ini-cols">
        <div className="ini-principal">
          {esSocio ? <div className="ini-fila"><MiCodigo base={base} />
            <section className="ini-tarjeta ini-nivel" aria-label="Nivel actual"><header><h2>Nivel actual</h2><Link className="ini-enlace" to={`${base}/ranking`}>Clasificación{FLECHA}</Link></header>
              <div className="ini-nivel__ico"><PICopa /></div>
              <strong className="ini-gran">{puntos.datos?.nivel ?? "Inicial"}</strong>
              <p className="ini-sub">{puntos.datos?.insignias?.length ? `${puntos.datos.insignias.length} insignias obtenidas` : "Completa actividades validadas para subir de nivel y ganar insignias."}</p>
            </section></div>
            : <section className="ini-tarjeta" aria-label="Notificaciones"><header><h2>Notificaciones</h2></header>
              <p className="ini-gran">{n.datos?.no_leidas ?? 0}</p><p className="ini-sub">sin leer</p><Link className="boton boton--claro" to={`${base}/notificaciones`}>Ver mi bandeja</Link></section>}
          {esSocio && <section className="ini-banner" aria-label="Invitación a referir"><div><small>Refiere a tus amigos</small><h2>Comparte tu código</h2>
            <p>Invita a quienes quieras a conocer la plataforma y acumula puntos con cada conversión validada.</p></div><Link className="boton boton--amarillo" to={`${base}/referidos`}>Ver mis referidos{FLECHA}</Link></section>}
          <Accesos area={area} base={base} />
        </div>
        <aside className="ini-lateral">
          {esSocio ? <section className="ini-tarjeta ini-puntos" aria-label="Puntos disponibles"><small>Disponible</small><strong>{puntos.datos?.saldo ?? 0}</strong>
              <span>puntos</span><Link className="boton boton--amarillo" to={`${base}/puntos`}>Ver movimientos{FLECHA}</Link></section>
            : <MiPerfil base={base} usuario={usuario} />}
          <Actividad lista={n.datos?.resultados} base={base} sinLeer={n.datos?.no_leidas} />
        </aside>
      </div>
    </div>
  );
}

/** El administrador tiene su propio Inicio (supervisión); los demás roles usan el general. */
export default function Inicio({ area }) {
  if (area === "admin") return <InicioAdmin base={RUTA_DE_AREA.admin} />;
  if (area === "contenidos") return <InicioGestor base={RUTA_DE_AREA.contenidos} />;
  return <InicioGeneral area={area} />;
}
