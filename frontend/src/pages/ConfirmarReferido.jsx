import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/cliente";
import Marca from "../components/Marca";
import { Aviso } from "../panel/sprint2/comunes";
import { useOperacion } from "../panel/sprint2/operaciones";

export default function ConfirmarReferido() {
  const { token } = useParams(); const op = useOperacion(); const [listo, setListo] = useState(false);
  return <main className="s2-centrado"><Marca /><h1>Confirmación de contacto</h1>
    <p>Confirma que autorizas a la cooperativa a contactarte por la referencia registrada, según la política de tratamiento de datos versión 1.0.</p>
    <Aviso {...op} />{!listo && <button className="boton" disabled={op.ocupado} onClick={async () => {
      if (await op.ejecutar(() => api.post(`/plataforma/referidos/confirmar/${encodeURIComponent(token)}/`, {}), "Consentimiento confirmado.")) setListo(true);
    }}>Confirmar mi consentimiento</button>}<p><Link to="/">Volver al inicio</Link></p>
  </main>;
}
