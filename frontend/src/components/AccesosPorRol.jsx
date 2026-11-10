import { Link } from "react-router-dom";
import { AREAS, RUTA_DE_AREA } from "../utils/areas";


export default function AccesosPorRol({ usuario, areaActual, enMenu = false }) {
  const areas = [...new Set(usuario.areas || [])].filter((area) => AREAS[area] && RUTA_DE_AREA[area]);
  if (areas.length < 2) return null;
  return (
    <nav className={enMenu ? "menu__otras" : "panel__roles"} aria-label="Áreas disponibles">
      <small>Tus áreas</small>
      {areas.map((area) => <Link key={area} to={RUTA_DE_AREA[area]}
        className={enMenu ? "menu__item" : "enlace acceso-area"}
        aria-current={area === areaActual ? "page" : undefined}>{AREAS[area].nombre}</Link>)}
    </nav>
  );
}
