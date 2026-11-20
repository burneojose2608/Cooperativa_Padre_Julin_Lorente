import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/cliente";
import { useAuth } from "../../context/AuthContext";
import useRecurso from "../../hooks/useRecurso";
import { RUTA_DE_AREA } from "../../utils/areas";
import { PIAuditoria, PIBeneficios, PICapacitacion, PICompartir, PICopiar, PIEditar, PIJuegos, PINotificaciones, PIOk,
  PICopa, PIParametros, PIPuntos, PIReferidos, PIRoles, PIUsuarios, PIContenidos } from "../IconosPanel";
import { MENUS } from "../menus";
import InicioAdmin from "./InicioAdmin";
import InicioGestor from "./InicioGestor";
import "./inicio.css";

const FLECHA = " →";
const fechaCorta = (iso) => { try { return new Date(iso).toLocaleString("es-EC", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" }); } catch { return ""; } };

/** Foto real del usuario (si la subió); si no, sus iniciales. */
function Foto({ perfil, usuario }) {
  const [url, setUrl] = useState("");
  useEffect(() => {
    let vigente = true, enlace;
    if (perfil?.tiene_foto) api.archivoProtegido("/auth/yo/foto/").then((blob) => { enlace = URL.createObjectURL(blob); if (vigente) setUrl(enlace); }).catch(() => {});
    return () => { vigente = false; if (enlace) URL.revokeObjectURL(enlace); };
  }, [perfil]);
  const ini = `${usuario.nombre?.[0] ?? ""}${usuario.apellido?.[0] ?? ""}`.toUpperCase() || "U";
  return url ? <img className="ini-foto" src={url} alt="Tu foto de perfil" /> : <span className="ini-foto ini-foto--ini" aria-hidden="true">{ini}</span>;
}

function MiPerfil({ base, usuario }) {
  const p = useRecurso("/auth/yo/"); const d = p.datos;
  return (
    <section className="ini-tarjeta ini-perfil" aria-label="Mi perfil">
      <header><h2>Mi perfil</h2><Link className="ini-chip" to={`${base}/perfil`}><PIEditar />Editar</Link></header>
      <div className="ini-perfil__id"><Foto perfil={d} usuario={usuario} />
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

const Proximo = ({ icono: Ico, etq, tono }) => (
  <div className={`ini-kpi ini-kpi--${tono}`}><span className="ini-kpi__ico"><Ico /></span>
    <div><strong aria-label="Sin datos todavía">—</strong><span>{etq}</span><small>Próximamente</small></div></div>
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
  return (
    <div className="ini">
      <section className="ini-hero" aria-label="Bienvenida">
        <div><p className="ini-hero__etq">{esSocio ? "Tu comunidad cooperativa" : "Tu espacio de trabajo"}</p>
          <h1>¡Hola, {usuario.nombre}!</h1>
          <p className="ini-hero__txt">{esSocio ? "Sigue refiriendo y comparte tu código con quienes quieras invitar." : "Cooperativa de Ahorro y Crédito Padre Julián Lorente."}</p>
          <Link className="boton boton--amarillo" to={esSocio ? `${base}/referidos` : `${base}/perfil`}>{esSocio ? <><PICopiar className="boton__ico" />Compartir mi código</> : "Consultar mi perfil"}</Link></div>
        <svg className="ini-hero__arte" viewBox="40 0 240 200" aria-hidden="true"><circle cx="175" cy="105" r="78" fill="none" stroke="#ffc72c" strokeWidth="26" opacity=".95" /><circle cx="130" cy="95" r="62" fill="#1556bd" />
          <circle cx="82" cy="52" r="9" fill="#ffc72c" /><path d="M110 62h42v26c0 12-9 20-21 20s-21-8-21-20Zm-1 8H98c0 12 6 18 14 19M153 70h11c0 12-6 18-14 19M131 108v14M118 124h26" fill="none" stroke="#ffc72c" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </section>
      {n.error && <p className="ini-error" role="alert">{n.error}</p>}
      {esSocio && <div className="ini-kpis">
        <Proximo icono={PIReferidos} etq="Referidos en proceso" tono="azul" />
        <Proximo icono={PICapacitacion} etq="Capacitaciones disponibles" tono="morado" />
        <Proximo icono={PIJuegos} etq="Juegos activos" tono="verde" />
        <Proximo icono={PIBeneficios} etq="Beneficios a tu alcance" tono="amarillo" />
      </div>}
      <div className="ini-cols">
        <div className="ini-principal">
          {esSocio ? <div className="ini-fila"><MiCodigo base={base} />
            <section className="ini-tarjeta ini-nivel" aria-label="Nivel actual"><header><h2>Nivel actual</h2></header>
              <div className="ini-nivel__ico"><PICopa /></div><p className="ini-sub">Tu nivel y tus puntos aparecerán aquí cuando se habilite el módulo de puntos.</p><small className="ini-prox">Próximamente</small></section></div>
            : <section className="ini-tarjeta" aria-label="Notificaciones"><header><h2>Notificaciones</h2></header>
              <p className="ini-gran">{n.datos?.no_leidas ?? 0}</p><p className="ini-sub">sin leer</p><Link className="boton boton--claro" to={`${base}/notificaciones`}>Ver mi bandeja</Link></section>}
          {esSocio && <section className="ini-banner" aria-label="Invitación a referir"><div><small>Refiere a tus amigos</small><h2>Comparte tu código</h2>
            <p>Invita a quienes quieras a conocer la plataforma.</p></div><Link className="boton boton--amarillo" to={`${base}/referidos`}>Ver mi código{FLECHA}</Link></section>}
          <Accesos area={area} base={base} />
        </div>
        <aside className="ini-lateral">
          {esSocio ? <section className="ini-tarjeta ini-puntos" aria-label="Puntos disponibles"><small>Disponible</small><strong aria-label="Sin datos todavía">—</strong>
              <span>puntos</span><small className="ini-prox">Próximamente</small><Link className="boton boton--amarillo" to={`${base}/puntos`}>Ver movimientos{FLECHA}</Link></section>
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
