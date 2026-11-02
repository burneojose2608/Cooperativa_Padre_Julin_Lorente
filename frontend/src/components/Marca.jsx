/** Marca provisional. Para usar el logo oficial, coloca el archivo en src/assets
 *  y reemplaza el <svg> por <img src={logo} alt="..."/>. */
export default function Marca({ compacta = false }) {
  return (
    <div className="marca">
      <svg viewBox="0 0 48 48" aria-hidden="true" className="marca__icono">
        <circle cx="24" cy="24" r="22" fill="#5b3fa8" />
        <path d="M14 30c4-12 14-16 22-14-3 12-12 18-22 14z" fill="#3fb37f" />
      </svg>
      <div className="marca__texto">
        <span>Cooperativa de Ahorro y Crédito</span>
        <strong>Padre Julián Lorente</strong>
        {!compacta && null}
      </div>
    </div>
  );
}
