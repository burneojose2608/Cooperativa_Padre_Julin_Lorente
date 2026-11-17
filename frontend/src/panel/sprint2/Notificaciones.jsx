import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { Aviso } from "./comunes";
import { useOperacion } from "./operaciones";

function Bandeja() {
  const r = useRecurso("/plataforma/notificaciones/"); const p = useRecurso("/plataforma/preferencias/"); const op = useOperacion(r.recargar);
  return <><TituloPagina titulo="Notificaciones" sub={`${r.datos?.no_leidas ?? 0} sin leer`}><button className="boton boton--claro" onClick={r.recargar}>Actualizar bandeja</button></TituloPagina>
    <Aviso error={r.error || p.error || op.error} mensaje={op.mensaje} />
    <div className="s2-columnas"><Tarjeta titulo="Mi bandeja"><div className="s2-lista">
      {r.datos?.resultados.map((n) => <article key={n.id} className={!n.leida_en ? "s2-lectura" : ""}>
        <h3>{n.titulo}</h3><p className="s2-texto">{n.mensaje}</p><small>{new Date(n.creada_en).toLocaleString("es-EC")}</small>
        {!n.leida_en && <div className="s2-acciones"><button className="boton boton--claro" disabled={op.ocupado} onClick={() => op.ejecutar(async () => {
          await api.postProtegido(`/plataforma/notificaciones/${n.id}/leida/`, {});
          window.dispatchEvent(new Event("coop:notificaciones"));
        }, "Marcada como leída.")}>Marcar como leída</button></div>}
      </article>)}{r.datos?.resultados.length === 0 && <p className="vacio">No tienes notificaciones entregadas.</p>}
    </div></Tarjeta><Tarjeta titulo="Preferencias"><div className="s2-form"><p>Elige los eventos y canales que deseas recibir.</p>
      {p.datos?.map((pref) => <label className="s2-check" key={pref.evento + pref.canal}>
        <input type="checkbox" checked={pref.habilitada} disabled={op.ocupado} onChange={(e) => op.ejecutar(async () => {
          await api.putProtegido("/plataforma/preferencias/", { evento: pref.evento, canal: pref.canal, habilitada: e.target.checked }); p.recargar();
        }, "Preferencia guardada.")} />{pref.titulo} · {pref.canal === "INTERNA" ? "Plataforma" : "Correo"}
      </label>)}
    </div></Tarjeta></div></>;
}
export default function Notificaciones() {
  const { usuario, verificando } = useAuth();
  if (verificando) return <p>Cargando…</p>;
  return usuario ? <Bandeja /> : <Navigate to="/ingresar" replace />;
}
