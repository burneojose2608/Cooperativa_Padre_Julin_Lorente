import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Marca from "../components/Marca";
import { api } from "../api/cliente";
import { Aviso } from "../panel/sprint2/comunes";

export default function Invitacion() {
  const { codigo } = useParams(); const [datos, setDatos] = useState(null); const [error, setError] = useState("");
  useEffect(() => {
    let vigente = true;
    api.get(`/plataforma/invitaciones/${encodeURIComponent(codigo)}/`).then((r) => { if (vigente) setDatos(r); })
      .catch((e) => { if (vigente) setError(e.message); });
    return () => { vigente = false; };
  }, [codigo]);
  return <main className="s2-centrado"><Marca /><h1>Te damos la bienvenida</h1><Aviso error={error} />
    {datos && <><p>{datos.mensaje}</p><p>Código de invitación: <strong>{datos.codigo}</strong></p>
      <p>Puedes crear una cuenta general. La cooperativa validará tu condición de socio cuando corresponda.</p>
      <Link className="boton" to="/registro">Crear mi cuenta</Link></>}
    {!datos && !error && <p>Cargando invitación…</p>}<p><Link to="/">Conocer la plataforma</Link></p>
  </main>;
}
