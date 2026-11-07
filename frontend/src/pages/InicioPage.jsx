import { useState } from "react";
import { Link, Navigate } from "react-router-dom";
import Marca from "../components/Marca";
import {
  IcoApreton, IcoCopa, IcoFlecha, IcoGorro, IcoGrupo, IcoMedalla, IcoPersona, IcoRegalo, IcoTelefonoGrande,
} from "../components/Iconos";
import { useAuth } from "../context/AuthContext";
import { rutaDe } from "../utils/areas";

const BENEFICIOS = [
  { icono: IcoApreton, titulo: "Refiere", texto: "y suma puntos" },
  { icono: IcoGorro, titulo: "Capacítate", texto: "y aprende" },
  { icono: IcoCopa, titulo: "Participa en", texto: "campañas y sorteos" },
  { icono: IcoRegalo, titulo: "Canjea", texto: "beneficios" },
];

const PASOS = [
  ["1", "Crea tu cuenta", "Regístrate con tu cédula y tus datos para ser parte de la comunidad."],
  ["2", "Invita a tus amigos", "Comparte tu código de referido con quienes quieras que se unan."],
  ["3", "Acumula puntos", "Suma puntos cuando tus referidos se concretan y cuando completas capacitaciones."],
  ["4", "Canjea beneficios", "Usa tus puntos para obtener beneficios y participar en sorteos."],
];

const REQUISITOS = [
  "Tener una cédula de identidad ecuatoriana válida.",
  "Contar con un correo electrónico y un número de teléfono.",
  "Aceptar los Términos y Condiciones y el tratamiento de tus datos personales.",
];

/** Ilustración del héroe. Si existe `public/hero.png` (foto del programa) se muestra esa. */
function Ilustracion() {
  const [sinFoto, setSinFoto] = useState(false);
  return (
    <div className="hero__arte" aria-hidden="true">
      <div className="hero__circulo" />
      {!sinFoto && <img className="hero__foto" src="/hero.png" alt="" onError={() => setSinFoto(true)} />}
      {sinFoto && <IcoTelefonoGrande className="hero__telefono" />}
      <span className="hero__chip hero__chip--a"><IcoRegalo /></span>
      <span className="hero__chip hero__chip--b"><IcoMedalla /></span>
      <span className="hero__chip hero__chip--c"><IcoGrupo /></span>
    </div>
  );
}

export default function InicioPage() {
  const { usuario, verificando } = useAuth();
  if (!verificando && usuario) return <Navigate to={rutaDe(usuario.area)} replace />;

  return (
    <div className="inicio">
      <header className="inicio__barra">
        <Marca claro />
        <nav className="inicio__menu" aria-label="Secciones">
          <a href="#asi-funciona">Así funciona</a>
          <a href="#beneficios">Beneficios</a>
          <a href="#requisitos">Requisitos</a>
        </nav>
        <div className="inicio__acciones">
          <Link className="boton boton--borde-claro" to="/ingresar"><IcoPersona className="boton__ico" /> Iniciar sesión</Link>
          <Link className="boton boton--amarillo" to="/registro"><IcoPersona className="boton__ico" /> Crear cuenta</Link>
        </div>
      </header>

      <section className="hero">
        <div className="hero__texto">
          <h1>
            <span className="hero__ligero">Programa de</span>
            <span className="hero__fuerte">Referidos y Gamificación</span>
          </h1>
          <svg className="hero__subrayado" viewBox="0 0 120 12" aria-hidden="true"><path d="M2 8c30-6 70-7 116-3" stroke="#ffc72c" strokeWidth="4" strokeLinecap="round" fill="none" /></svg>
          <p>Invita a tus amigos, participa en capacitaciones, acumula puntos y canjea beneficios exclusivos.</p>
          <div className="hero__botones">
            <Link className="boton boton--amarillo boton--grande" to="/registro">Crear mi cuenta <IcoFlecha className="boton__flecha" /></Link>
            <Link className="boton boton--borde boton--grande" to="/ingresar"><IcoPersona className="boton__ico" /> Iniciar sesión</Link>
          </div>
        </div>
        <Ilustracion />
      </section>

      <section className="inicio__cinta" aria-label="Qué puedes hacer">
        <ul>
          {BENEFICIOS.map(({ icono: Ico, titulo, texto }) => (
            <li key={titulo}><Ico className="cinta__icono" /><span>{titulo}<br />{texto}</span></li>
          ))}
        </ul>
      </section>

      <section className="seccion" id="asi-funciona">
        <h2>Así funciona</h2>
        <ol className="pasos">
          {PASOS.map(([n, t, d]) => (
            <li key={n}><span className="pasos__n">{n}</span><strong>{t}</strong><p>{d}</p></li>
          ))}
        </ol>
      </section>

      <section className="seccion seccion--gris" id="beneficios">
        <h2>Beneficios</h2>
        <div className="beneficios">
          {BENEFICIOS.map(({ icono: Ico, titulo, texto }) => (
            <div key={titulo} className="beneficio"><Ico className="beneficio__ico" /><strong>{titulo} {texto}</strong></div>
          ))}
        </div>
      </section>

      <section className="seccion" id="requisitos">
        <h2>Requisitos</h2>
        <ul className="requisitos">
          {REQUISITOS.map((r) => <li key={r}>{r}</li>)}
        </ul>
        <div className="seccion__cta">
          <Link className="boton boton--amarillo boton--grande" to="/registro">Crear mi cuenta <IcoFlecha className="boton__flecha" /></Link>
        </div>
      </section>

      <footer className="inicio__pie">© Cooperativa de Ahorro y Crédito Padre Julián Lorente</footer>
    </div>
  );
}
