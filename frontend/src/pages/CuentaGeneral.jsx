import { Navigate } from "react-router-dom";
import { useState } from "react";
import Marca from "../components/Marca";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";

/** Acceso básico de una cuenta general; las áreas con rol conservan sus permisos. */
export default function CuentaGeneral() {
  const { usuario, verificando, salir, refrescarPerfil } = useAuth();
  const [consultando, setConsultando] = useState(false);
  const [mensaje, setMensaje] = useState("");
  async function comprobarEstado() {
    setConsultando(true);
    setMensaje("");
    try {
      const perfil = await refrescarPerfil();
      if (!perfil.area) setMensaje("Tu cuenta continúa como usuario general. La validación debe realizarla un administrador.");
    } catch (err) {
      setMensaje(err.message);
    } finally {
      setConsultando(false);
    }
  }
  if (verificando) return <p className="cargando">Cargando…</p>;
  if (!usuario) return <Navigate to="/ingresar" replace />;
  if (usuario.area) return <Navigate to={rutaDe(usuario.area)} replace />;
  return (
    <div className="panel">
      <header className="panel__barra">
        <Marca compacta />
        <button className="boton boton--claro" onClick={salir}>Cerrar sesión</button>
      </header>
      <main className="panel__contenido">
        <h1>Mi cuenta</h1>
        <p className="panel__roles">Bienvenido, {usuario.nombre}. Has ingresado como usuario general.</p>
        <dl>
          <dt>Nombre</dt><dd>{usuario.nombre} {usuario.apellido}</dd>
          <dt>Usuario</dt><dd>{usuario.username}</dd>
          {usuario.correo && <><dt>Correo electrónico</dt><dd>{usuario.correo}</dd></>}
          <dt>Tipo de cuenta</dt><dd>Usuario general</dd>
        </dl>
        <p>Tu cuenta general está activa. Las funciones de socio requieren que la cooperativa confirme tu condición de socio activo.</p>
        <button className="boton boton--azul" disabled={consultando} onClick={comprobarEstado}>
          {consultando ? "Comprobando…" : "Comprobar mi condición de socio"}
        </button>
        {mensaje && <p role="status">{mensaje}</p>}
      </main>
    </div>
  );
}
