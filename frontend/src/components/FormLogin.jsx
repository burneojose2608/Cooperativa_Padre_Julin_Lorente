import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";
import Campo from "./Campo";

export default function FormLogin({ alIrARegistro, aviso }) {
  const { entrar } = useAuth();
  const navegar = useNavigate();
  const [identificador, setIdentificador] = useState("");
  const [clave, setClave] = useState("");
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [cargando, setCargando] = useState(false);

  async function enviar(e) {
    e.preventDefault();
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
      <h2>Bienvenido</h2>
      <p className="tarjeta__sub">Ingresa a tu cuenta</p>

      {aviso && <div className="alerta alerta--ok" role="status">{aviso}</div>}
      {errorGeneral && <div className="alerta alerta--error" role="alert">{errorGeneral}</div>}

      <Campo etiqueta="Correo, cédula o usuario" autoComplete="username" value={identificador}
             onChange={(e) => setIdentificador(e.target.value)} error={errores.identificador} />
      <Campo etiqueta="Contraseña" tipo="password" autoComplete="current-password" value={clave}
             onChange={(e) => setClave(e.target.value)} error={errores.clave} />

      <button className="boton" disabled={cargando}>{cargando ? "Ingresando…" : "Iniciar sesión"}</button>
      <Link className="enlace" style={{ alignSelf: "center" }} to="/recuperar">¿Olvidaste tu contraseña?</Link>

      <p className="tarjeta__pie">
        ¿Aún no tienes una cuenta?{" "}
        <button type="button" className="enlace" onClick={alIrARegistro}>Regístrate</button>
      </p>
    </form>
  );
}
