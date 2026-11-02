import Marca from "./Marca";

/** Estructura común de las pantallas de recuperación: logo, título y una sola tarjeta centrada. */
export default function MarcoRecuperacion({ titulo, subtitulo, children }) {
  return (
    <main className="auth">
      <header className="auth__cabecera"><Marca /></header>
      <div style={{ maxWidth: 440, margin: "0 auto" }}>
        <section className="tarjeta tarjeta--activa" aria-label={titulo}>
          <div className="tarjeta__form">
            <h2>{titulo}</h2>
            {subtitulo && <p className="tarjeta__sub">{subtitulo}</p>}
            {children}
          </div>
        </section>
      </div>
    </main>
  );
}
