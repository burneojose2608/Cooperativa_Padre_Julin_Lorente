import { Link, Navigate } from "react-router-dom";
import { useState } from "react";
import Marca from "../components/Marca";
import FotoPerfil from "../components/FotoPerfil";
import { useAuth } from "../context/AuthContext";
import { PICandado, PINotificaciones, PISalir, PIUsuarios, PIValidar } from "../panel/IconosPanel";
import { rutaDe } from "../utils/areas";
import "./cuenta-general.css";

/** Acceso básico de una cuenta general; las áreas con rol conservan sus permisos. */
export default function CuentaGeneral() {
  const { usuario, verificando, salir, refrescarPerfil } = useAuth();
  const [consultando, setConsultando] = useState(false);
  const [aviso, setAviso] = useState(null);
  async function comprobarEstado() {
    setConsultando(true);
    setAviso(null);
    try {
      const perfil = await refrescarPerfil();
      if (!perfil.area) setAviso({ texto: "La cooperativa aún no ha confirmado tu condición de socio." });
    } catch (err) {
      setAviso({ texto: err.message, error: true });
    } finally {
      setConsultando(false);
    }
  }
  if (verificando) return <p className="cargando">Cargando…</p>;
  if (!usuario) return <Navigate to="/ingresar" replace />;
  if (usuario.area) return <Navigate to={rutaDe(usuario.area)} replace />;
  return (
    <div className="cg">
      <header className="cg-barra">
        <Marca compacta />
        <button className="boton boton--claro" onClick={salir}><PISalir className="boton__ico" aria-hidden="true" />Cerrar sesión</button>
      </header>
      <main className="cg-contenido">
        <div className="cg-intro">
          <FotoPerfil perfil={usuario} className="cg-avatar" />
          <div><h1>Mi cuenta</h1><p>Hola, {usuario.nombre}</p></div>
        </div>
        <div className="cg-rejilla">
          <section className="cg-tarjeta" aria-labelledby="cg-datos">
            <h2 id="cg-datos"><PIUsuarios aria-hidden="true" />Datos de tu cuenta</h2>
            <dl className="cg-datos">
              <div><dt>Nombre</dt><dd>{usuario.nombre} {usuario.apellido}</dd></div>
              <div><dt>Usuario</dt><dd>{usuario.username}</dd></div>
              {usuario.correo && <div><dt>Correo electrónico</dt><dd>{usuario.correo}</dd></div>}
            </dl>
            <nav className="cg-acciones" aria-label="Opciones de mi cuenta">
              <Link className="boton boton--claro" to="/mi-perfil"><PICandado className="boton__ico" aria-hidden="true" />Perfil y contraseña</Link>
              <Link className="boton boton--claro" to="/mis-notificaciones"><PINotificaciones className="boton__ico" aria-hidden="true" />Notificaciones</Link>
            </nav>
          </section>
          <section className="cg-tarjeta cg-membresia" aria-labelledby="cg-membresia">
            <h2 id="cg-membresia"><PIValidar aria-hidden="true" />Condición de socio</h2>
            <span className="cg-estado">Cuenta general activa</span>
            <p>Cuando la cooperativa confirme tu condición de socio activo, podrás acceder a sus funciones desde esta misma cuenta.</p>
            <button className="boton boton--azul" type="button" disabled={consultando} onClick={comprobarEstado}>
              {consultando ? "Comprobando…" : "Comprobar mi condición de socio"}
            </button>
            {aviso && <p className={aviso.error ? "alerta alerta--error" : "cg-aviso"} role={aviso.error ? "alert" : "status"}>{aviso.texto}</p>}
          </section>
        </div>
      </main>
    </div>
  );
}
