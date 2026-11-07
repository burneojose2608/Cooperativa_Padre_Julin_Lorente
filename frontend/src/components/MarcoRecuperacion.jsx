import AuthLayout from "./AuthLayout";

/** Estructura común de las pantallas de recuperación: misma imagen lateral y una sola tarjeta. */
export default function MarcoRecuperacion({ titulo, subtitulo, children }) {
  return (
    <AuthLayout etiqueta={titulo}>
      <div className="tarjeta__form">
        <h1 className="acceso__titulo">{titulo}</h1>
        {subtitulo && <p className="tarjeta__sub">{subtitulo}</p>}
        {children}
      </div>
    </AuthLayout>
  );
}
