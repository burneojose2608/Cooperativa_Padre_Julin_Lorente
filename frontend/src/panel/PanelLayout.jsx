import { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { api } from "../api/cliente";
import AccesosPorRol from "../components/AccesosPorRol";
import Marca from "../components/Marca";
import { useAuth } from "../context/AuthContext";
import { AREAS, RUTA_DE_AREA } from "../utils/areas";
import { PIMenu, PINotificaciones, PISalir } from "./IconosPanel";
import { MENUS } from "./menus";

const iniciales = (u) => `${u.nombre?.[0] ?? ""}${u.apellido?.[0] ?? ""}`.toUpperCase() || "U";

/** Marco común de los paneles: menú lateral azul (en celular, un cajón) + barra superior. */
export default function PanelLayout({ area, children }) {
  const { usuario, salir } = useAuth();
  const [abierto, setAbierto] = useState(false);
  const base = RUTA_DE_AREA[area];
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
      <aside className={`menu ${abierto ? "menu--abierto" : ""}`} aria-label="Menú principal">
        <div className="menu__marca"><Marca claro compacta /></div>
        <nav>
          {MENUS[area].map(({ ruta, etq, ico: Ico }) => (
            <NavLink key={etq} end={ruta === ""} to={ruta ? `${base}/${ruta}` : base} className="menu__item" onClick={() => setAbierto(false)}>
              <Ico /><span>{etq}</span>
            </NavLink>
          ))}
        </nav>
        <AccesosPorRol usuario={usuario} areaActual={area} enMenu />
      </aside>
      <div className="shell__cuerpo">
        <header className="barra">
          <button className="icono-btn barra__menu" onClick={() => setAbierto(true)} aria-label="Abrir menú"><PIMenu /></button>
          <span className="barra__area">{AREAS[area].nombre}</span>
          <div className="barra__der">
            <Link className="icono-btn" to={`${base}/notificaciones`} aria-label={`Notificaciones: ${noLeidas} sin leer`}><PINotificaciones />{noLeidas > 0 && <small>{noLeidas}</small>}</Link>
            <Link className="barra__perfil" to={`${base}/perfil`}><span className="avatar">{iniciales(usuario)}</span>
              <span className="barra__nombre">{usuario.nombre}</span></Link>
            <button className="boton boton--claro barra__salir" onClick={salir}><PISalir className="boton__ico" /><span>Cerrar sesión</span></button>
          </div>
        </header>
        <main className="pagina">{children}</main>
      </div>
    </div>
  );
}
