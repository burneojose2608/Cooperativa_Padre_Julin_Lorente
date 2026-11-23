import { Navigate, Route, Routes } from "react-router-dom";
import "./panel.css";
import PanelLayout from "./PanelLayout";
import Inicio from "./sprint2/Inicio";
import Usuarios from "./sprint2/Usuarios";
import Roles from "./sprint2/Roles";
import Reglas from "./sprint2/Reglas";
import { Catalogo, Puntos, Referidos, Canjes, Actividades, Reportes } from "./negocio/Modulos";
import { Comunidad, PerfilPublico, Ranking, Moderacion } from "./negocio/Comunidad";
import { Envios, Segmentos } from "./negocio/Supervision";
import Perfil from "./sprint2/Perfil";
import Notificaciones from "./sprint2/Notificaciones";
import Materiales from "./sprint2/Materiales";
import Auditoria from "./sprint2/Auditoria";
import { GestionContenidos, Publicaciones } from "./sprint2/Contenidos";
import ValidarSocios from "./ValidarSocios";
import { Proximamente } from "./ui";
import { MENUS } from "./menus";
import "./sprint2/sprint2.css";
import { RUTA_DE_AREA } from "../utils/areas";

const TABLAS = {
  socio: { referidos: <Referidos socio />, puntos: <Puntos />, canjes: <Canjes />, actividades: <Actividades />,
    comunidad: <Comunidad />, privacidad: <PerfilPublico />, ranking: <Ranking /> },
  admin: { usuarios: <Usuarios />, roles: <Roles />, parametros: <Reglas />, auditoria: <Auditoria />, "validar-socios": <ValidarSocios />,
    referidos: <Referidos />, canjes: <Canjes />, moderacion: <Moderacion />, reportes: <Reportes area="admin" />, envios: <Envios />, segmentos: <Segmentos /> },
  contenidos: { gestionar: <GestionContenidos />, materiales: <Materiales />, moderacion: <Moderacion /> },
  rse: { materiales: <Materiales />, reportes: <Reportes area="rse" /> },
  marketing: { referidos: <Referidos />, reportes: <Reportes area="marketing" /> },
};
const CATALOGOS = {
  socio: ["campanas", "capacitaciones", "talleres", "juegos", "retos", "beneficios", "sorteos", "convenios"],
  admin: ["campanas", "niveles", "insignias", "capacitaciones", "modulos", "evaluaciones", "talleres", "juegos", "retos", "beneficios", "sorteos", "convenios", "plantillas", "gastos"],
  contenidos: ["capacitaciones", "modulos", "evaluaciones", "talleres", "juegos", "retos", "convenios"],
  rse: ["campanas", "capacitaciones", "modulos", "evaluaciones", "talleres", "convenios"],
  marketing: ["campanas", "beneficios", "sorteos", "retos", "gastos"],
};
for (const [area, recursos] of Object.entries(CATALOGOS)) for (const recurso of recursos) TABLAS[area][recurso] = <Catalogo key={recurso} recurso={recurso} />;

/** Panel con menú lateral para socio, marketing y administración. Cada sección es una sub-ruta. */
export default function PanelRol({ area }) {
  const futuras = Object.fromEntries(MENUS[area].map((m) => [m.ruta, <Proximamente key={m.ruta} titulo={m.etq} />]));
  const rutas = { ...futuras, ...TABLAS[area], "": <Inicio area={area} />, perfil: <Perfil />,
    notificaciones: <Notificaciones />, contenidos: <Publicaciones /> };
  const contenido = (
    <PanelLayout area={area}>
      <Routes>
        {Object.entries(rutas).map(([r, el]) => r === ""
          ? <Route key="i" index element={el} /> : <Route key={r} path={r} element={el} />)}
        <Route path="*" element={<Navigate to={RUTA_DE_AREA[area]} replace />} />
      </Routes>
    </PanelLayout>
  );
  return contenido;
}
