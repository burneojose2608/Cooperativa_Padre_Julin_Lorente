import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import Marca from "../components/Marca";
import { api } from "../api/cliente";
import { Aviso, CampoPanel } from "../panel/sprint2/comunes";
import { useOperacion } from "../panel/sprint2/operaciones";

export default function VerificarCertificado() {
  const { codigo: inicial } = useParams(); const [codigo, setCodigo] = useState(inicial || ""); const [resultado, setResultado] = useState(null); const op = useOperacion();
  return <main className="s2-centrado"><Marca /><h1>Verificar certificado</h1><p>Consulta el código impreso en el certificado de formación.</p>
    <form className="s2-form" onSubmit={(e) => { e.preventDefault(); op.ejecutar(async () => setResultado(await api.get(`/plataforma/certificados/verificar/${encodeURIComponent(codigo.trim())}/`)), "Consulta realizada."); }}>
      <CampoPanel etiqueta="Código de verificación" value={codigo} required maxLength={32} onChange={(e) => setCodigo(e.target.value)} />
      <button className="boton" disabled={op.ocupado}>Verificar</button></form><Aviso {...op} />
    {resultado && <section role="status"><h2>{resultado.valido ? "Certificado válido" : "No se encontró un certificado válido"}</h2>
      {resultado.valido && <><p>{resultado.titulo}</p><p>Emisión: {new Date(resultado.emitido_en).toLocaleDateString("es-EC")}</p></>}</section>}
    <p><Link to="/">Volver al inicio</Link></p>
  </main>;
}
