import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";
import Campo from "./Campo";
import { IcoCandado, IcoFlecha, IcoPersona } from "./Iconos";

export default function FormLogin({ aviso }) {
  const { entrar } = useAuth();
  const navegar = useNavigate();
  const [identificador, setIdentificador] = useState("");
  const [clave, setClave] = useState("");
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [cargando, setCargando] = useState(false);

  async function enviar(e) {
    e.preventDefault();
    if (cargando) return;
    const nuevos = {};
    if (!identificador.trim()) nuevos.identificador = "Ingresa tu correo, cédula o usuario.";
    if (!clave) nuevos.clave = "Ingresa tu contraseña.";
    setErrores(nuevos);
    setErrorGeneral("");
    if (Object.keys(nuevos).length) return;

    setCargando(true);
    try {
      const u = await entrar(identificador.trim(), clave);
      navegar(rutaDe(u.area), { replace: true });  // cada rol llega a su propia pantalla
    } catch (err) {
      setErrorGeneral(err.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <form onSubmit={enviar} noValidate className="tarjeta__form">
      <h1 className="acceso__titulo">¡Bienvenido de nuevo!</h1>
      <p className="tarjeta__sub">Ingresa tus credenciales para continuar.</p>
      <p>Por seguridad, cinco intentos fallidos bloquean el acceso durante 15 minutos.</p>

      {aviso && <div className="alerta alerta--ok" role="status">{aviso}</div>}
      {errorGeneral && <div className="alerta alerta--error" role="alert">{errorGeneral}</div>}

      <Campo etiqueta="Correo, cédula o usuario" required icono={IcoPersona} autoComplete="username" value={identificador}
             onChange={(e) => setIdentificador(e.target.value)} error={errores.identificador} />
      <Campo etiqueta="Contraseña" required tipo="password" icono={IcoCandado} autoComplete="current-password" value={clave}
             onChange={(e) => setClave(e.target.value)} error={errores.clave} />

      <Link className="enlace enlace--derecha" to="/recuperar">¿Olvidaste tu contraseña?</Link>
      <button className="boton boton--azul" disabled={cargando}>
        {cargando ? "Ingresando…" : <>Iniciar sesión <IcoFlecha className="boton__flecha" /></>}
      </button>

      <p className="tarjeta__pie">
        ¿Aún no tienes una cuenta?<br />
        <Link className="enlace" to="/registro">Crear cuenta</Link>
      </p>
    </form>
  );
}
