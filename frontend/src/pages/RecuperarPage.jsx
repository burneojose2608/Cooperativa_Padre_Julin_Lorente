import { useState } from "react";
import { Link } from "react-router-dom";
import { solicitarRecuperacion } from "../api/auth";
import Campo from "../components/Campo";
import MarcoRecuperacion from "../components/MarcoRecuperacion";

export default function RecuperarPage() {
  const [identificador, setIdentificador] = useState("");
  const [error, setError] = useState("");
  const [enviado, setEnviado] = useState("");
  const [cargando, setCargando] = useState(false);

  async function enviar(e) {
    e.preventDefault();
    setError("");
    if (!identificador.trim()) return setError("Ingresa tu correo, cédula o usuario.");
    setCargando(true);
    try {
      const r = await solicitarRecuperacion(identificador.trim());
      setEnviado(r.mensaje);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }

  if (enviado) {
    return (
      <MarcoRecuperacion titulo="Revisa tu correo">
        <div className="alerta alerta--ok" role="status">{enviado}</div>
        <p className="tarjeta__pie">El enlace vence en 30 minutos.</p>
        <Link className="boton boton--claro" style={{ textAlign: "center", textDecoration: "none", display: "grid", placeItems: "center" }} to="/ingresar">
          Volver a iniciar sesión
        </Link>
      </MarcoRecuperacion>
    );
  }

  return (
    <MarcoRecuperacion titulo="¿Olvidaste tu contraseña?"
                       subtitulo="Escribe tu correo, cédula o usuario y te enviaremos un enlace para crear una nueva.">
      <form onSubmit={enviar} noValidate className="tarjeta__form">
        {error && <div className="alerta alerta--error" role="alert">{error}</div>}
        <Campo etiqueta="Correo, cédula o usuario" autoComplete="username" value={identificador}
               onChange={(e) => setIdentificador(e.target.value)} />
        <button className="boton" disabled={cargando}>{cargando ? "Enviando…" : "Enviar enlace"}</button>
        <p className="tarjeta__pie"><Link className="enlace" to="/ingresar">Volver a iniciar sesión</Link></p>
      </form>
    </MarcoRecuperacion>
  );
}
