import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { RUTA_DE_AREA } from "../../utils/areas";
import { Tarjeta, TituloPagina } from "../ui";
import useRecurso from "../../hooks/useRecurso";
import { Aviso } from "./comunes";

export default function Inicio({ area }) {
  const { usuario } = useAuth(); const r = useRecurso("/plataforma/notificaciones/"); const base = RUTA_DE_AREA[area];
  return <><TituloPagina titulo={`Bienvenido, ${usuario.nombre}`} sub="Tu espacio en la Cooperativa Padre Julián Lorente." />
    <Aviso error={r.error} /><div className="s2-columnas"><Tarjeta titulo="Mi cuenta"><div className="s2-form">
      <p>{usuario.nombre} {usuario.apellido}</p><p>{usuario.roles?.join(", ")}</p><Link className="boton" to={`${base}/perfil`}>Consultar mi perfil</Link></div></Tarjeta>
      <Tarjeta titulo="Notificaciones"><div className="s2-form"><p>{r.datos?.no_leidas ?? 0} notificaciones sin leer</p><Link className="boton boton--claro" to={`${base}/notificaciones`}>Ver mi bandeja</Link></div></Tarjeta>
      {area === "socio" && <Tarjeta titulo="Invita a nuestra comunidad"><div className="s2-form"><p>Obtén tu código personal y comparte tu enlace.</p><Link className="boton" to={`${base}/referidos`}>Mi código de referido</Link></div></Tarjeta>}
    </div></>;
}
