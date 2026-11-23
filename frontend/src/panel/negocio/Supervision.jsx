import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { TituloPagina } from "../ui";
import { Aviso, CampoPanel } from "../sprint2/comunes";
import { useOperacion } from "../sprint2/operaciones";
import { Tabla } from "./Modulos";

export function Envios() {
  const [estado, setEstado] = useState(""); const [canal, setCanal] = useState("");
  const r = useRecurso(`/plataforma/negocio/envios/?estado=${estado}&canal=${canal}`);
  return <><TituloPagina titulo="Historial de notificaciones" /><Aviso error={r.error} />
    <div className="s2-form"><CampoPanel etiqueta="Estado"><select value={estado} onChange={(e) => setEstado(e.target.value)}><option value="">Todos</option>
      {["PENDIENTE", "PROCESANDO", "ENVIADA", "FALLIDA", "OMITIDA"].map((v) => <option key={v}>{v}</option>)}</select></CampoPanel>
      <CampoPanel etiqueta="Canal"><select value={canal} onChange={(e) => setCanal(e.target.value)}><option value="">Todos</option><option>INTERNA</option><option>CORREO</option></select></CampoPanel></div>
    <Tabla filas={r.datos?.resultados} columnas={["evento", "destinatario", "canal", "estado", "intentos", "enviada_en", "error"]} />
  </>;
}

export function Segmentos() {
  const [socio, setSocio] = useState(""); const [datos, setDatos] = useState({ TIPO_SOCIO: "", PRODUCTO: "", AGENCIA: "" }); const op = useOperacion();
  return <><TituloPagina titulo="Atributos de segmentación" sub="Registra los atributos confirmados del socio para determinar su elegibilidad en campañas." /><Aviso {...op} />
    <form className="s2-form" onSubmit={(e) => { e.preventDefault(); op.ejecutar(() => api.putProtegido(`/plataforma/negocio/segmentos/${socio}/`, Object.fromEntries(Object.entries(datos).filter(([, v]) => v.trim())))); }}>
      <CampoPanel etiqueta="Identificador del socio" type="number" min="1" required value={socio} onChange={(e) => setSocio(e.target.value)} />
      {Object.keys(datos).map((k) => <CampoPanel key={k} etiqueta={k.replaceAll("_", " ")} value={datos[k]} onChange={(e) => setDatos({ ...datos, [k]: e.target.value })} />)}
      <button className="boton" disabled={op.ocupado}>Guardar atributos</button></form>
  </>;
}
