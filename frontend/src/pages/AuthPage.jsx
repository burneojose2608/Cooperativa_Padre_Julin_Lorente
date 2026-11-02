import { useState } from "react";
import { Navigate } from "react-router-dom";
import FormLogin from "../components/FormLogin";
import FormRegistro from "../components/FormRegistro";
import Marca from "../components/Marca";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";

/** Computador: dos tarjetas lado a lado. Celular: una sola con pestañas. */
export default function AuthPage() {
  const { usuario, verificando } = useAuth();
  const [vista, setVista] = useState("login");
  const [aviso, setAviso] = useState("");

  if (!verificando && usuario) return <Navigate to={rutaDe(usuario.area)} replace />;

  const irALogin = (correo) => {
    setAviso(correo ? `¡Cuenta creada! Ya puedes iniciar sesión con ${correo}.` : "");
    setVista("login");
  };

  return (
    <main className="auth">
      <header className="auth__cabecera">
        <Marca />
        <h1>Plataforma de Referidos y Gamificación</h1>
      </header>

      <div className="pestanas" role="tablist" aria-label="Acceso">
        <button role="tab" aria-selected={vista === "login"} onClick={() => setVista("login")}>Iniciar sesión</button>
        <button role="tab" aria-selected={vista === "registro"} onClick={() => setVista("registro")}>Crear cuenta</button>
      </div>

      <div className="auth__tarjetas">
        <section className={`tarjeta ${vista === "login" ? "tarjeta--activa" : ""}`} aria-label="Iniciar sesión">
          <FormLogin aviso={aviso} alIrARegistro={() => { setAviso(""); setVista("registro"); }} />
        </section>
        <section className={`tarjeta ${vista === "registro" ? "tarjeta--activa" : ""}`} aria-label="Crear cuenta">
          <FormRegistro alRegistrar={irALogin} />
        </section>
      </div>
    </main>
  );
}
