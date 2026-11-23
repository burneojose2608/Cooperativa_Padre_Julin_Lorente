import { useEffect, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { api } from "../api/cliente";
import AccesosPorRol from "../components/AccesosPorRol";
import Marca from "../components/Marca";
import FotoPerfil from "../components/FotoPerfil";
import { useAuth } from "../context/AuthContext";
import { AREAS, RUTA_DE_AREA } from "../utils/areas";
import { PIMenu, PINotificaciones, PISalir } from "./IconosPanel";
import { MENUS } from "./menus";

function Navegacion({ grupos, base, grupoActivo, cerrar }) {
  const [abierto, setAbierto] = useState(grupoActivo);
  const enlace = ({ ruta, etq, ico: Icono }) => (
    <NavLink key={ruta} end={ruta === ""} to={ruta ? `${base}/${ruta}` : base} className="menu__item" onClick={cerrar}>
      <Icono aria-hidden="true" /><span>{etq}</span>
    </NavLink>
  );
  return <nav aria-label="Secciones del panel">
    {[...grupos].map(([grupo, entradas], indice) => {
      if (!grupo) return entradas.map(enlace);
      const id = `menu-grupo-${indice}`;
      const expandido = abierto === grupo;
      return <div className="menu__entrada" key={grupo}>
        <button type="button" className="menu__grupo" aria-expanded={expandido} aria-controls={id}
          onClick={() => setAbierto(expandido ? null : grupo)}>
          {grupo}<span className="menu__flecha" aria-hidden="true" />
        </button>
        <div className="menu__enlaces" id={id} hidden={!expandido}>{entradas.map(enlace)}</div>
      </div>;
    })}
  </nav>;
}

/** Marco común de los paneles: menú lateral azul (en celular, un cajón) + barra superior. */
export default function PanelLayout({ area, children }) {
  const { usuario, salir } = useAuth();
  const [abierto, setAbierto] = useState(false);
  const base = RUTA_DE_AREA[area];
  const { pathname } = useLocation();
  const grupos = new Map();
  let grupoActivo = null;
  const rutaActual = pathname.slice(base.length).split("/")[1];
  for (const entrada of MENUS[area]) {
    const grupo = entrada.ruta ? entrada.grupo : null;
    if (!grupos.has(grupo)) grupos.set(grupo, []);
    grupos.get(grupo).push(entrada);
    if (entrada.ruta === rutaActual) grupoActivo = grupo;
  }
  const [noLeidas, setNoLeidas] = useState(0);
  useEffect(() => {
    let vigente = true;
    const cargar = () => api.getProtegido("/plataforma/notificaciones/").then((r) => { if (vigente) setNoLeidas(r.no_leidas); }).catch(() => {});
    cargar(); const intervalo = setInterval(cargar, 30000);
    window.addEventListener("coop:notificaciones", cargar);
    return () => { vigente = false; clearInterval(intervalo); window.removeEventListener("coop:notificaciones", cargar); };
  }, []);

  return (
    <div className="shell">
      {abierto && <div className="shell__velo" onClick={() => setAbierto(false)} />}
      <aside id="menu-principal" className={`menu ${abierto ? "menu--abierto" : ""}`} aria-label="Menú principal"
        onKeyDown={(e) => { if (e.key === "Escape" && abierto) setAbierto(false); }}>
        <div className="menu__marca"><Marca claro compacta /></div>
        <Navegacion key={`${area}:${grupoActivo}`} grupos={grupos} grupoActivo={grupoActivo} base={base} cerrar={() => setAbierto(false)} />
        <AccesosPorRol usuario={usuario} areaActual={area} enMenu />
      </aside>
      <div className="shell__cuerpo">
        <header className="barra">
          <button className="icono-btn barra__menu" onClick={() => setAbierto(!abierto)} aria-label={abierto ? "Cerrar menú" : "Abrir menú"}
            aria-expanded={abierto} aria-controls="menu-principal"><PIMenu /></button>
          <span className="barra__area">{AREAS[area].nombre}</span>
          <div className="barra__der">
            <Link className="icono-btn barra__avisos" to={`${base}/notificaciones`} aria-label={`Notificaciones: ${noLeidas} sin leer`}>
              <PINotificaciones />{noLeidas > 0 && <small aria-hidden="true">{noLeidas > 99 ? "99+" : noLeidas}</small>}
            </Link>
            <Link className="barra__perfil" to={`${base}/perfil`} aria-label="Mi perfil"><FotoPerfil perfil={usuario} className="avatar" />
              <span className="barra__nombre">{usuario.nombre}</span></Link>
            <button className="boton boton--claro barra__salir" aria-label="Cerrar sesión" onClick={salir}><PISalir className="boton__ico" /><span>Cerrar sesión</span></button>
          </div>
        </header>
        <main className="pagina">{children}</main>
      </div>
    </div>
  );
}
