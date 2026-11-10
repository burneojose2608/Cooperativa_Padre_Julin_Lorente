import AccesosPorRol from "../components/AccesosPorRol";
import Marca from "../components/Marca";
import { useAuth } from "../context/AuthContext";
import { AREAS } from "../utils/areas";

export default function PanelArea({ area }) {
  const { usuario, salir } = useAuth();
  const datos = AREAS[area];

  return (
    <div className="panel">
      <header className="panel__barra">
        <Marca compacta />
        <button className="boton boton--claro" onClick={salir}>Cerrar sesión</button>
      </header>
      <main className="panel__contenido">
        <h1>Hola, {usuario.nombre} 👋</h1>
        <p className="panel__roles">
          Tu rol: {(usuario.roles || []).map((r) => <span key={r} className="etiqueta">{r}</span>)}
        </p>
        <h2>{datos.nombre}</h2>
        <p className="panel__roles">{datos.subtitulo}</p>
        <AccesosPorRol usuario={usuario} areaActual={area} />
        <section className="rejilla" aria-label={`Opciones de ${datos.nombre}`}>
          {datos.opciones.map((o) => (
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
