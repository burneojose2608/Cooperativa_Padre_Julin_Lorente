import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { PIAlerta, PIBuscar, PICalendario, PICampanas, PICapacitacion, PIContenidos, PIEditar, PIGuardar, PIInfo, PIMas, PIModulos, PIOk } from "../IconosPanel";
import Lateral from "./Lateral";
import "./usuarios.css";
import "./contenidos.css";
import { Aviso } from "./comunes";
import { descargar, useOperacion } from "./operaciones";

const TIPOS = { NOTICIA: ["Noticia", PIContenidos], ANUNCIO: ["Anuncio", PICampanas], MULTIMEDIA: ["Multimedia", PICapacitacion] };
const hoyLocal = () => new Date().toLocaleDateString("sv-SE");
const fecha = (iso) => iso ? new Date(`${iso}T00:00:00`).toLocaleDateString("es-EC", { day: "2-digit", month: "short", year: "numeric" }).replace(".", "") : "";
function situacion(c) {
  if (c.estado === "BORRADOR") return ["Borrador", "borrador"];
  if (c.estado === "RETIRADO") return ["Retirado", "retirado"];
  if (c.visible) return ["Publicado", "publicado"];
  return c.desde && c.desde > hoyLocal() ? ["Programado", "programado"] : ["Fuera de fecha", "retirado"];
}
function Campo({ etiqueta, icono: Icono, children }) {
  return <label className="gc-campo"><span>{etiqueta}</span><div className="gc-input">{Icono && <Icono aria-hidden="true" />}{children}</div></label>;
}

