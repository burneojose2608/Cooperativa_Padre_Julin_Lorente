import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { restablecerClave } from "../api/auth";
import Campo from "../components/Campo";
import MarcoRecuperacion from "../components/MarcoRecuperacion";
import { claveValida } from "../utils/validaciones";

export default function RestablecerPage() {
  const [params] = useSearchParams();
  const token = params.get("token") || "";
  const [clave, setClave] = useState("");
  const [repetir, setRepetir] = useState("");
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [listo, setListo] = useState(false);
  const [cargando, setCargando] = useState(false);

  const irAlLogin = (
    <Link className="boton" style={{ textAlign: "center", textDecoration: "none", display: "grid", placeItems: "center" }} to="/">
      Ir a iniciar sesión
    </Link>
  );

  if (!token) {
    return (
      <MarcoRecuperacion titulo="Enlace no válido">
        <div className="alerta alerta--error" role="alert">Este enlace está incompleto. Pide uno nuevo.</div>
        <Link className="enlace" style={{ textAlign: "center" }} to="/recuperar">Solicitar un enlace nuevo</Link>
      </MarcoRecuperacion>
    );
  }

  if (listo) {
    return (
      <MarcoRecuperacion titulo="¡Contraseña actualizada!">
        <div className="alerta alerta--ok" role="status">Ya puedes iniciar sesión con tu nueva contraseña.</div>
        {irAlLogin}
      </MarcoRecuperacion>
    );
  }

  async function enviar(e) {
    e.preventDefault();
    setErrorGeneral("");
    const nuevos = {};
    if (!claveValida(clave)) nuevos.clave = "Mínimo 8 caracteres, con letras y números.";
    if (repetir !== clave) nuevos.repetir = "Las contraseñas no coinciden.";
    setErrores(nuevos);
    if (Object.keys(nuevos).length) return;

    setCargando(true);
    try {
      await restablecerClave(token, clave);
      setListo(true);
    } catch (err) {
      setErrores(err.campos?.clave ? { clave: err.campos.clave } : {});
      setErrorGeneral(err.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <MarcoRecuperacion titulo="Crea una nueva contraseña" subtitulo="Elige una contraseña que no hayas usado antes.">
      <form onSubmit={enviar} noValidate className="tarjeta__form">
        {errorGeneral && (
          <div className="alerta alerta--error" role="alert">
            {errorGeneral}{" "}
            {errorGeneral.includes("enlace") && <Link className="enlace" to="/recuperar">Pedir uno nuevo</Link>}
          </div>
        )}
        <Campo etiqueta="Nueva contraseña" tipo="password" autoComplete="new-password" value={clave}
               onChange={(e) => setClave(e.target.value)} error={errores.clave}
               ayuda="Mínimo 8 caracteres, con letras y números." />
        <Campo etiqueta="Repite la contraseña" tipo="password" autoComplete="new-password" value={repetir}
               onChange={(e) => setRepetir(e.target.value)} error={errores.repetir} />
        <button className="boton" disabled={cargando}>{cargando ? "Guardando…" : "Guardar contraseña"}</button>
      </form>
    </MarcoRecuperacion>
  );
}
