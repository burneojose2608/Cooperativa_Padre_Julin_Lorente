import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Marca from "../components/Marca";
import { api } from "../api/cliente";
import { useAuth } from "../context/AuthContext";
import { Aviso } from "../panel/sprint2/comunes";
import { PICorreo, PIUsuarios } from "../panel/IconosPanel";
import { FormReferido } from "../panel/negocio/Modulos";
import { rutaDe } from "../utils/areas";
import "./invitacion.css";

export default function Invitacion() {
  const { codigo } = useParams();
  const { usuario, verificando } = useAuth();
  const [resultado, setResultado] = useState(null);
  useEffect(() => {
    let vigente = true;
    api.get(`/plataforma/invitaciones/${encodeURIComponent(codigo)}/`)
      .then((datos) => { if (vigente) setResultado({ codigo, datos }); })
      .catch((e) => { if (vigente) setResultado({ codigo, error: e.message }); });
    return () => { vigente = false; };
  }, [codigo]);
  const { datos, error } = resultado?.codigo === codigo ? resultado : {};
  return <div className="inv-pagina">
    <header className="inv-marca"><Marca compacta /><Link to="/">Conocer la plataforma</Link></header>
    <main className="inv-contenido">
      <div className="inv-intro">
        <h1>Tu invitación a la cooperativa</h1>
        <p>Cuéntanos qué producto te interesa y confirma que podemos contactarte.</p>
        {datos && <p className="inv-codigo">Código de invitación <strong>{datos.codigo}</strong></p>}
      </div>
      <Aviso error={error} />
      {!datos && !error && <p role="status">Cargando invitación…</p>}
      {datos && <div className="inv-rejilla">
        <section className="inv-tarjeta" aria-labelledby="inv-solicitud">
          <div className="inv-tarjeta__cab"><PICorreo aria-hidden="true" />
            <div><h2 id="inv-solicitud">Solicitar información</h2>
              <p>La solicitud se vincula al socio que te invitó. Puedes enviarla sin crear una cuenta.</p></div>
          </div>
          <FormReferido key={codigo} codigo={codigo} publico />
        </section>
        <aside className="inv-tarjeta inv-cuenta" aria-labelledby="inv-cuenta">
          <PIUsuarios aria-hidden="true" />
          <h2 id="inv-cuenta">{usuario ? "Tu cuenta" : "Cuenta en la plataforma"}</h2>
          <p>{usuario ? "Ya tienes una sesión abierta en este navegador." : "El registro te permite iniciar sesión. Si también quieres que te contacten, envía la solicitud de información."}</p>
          {!verificando && <Link className="boton boton--claro" to={usuario ? rutaDe(usuario.area) : "/registro"}>
            {usuario ? "Ir a mi panel" : "Crear mi cuenta"}
          </Link>}
        </aside>
      </div>}
    </main>
  </div>;
}
