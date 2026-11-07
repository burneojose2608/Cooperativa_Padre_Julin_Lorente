import { useState } from "react";
import { NavLink, Link } from "react-router-dom";
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
  const otras = (usuario.areas || []).filter((a) => a !== area && MENUS[a]);

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
        {otras.length > 0 && (
          <div className="menu__otras">
            <small>Cambiar de área</small>
            {otras.map((a) => <Link key={a} to={RUTA_DE_AREA[a]} className="menu__item">{AREAS[a].nombre}</Link>)}
          </div>
        )}
      </aside>
      <div className="shell__cuerpo">
        <header className="barra">
          <button className="icono-btn barra__menu" onClick={() => setAbierto(true)} aria-label="Abrir menú"><PIMenu /></button>
          <span className="barra__area">{AREAS[area].nombre}</span>
          <div className="barra__der">
            <button className="icono-btn" aria-label="Notificaciones"><PINotificaciones /></button>
            <div className="barra__perfil"><span className="avatar">{iniciales(usuario)}</span>
              <span className="barra__nombre">{usuario.nombre}</span></div>
            <button className="boton boton--claro barra__salir" onClick={salir}><PISalir className="boton__ico" /><span>Cerrar sesión</span></button>
          </div>
        </header>
        <main className="pagina">{children}</main>
      </div>
    </div>
  );
}
