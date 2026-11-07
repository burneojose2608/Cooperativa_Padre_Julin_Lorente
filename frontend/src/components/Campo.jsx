import { useId, useState } from "react";
import { IcoOjo, IcoOjoCerrado } from "./Iconos";

/** Campo de formulario accesible: etiqueta, icono opcional, ayuda, error y ojo para contraseñas. */
export default function Campo({ etiqueta, error, ayuda, tipo = "text", icono: Icono, ...props }) {
  const id = useId();
  const [visible, setVisible] = useState(false);
  const esClave = tipo === "password";
  return (
    <div className={`campo ${error ? "campo--error" : ""}`}>
      <label htmlFor={id}>{etiqueta}</label>
      <div className={`campo__control ${Icono ? "campo__control--icono" : ""}`}>
        {Icono && <Icono className="campo__icono" />}
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
            {visible ? <IcoOjoCerrado /> : <IcoOjo />}
          </button>
        )}
      </div>
      {error ? <small id={`${id}-e`} role="alert" className="campo__error">{error}</small>
             : ayuda ? <small id={`${id}-a`} className="campo__ayuda">{ayuda}</small> : null}
    </div>
  );
}
