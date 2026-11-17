export const Aviso = ({ error, mensaje }) => error
  ? <p className="alerta alerta--error" role="alert">{error}</p>
  : mensaje ? <p className="alerta alerta--ok" role="status">{mensaje}</p> : null;
export function CampoPanel({ etiqueta, children, ...props }) {
  return <label className="s2-campo"><span>{etiqueta}</span>{children || <input {...props} />}</label>;
}