function FormContenido({ contenido, recargar, alCerrar }) {
  const [datos, setDatos] = useState(contenido || { titulo: "", cuerpo: "", categoria: "", tipo: "NOTICIA", desde: "", hasta: "" });
  const op = useOperacion(recargar); const cambiar = (clave) => (e) => setDatos({ ...datos, [clave]: e.target.value });
  async function enviar(e) {
    e.preventDefault();
    const { titulo, cuerpo, categoria, tipo, desde, hasta } = datos;
    const cuerpoApi = { titulo, cuerpo, categoria, tipo, desde: desde || null, hasta: hasta || null };
    if (await op.ejecutar(() => contenido ? api.putProtegido(`/plataforma/contenidos/${contenido.id}/`, cuerpoApi) : api.postProtegido("/plataforma/contenidos/", cuerpoApi))) alCerrar();
  }
  return <Lateral titulo={contenido ? "Editar contenido" : "Crear contenido"} subtitulo="Prepara el contenido; se guarda como borrador hasta que lo publiques." alCerrar={alCerrar}
    cabeza={<span className="us-cab-ico"><PIContenidos /></span>}
    pie={<><button type="button" className="boton boton--claro" disabled={op.ocupado} onClick={alCerrar}>Cancelar</button>
      <button form="form-contenido" className="boton boton--amarillo" type="submit" disabled={op.ocupado}><PIGuardar className="boton__ico" />{op.ocupado ? "Guardando…" : "Guardar borrador"}</button></>}>
    <form id="form-contenido" className="gc-form" onSubmit={enviar}>
      <Campo etiqueta="Título" icono={PIContenidos}><input required maxLength={200} value={datos.titulo} onChange={cambiar("titulo")} placeholder="Ej. Fundamentos de ahorro" /></Campo>
      <fieldset className="gc-tipos"><legend>Tipo</legend>{Object.entries(TIPOS).map(([valor, [etq, Ico]]) => <label key={valor} className={datos.tipo === valor ? "gc-tipo gc-tipo--on" : "gc-tipo"}>
        <input type="radio" name="tipo" value={valor} checked={datos.tipo === valor} onChange={cambiar("tipo")} /><Ico aria-hidden="true" />{etq}</label>)}</fieldset>
      <Campo etiqueta="Categoría" icono={PIModulos}><input required maxLength={100} value={datos.categoria} onChange={cambiar("categoria")} placeholder="Ej. Banco, Educación" /></Campo>
      <label className="gc-campo"><span>Cuerpo</span><textarea required maxLength={100000} rows={6} value={datos.cuerpo} onChange={cambiar("cuerpo")} placeholder="Escribe aquí el contenido…" /></label>
      <div className="gc-fechas">
        <Campo etiqueta="Mostrar desde" icono={PICalendario}><input type="date" required value={datos.desde || ""} onChange={cambiar("desde")} /></Campo>
        <Campo etiqueta="Mostrar hasta (opcional)" icono={PICalendario}><input type="date" min={datos.desde || ""} value={datos.hasta || ""} onChange={cambiar("hasta")} /></Campo></div>
      <p className="us-nota"><PIInfo aria-hidden="true" />Se guarda como borrador. Publícalo cuando hayas revisado su contenido. Para multimedia, adjunta los archivos desde Material educativo.</p>
      {op.error && <p className="alerta alerta--error" role="alert">{op.error}</p>}
    </form>
  </Lateral>;
}
const FILTROS = [["todos", "Todos"], ["borrador", "Borradores"], ["publicado", "Publicados"], ["programado", "Programados"], ["retirado", "Retirados"]];
export function GestionContenidos() {
  const r = useRecurso("/plataforma/contenidos/"); const op = useOperacion(r.recargar);
  const [editar, setEditar] = useState(null); const [nuevo, setNuevo] = useState(false); const [retirar, setRetirar] = useState(null); const [motivo, setMotivo] = useState("");
  const [filtro, setFiltro] = useState("todos"); const [q, setQ] = useState("");
  const lista = Array.isArray(r.datos) ? r.datos : [];
  const cuenta = (f) => f === "todos" ? lista.length : lista.filter((c) => situacion(c)[1] === f || (f === "retirado" && situacion(c)[1] === "retirado")).length;
  const vista = lista.filter((c) => (filtro === "todos" || situacion(c)[1] === filtro) && `${c.titulo} ${c.categoria}`.toLowerCase().includes(q.trim().toLowerCase()));
  return <div className="us gc">
    <div className="us-cab"><span className="us-cab__ico"><PIContenidos /></span><div className="us-cab__txt"><h1>Contenidos institucionales</h1><p>Prepara, publica y programa noticias, anuncios y multimedia.</p></div>
      <button className="boton boton--amarillo" onClick={() => setNuevo(true)}><PIMas className="boton__ico" />Crear contenido</button></div>
    {(r.error || op.error) && <p className="alerta alerta--error" role="alert">{r.error || op.error}</p>}
    {op.mensaje && <p className="gc-exito" role="status"><PIOk aria-hidden="true" />{op.mensaje}</p>}
    <div className="us-filtros gc-barra">
      <label className="us-buscar"><PIBuscar aria-hidden="true" /><input type="search" placeholder="Buscar por título o categoría" aria-label="Buscar por título o categoría" value={q} onChange={(e) => setQ(e.target.value)} /></label>
      <div className="gc-chips" role="group" aria-label="Filtrar por estado">{FILTROS.map(([v, etq]) => <button key={v} type="button" aria-pressed={filtro === v} className={filtro === v ? "gc-chip gc-chip--on" : "gc-chip"} onClick={() => setFiltro(v)}>{etq}<b>{cuenta(v)}</b></button>)}</div></div>
    {!r.datos && !r.error ? <p className="us-vacio" role="status">Cargando contenidos…</p> : vista.length === 0 ? <div className="us-tarjeta gc-vacio"><span><PIContenidos /></span><h2>{lista.length ? "Sin resultados" : "Aún no hay contenidos"}</h2>
      <p>{lista.length ? "Prueba con otro filtro o búsqueda." : "Crea el primero con el botón «Crear contenido»."}</p></div> :
    <div className="gc-grid">{vista.map((c) => { const [etq, clase] = situacion(c); const [tipoEtq, Ico] = TIPOS[c.tipo] ?? [c.tipo, PIContenidos]; return <article key={c.id} className="gc-card">
      <header><span className="gc-card__ico"><Ico /></span><div><h2>{c.titulo}</h2><small>{tipoEtq} · {c.categoria}</small></div><span className={`us-estado gc-est gc-est--${clase}`}>{etq}</span></header>
      <p className="gc-card__txt">{c.cuerpo}</p>
      <p className="gc-card__fechas"><PICalendario aria-hidden="true" />{fecha(c.desde) || "Sin definir"} — {c.hasta ? fecha(c.hasta) : "Sin fecha de fin"}</p>
      <div className="gc-card__acc"><button className="boton boton--claro" onClick={() => setEditar(c)}><PIEditar className="boton__ico" />Editar</button>
        <button className="boton boton--azul" disabled={op.ocupado || c.estado === "PUBLICADO"} onClick={() => op.ejecutar(() => api.postProtegido(`/plataforma/contenidos/${c.id}/publicar/`, {}), "Contenido publicado o programado según sus fechas.")}>Publicar / programar</button>
        <button className="boton boton--claro" disabled={c.estado === "RETIRADO"} onClick={() => { setRetirar(c); setMotivo(""); }}>Retirar</button></div>
    </article>; })}</div>}
    {(nuevo || editar) && <FormContenido contenido={editar} recargar={r.recargar} alCerrar={() => { setEditar(null); setNuevo(false); }} />}
    {retirar && <Lateral titulo="Retirar contenido" subtitulo={retirar.titulo} alCerrar={() => setRetirar(null)} cabeza={<span className="us-cab-ico"><PIAlerta /></span>}
      pie={<><button type="button" className="boton boton--claro" onClick={() => setRetirar(null)}>Cancelar</button><button form="form-retiro" className="boton boton--amarillo" disabled={op.ocupado}>Confirmar retiro</button></>}>
      <form id="form-retiro" className="gc-form" onSubmit={async (e) => { e.preventDefault(); if (await op.ejecutar(() => api.postProtegido(`/plataforma/contenidos/${retirar.id}/retirar/`, { motivo }))) setRetirar(null); }}>
        <label className="gc-campo"><span>Motivo</span><textarea required maxLength={1000} rows={4} value={motivo} onChange={(e) => setMotivo(e.target.value)} placeholder="Explica por qué se retira este contenido" /></label>
        {op.error && <p className="alerta alerta--error" role="alert">{op.error}</p>}</form></Lateral>}
  </div>;
}
export function Publicaciones() {
  const r = useRecurso("/plataforma/publicaciones/"); const op = useOperacion();
  return <><TituloPagina titulo="Publicaciones" sub="Información institucional disponible en este momento." /><Aviso error={r.error || op.error} />
    <div className="s2-lista">{r.datos?.map((c) => <article className="s2-publicacion" key={c.id}><h2>{c.titulo}</h2><p>{c.categoria} · {c.desde}</p>
      <p className="s2-texto">{c.cuerpo}</p>{c.materiales.map((m) => <button className="boton boton--claro" key={m.id} disabled={op.ocupado} onClick={() => op.ejecutar(() => descargar(`/plataforma/materiales/${m.id}/archivo/`, m.titulo), "Archivo descargado.")}>Descargar {m.titulo}</button>)}
    </article>)}</div>{r.datos?.length === 0 && <Tarjeta><p className="vacio">No hay publicaciones vigentes.</p></Tarjeta>}</>;
}
