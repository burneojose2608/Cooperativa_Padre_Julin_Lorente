import { useState } from "react";
import { Link } from "react-router-dom";

/** Logo de la cooperativa.
 *  - Si existe el archivo `public/logo.png`, se usa ese (el logo oficial).
 *  - Si no, se dibuja una marca provisional en SVG (rombo azul y amarillo).
 *  `claro` = texto blanco, para usarlo sobre fondo azul. `enlace` = al hacer clic va al inicio. */
export default function Marca({ claro = false, enlace = true, compacta = false }) {
  const [sinLogo, setSinLogo] = useState(false);

  const contenido = (
    <div className={`marca ${claro ? "marca--clara" : ""} ${compacta ? "marca--compacta" : ""}`}>
      {sinLogo ? (
        <svg viewBox="0 0 56 56" aria-hidden="true" className="marca__icono">
          <rect x="3" y="3" width="50" height="50" rx="12" fill="#ffc72c" />
          <path d="M3 18C3 9 9 3 18 3h20c-12 2-22 10-26 22L3 30Z" fill="#1556bd" />
          <path d="M3 38c12 4 26 4 50-8v11c0 8-5 12-13 12H16C8 53 3 48 3 40Z" fill="#fff" opacity=".92" />
          <path d="M3 41c14 4 30 3 50-9v9c0 8-5 12-13 12H16C8 53 3 49 3 41Z" fill="#ffc72c" />
        </svg>
      ) : (
        <img src="/logo.png" alt="" className="marca__logo" onError={() => setSinLogo(true)} />
      )}
      <div className="marca__texto">
        <strong>Padre Julián Lorente</strong>
        <span>Cooperativa de ahorro y crédito</span>
      </div>
    </div>
  );

  return enlace ? <Link to="/" className="marca__enlace" aria-label="Padre Julián Lorente, ir al inicio">{contenido}</Link> : contenido;
}
