import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { Aviso } from "./comunes";

export default function Auditoria() {
  const r = useRecurso("/auth/administracion/auditoria/");
  return <><TituloPagina titulo="Auditoría" sub="Últimas 100 acciones registradas. La base conserva esta bitácora sin permitir modificaciones."><button className="boton boton--claro" onClick={r.recargar}>Actualizar</button></TituloPagina>
    <Aviso error={r.error} /><Tarjeta><div className="s2-tabla"><table><thead><tr><th>Fecha</th><th>Responsable</th><th>Acción</th><th>Registro</th><th>Resultado</th><th>Detalle</th></tr></thead>
      <tbody>{r.datos?.map((e) => <tr key={e.id_auditoria}><td>{new Date(e.fecha).toLocaleString("es-EC")}</td><td>{e.usuario_id || "Anónimo"}</td><td>{e.accion}</td><td>{e.entidad} #{e.registro_id}</td><td>{e.resultado}</td><td className="s2-texto">{JSON.stringify(e.detalle)}</td></tr>)}</tbody></table></div></Tarjeta></>;
}
