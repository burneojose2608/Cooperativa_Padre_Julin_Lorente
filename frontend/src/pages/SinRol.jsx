import { Navigate } from "react-router-dom";
import Marca from "../components/Marca";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";

/** Cuenta válida pero sin ningún rol asignado: no puede entrar a ninguna pantalla. */
export default function SinRol() {
  const { usuario, verificando, salir } = useAuth();
  if (verificando) return <p className="cargando">Cargando…</p>;
  if (!usuario) return <Navigate to="/" replace />;
  if (usuario.area) return <Navigate to={rutaDe(usuario.area)} replace />;
  return (
    <div className="panel">
      <header className="panel__barra">
        <Marca compacta />
        <button className="boton boton--claro" onClick={salir}>Cerrar sesión</button>
      </header>
      <main className="panel__contenido">
        <h1>Tu cuenta aún no tiene un rol</h1>
        <p className="panel__roles">Comunícate con la cooperativa para que te asignen uno y puedas ingresar.</p>
      </main>
    </div>
  );
}
