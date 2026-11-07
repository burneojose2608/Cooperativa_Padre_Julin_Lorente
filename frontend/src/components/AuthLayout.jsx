import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Marca from "./Marca";

/** Pantalla dividida: a la izquierda la imagen de la cooperativa, a la derecha la tarjeta con el formulario.
 *  En celular la imagen pasa a ser una franja arriba.
 *  Para usar la foto real del edificio, guarda el archivo como `public/edificio.jpg`. */
export default function AuthLayout({ children, etiqueta }) {
  // Si existe public/edificio.jpg se usa como foto (ya trae el rótulo); si no, se muestra el logo sobre el azul.
  const [hayFoto, setHayFoto] = useState(false);
  useEffect(() => { const i = new Image(); i.onload = () => setHayFoto(true); i.src = "/edificio.jpg"; }, []);

  return (
    <main className="acceso">
      <aside className="acceso__imagen" aria-hidden="true">
        {!hayFoto && <div className="acceso__rotulo"><Marca claro enlace={false} /></div>}
        <svg className="acceso__ola" viewBox="0 0 400 200" preserveAspectRatio="none">
          <path d="M0 200V90c60 40 130 50 210 10s130-40 190-10v110Z" fill="#ffc72c" />
          <path d="M0 200v-60c70 30 150 30 230-10s120-30 170-6v76Z" fill="#1556bd" opacity=".9" />
        </svg>
      </aside>
      <section className="acceso__tarjeta" aria-label={etiqueta}>
        <div className="acceso__logo"><Marca /></div>
        {children}
        <p className="acceso__volver"><Link className="enlace enlace--suave" to="/">← Volver al inicio</Link></p>
      </section>
    </main>
  );
}
