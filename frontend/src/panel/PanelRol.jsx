import { Navigate, Route, Routes } from "react-router-dom";
import "./panel.css";
import PanelLayout from "./PanelLayout";
import { RUTAS_ADMIN } from "./PanelAdmin";
import { RUTAS_MARKETING } from "./PanelMarketing";
import { RUTAS_SOCIO, SocioProvider } from "./PanelSocio";
import { RUTA_DE_AREA } from "../utils/areas";

const TABLAS = { socio: RUTAS_SOCIO, marketing: RUTAS_MARKETING, admin: RUTAS_ADMIN };

/** Panel con menú lateral para socio, marketing y administración. Cada sección es una sub-ruta. */
export default function PanelRol({ area }) {
  const rutas = TABLAS[area];
  const contenido = (
    <PanelLayout area={area}>
      <Routes>
        {Object.entries(rutas).map(([r, el]) => r === ""
          ? <Route key="i" index element={el} /> : <Route key={r} path={r} element={el} />)}
        <Route path="*" element={<Navigate to={RUTA_DE_AREA[area]} replace />} />
      </Routes>
    </PanelLayout>
  );
  return area === "socio" ? <SocioProvider>{contenido}</SocioProvider> : contenido;
}
