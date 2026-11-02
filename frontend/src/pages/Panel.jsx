import { Navigate } from "react-router-dom";
import Marca from "../components/Marca";
import { useAuth } from "../context/AuthContext";

// Qué ve cada rol. Las opciones se irán activando a medida que se construyan los módulos.
const MENU = {
  "Socio": ["Mi código de referido", "Mis referidos", "Mis puntos", "Capacitaciones", "Sorteos", "Canjes"],
  "Administrador": ["Usuarios y roles", "Auditoría", "Configuración de puntos"],
  "Responsable de Marketing": ["Campañas", "Segmentos", "Sorteos", "Reportes"],
  "Responsable de Responsabilidad Social": ["Convenios", "Bienestar", "Reportes"],
  "Gestor de contenidos": ["Contenidos", "Capacitaciones", "Talleres"],
};

export default function Panel() {
  const { usuario, verificando, salir } = useAuth();
  if (verificando) return <p className="cargando">Cargando…</p>;
  if (!usuario) return <Navigate to="/" replace />;

  const roles = usuario.roles || [];
  const opciones = [...new Set(roles.flatMap((r) => MENU[r] || []))];

  return (
    <div className="panel">
      <header className="panel__barra">
        <Marca compacta />
        <button className="boton boton--claro" onClick={salir}>Cerrar sesión</button>
      </header>
      <main className="panel__contenido">
        <h1>Hola, {usuario.nombre} 👋</h1>
        <p className="panel__roles">
          Tu rol: {roles.map((r) => <span key={r} className="etiqueta">{r}</span>)}
        </p>
        <section className="rejilla" aria-label="Opciones disponibles para tu rol">
          {opciones.map((o) => (
            <div key={o} className="opcion" aria-disabled="true">
              <strong>{o}</strong>
              <span>Próximamente</span>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
