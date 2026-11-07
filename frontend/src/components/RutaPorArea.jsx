import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";

/** Deja pasar solo a quien tenga el rol de esa área. A los demás los manda a SU pantalla.
 *  (La seguridad real está en el servidor; esto solo decide qué se muestra.) */
export default function RutaPorArea({ area, children }) {
  const { usuario, verificando } = useAuth();
  if (verificando) return <p className="cargando">Cargando…</p>;
  if (!usuario) return <Navigate to="/ingresar" replace />;
  if (!usuario.areas?.includes(area)) return <Navigate to={rutaDe(usuario.area)} replace />;
  return children;
}
