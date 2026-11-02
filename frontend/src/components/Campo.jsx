import { useId, useState } from "react";

/** Campo de formulario accesible: etiqueta, ayuda, error y (opcional) ojo para contraseñas. */
export default function Campo({ etiqueta, error, ayuda, tipo = "text", ...props }) {
  const id = useId();
  const [visible, setVisible] = useState(false);
  const esClave = tipo === "password";
  return (
    <div className={`campo ${error ? "campo--error" : ""}`}>
      <label htmlFor={id}>{etiqueta}</label>
      <div className="campo__control">
        <input
          id={id}
          type={esClave && visible ? "text" : tipo}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? `${id}-e` : ayuda ? `${id}-a` : undefined}
          {...props}
        />
        {esClave && (
          <button type="button" className="campo__ojo" onClick={() => setVisible((v) => !v)}
                  aria-label={visible ? "Ocultar contraseña" : "Mostrar contraseña"}>
            {visible ? "Ocultar" : "Ver"}
          </button>
        )}
      </div>
      {error ? <small id={`${id}-e`} role="alert" className="campo__error">{error}</small>
             : ayuda ? <small id={`${id}-a`} className="campo__ayuda">{ayuda}</small> : null}
    </div>
  );
}
