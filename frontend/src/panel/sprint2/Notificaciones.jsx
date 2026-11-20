import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { PIActualizar, PIAjustes, PIDoble, PINotificaciones } from "../IconosPanel";
import { Aviso } from "./comunes";
import { useOperacion } from "./operaciones";
import "./notificaciones.css";

/** Categoría de cada evento que hoy envía el backend. */
const CATEGORIA = { PERFIL_ACTUALIZADO: "Mi cuenta", SOCIO_VALIDADO: "Mi cuenta", CLAVE_ACTUALIZADA: "Seguridad", CONTENIDO_PUBLICADO: "Contenidos" };
const FILTROS = ["Todas", "Sin leer", "Mi cuenta", "Seguridad", "Contenidos"];

function cuando(iso) {
  const f = new Date(iso); if (Number.isNaN(f.getTime())) return "";
  const hora = f.toLocaleTimeString("es-EC", { hour: "2-digit", minute: "2-digit" });
  const dia = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
  const dif = Math.round((dia(new Date()) - dia(f)) / 86400000);
  if (dif === 0) return `Hoy, ${hora}`;
  if (dif === 1) return `Ayer, ${hora}`;
  return f.toLocaleDateString("es-EC", { day: "2-digit", month: "short", year: "numeric" });
}

function Interruptor({ etiqueta, texto, ...props }) {
  return <label className="nt-sw"><span>{texto}</span>
    <input type="checkbox" role="switch" aria-label={etiqueta} {...props} /><i aria-hidden="true" /></label>;
}

function Bandeja() {
  const r = useRecurso("/plataforma/notificaciones/"); const p = useRecurso("/plataforma/preferencias/"); const op = useOperacion(r.recargar);
  const [filtro, setFiltro] = useState("Todas");
  const lista = r.datos?.resultados ?? []; const sinLeer = lista.filter((n) => !n.leida_en);
  const visibles = lista.filter((n) => filtro === "Todas" || (filtro === "Sin leer" ? !n.leida_en : CATEGORIA[n.evento] === filtro));
  const avisar = () => window.dispatchEvent(new Event("coop:notificaciones"));
  const eventos = [...new Map((p.datos ?? []).map((x) => [x.evento, x.titulo]))];
  return <div className="nt">
    <div className="nt-cab"><span className="nt-cab__ico"><PINotificaciones /></span>
      <div className="nt-cab__txt"><h1>Mis notificaciones</h1><p>Novedades y avisos de tu cuenta.</p><span className="nt-cuenta">{r.datos?.no_leidas ?? 0} sin leer</span></div>
      <div className="nt-cab__acc">
        <button type="button" className="nt-boton nt-boton--icono" aria-label="Actualizar bandeja" title="Actualizar bandeja" onClick={r.recargar}><PIActualizar /></button>
        <button type="button" className="nt-boton" disabled={op.ocupado || sinLeer.length === 0} onClick={() => op.ejecutar(async () => {
          await Promise.all(sinLeer.map((n) => api.postProtegido(`/plataforma/notificaciones/${n.id}/leida/`, {}))); avisar();
        }, "Todas marcadas como leídas.")}><PIDoble />Marcar todas como leídas</button></div></div>
    <div className="nt-estado"><Aviso error={r.error || p.error || op.error} mensaje={op.mensaje} /></div>
    <div className="nt-cuerpo">
      <div className="nt-principal">
        <div className="nt-filtros" role="tablist" aria-label="Filtrar notificaciones">
          {FILTROS.map((f) => <button key={f} type="button" role="tab" aria-selected={filtro === f} className={filtro === f ? "on" : ""} onClick={() => setFiltro(f)}>{f}</button>)}</div>
        <section className="nt-lista" aria-label="Mi bandeja">
          {visibles.map((n) => <article key={n.id} className={n.leida_en ? "nt-item" : "nt-item nt-item--nueva"}>
            <span className="nt-item__ico" aria-hidden="true"><PINotificaciones /></span>
            <div className="nt-item__txt"><h3>{n.titulo}</h3><p>{n.mensaje}</p>
              <small>{CATEGORIA[n.evento] ?? "General"} · {cuando(n.creada_en)}</small></div>
            {!n.leida_en && <div className="nt-item__lado"><span className="nt-punto" title="Sin leer" aria-hidden="true" />
              <button type="button" className="nt-leer" disabled={op.ocupado} onClick={() => op.ejecutar(async () => {
                await api.postProtegido(`/plataforma/notificaciones/${n.id}/leida/`, {}); avisar();
              }, "Marcada como leída.")}>Marcar como leída</button></div>}
          </article>)}
          {r.datos && visibles.length === 0 && <p className="nt-vacio">{lista.length === 0 ? "No tienes notificaciones entregadas." : "No hay notificaciones en este filtro."}</p>}
          {!r.datos && !r.error && <p className="nt-vacio">Cargando…</p>}
        </section>
      </div>
      <aside className="nt-pref" aria-label="Preferencias">
        <h2><PIAjustes />Preferencias</h2>
        <p className="nt-pref__sub">Elige los eventos y canales que deseas recibir.</p>
        {eventos.map(([evento, titulo]) => <div className="nt-pref__fila" key={evento} role="group" aria-label={titulo}><strong>{titulo}</strong>
          <div>{p.datos.filter((x) => x.evento === evento).map((pref) => {
            const canal = pref.canal === "INTERNA" ? "Plataforma" : "Correo";
            return <Interruptor key={pref.canal} texto={canal} etiqueta={`${titulo} · ${canal}`} checked={pref.habilitada} disabled={op.ocupado}
              onChange={(e) => op.ejecutar(async () => {
                await api.putProtegido("/plataforma/preferencias/", { evento: pref.evento, canal: pref.canal, habilitada: e.target.checked }); p.recargar();
              }, "Preferencia guardada.")} />;
          })}</div></div>)}
      </aside>
    </div>
  </div>;
}
export default function Notificaciones() {
  const { usuario, verificando } = useAuth();
  if (verificando) return <p>Cargando…</p>;
  return usuario ? <Bandeja /> : <Navigate to="/ingresar" replace />;
}
