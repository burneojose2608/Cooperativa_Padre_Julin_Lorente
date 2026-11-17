import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Modal, Tarjeta, TituloPagina } from "../ui";
import { Aviso, CampoPanel } from "./comunes";
import { descargar, useOperacion } from "./operaciones";

function FormContenido({ contenido, recargar, alCerrar }) {
  const [datos, setDatos] = useState(contenido || { titulo: "", cuerpo: "", categoria: "", tipo: "NOTICIA", desde: "", hasta: "" });
  const op = useOperacion(recargar); const cambiar = (clave) => (e) => setDatos({ ...datos, [clave]: e.target.value });
  async function enviar(e) {
    e.preventDefault();
    const { titulo, cuerpo, categoria, tipo, desde, hasta } = datos;
    const cuerpoApi = { titulo, cuerpo, categoria, tipo, desde: desde || null, hasta: hasta || null };
    if (await op.ejecutar(() => contenido ? api.putProtegido(`/plataforma/contenidos/${contenido.id}/`, cuerpoApi) : api.postProtegido("/plataforma/contenidos/", cuerpoApi))) alCerrar();
  }
  return <Modal titulo={contenido ? "Editar contenido" : "Crear contenido"} alCerrar={alCerrar}><form className="s2-form" onSubmit={enviar}>
    <CampoPanel etiqueta="Título" required maxLength={200} value={datos.titulo} onChange={cambiar("titulo")} />
    <CampoPanel etiqueta="Cuerpo"><textarea required maxLength={100000} value={datos.cuerpo} onChange={cambiar("cuerpo")} /></CampoPanel>
    <CampoPanel etiqueta="Categoría" required maxLength={100} value={datos.categoria} onChange={cambiar("categoria")} />
    <CampoPanel etiqueta="Tipo"><select value={datos.tipo} onChange={cambiar("tipo")}>{["NOTICIA", "ANUNCIO", "MULTIMEDIA"].map((v) => <option key={v}>{v}</option>)}</select></CampoPanel>
    <CampoPanel etiqueta="Mostrar desde" type="date" required value={datos.desde || ""} onChange={cambiar("desde")} />
    <CampoPanel etiqueta="Mostrar hasta (opcional)" type="date" min={datos.desde || ""} value={datos.hasta || ""} onChange={cambiar("hasta")} />
    <p>Se guarda como borrador. Publícalo cuando hayas revisado su contenido. Para multimedia, adjunta los archivos desde Material educativo.</p>
    <Aviso {...op} /><button className="boton" disabled={op.ocupado}>Guardar borrador</button>
  </form></Modal>;
}
export function GestionContenidos() {
  const r = useRecurso("/plataforma/contenidos/"); const op = useOperacion(r.recargar);
  const [editar, setEditar] = useState(null); const [nuevo, setNuevo] = useState(false); const [retirar, setRetirar] = useState(null); const [motivo, setMotivo] = useState("");
  return <><TituloPagina titulo="Contenidos institucionales" sub="Prepara, publica y programa noticias, anuncios y multimedia."><button className="boton" onClick={() => setNuevo(true)}>Crear contenido</button></TituloPagina>
    <Aviso error={r.error || op.error} mensaje={op.mensaje} /><div className="s2-lista">{r.datos?.map((c) => <article key={c.id}>
      <h2>{c.titulo}</h2><p>{c.tipo} · {c.categoria} · <span className="s2-estado">{c.estado}</span> · {c.visible ? "Visible" : "Sin mostrar"}</p>
      <p>Desde {c.desde || "Sin definir"} hasta {c.hasta || "Sin fecha de fin"} · Autor #{c.autor}</p><p className="s2-texto">{c.cuerpo}</p>
      <div className="s2-acciones"><button className="boton boton--claro" onClick={() => setEditar(c)}>Editar</button>
        <button className="boton" disabled={op.ocupado || c.estado === "PUBLICADO"} onClick={() => op.ejecutar(() => api.postProtegido(`/plataforma/contenidos/${c.id}/publicar/`, {}), "Contenido publicado o programado según sus fechas.")}>Publicar / programar</button>
        <button className="boton boton--claro" disabled={c.estado === "RETIRADO"} onClick={() => { setRetirar(c); setMotivo(""); }}>Retirar</button></div>
    </article>)}</div>{r.datos?.length === 0 && <Tarjeta><p className="vacio">Aún no hay contenidos.</p></Tarjeta>}
    {(nuevo || editar) && <FormContenido contenido={editar} recargar={r.recargar} alCerrar={() => { setEditar(null); setNuevo(false); }} />}
    {retirar && <Modal titulo={`Retirar ${retirar.titulo}`} alCerrar={() => setRetirar(null)}><form className="s2-form" onSubmit={async (e) => { e.preventDefault(); if (await op.ejecutar(() => api.postProtegido(`/plataforma/contenidos/${retirar.id}/retirar/`, { motivo }))) setRetirar(null); }}>
      <CampoPanel etiqueta="Motivo" required maxLength={1000} value={motivo} onChange={(e) => setMotivo(e.target.value)} /><Aviso {...op} /><button className="boton" disabled={op.ocupado}>Confirmar retiro</button>
    </form></Modal>}
  </>;
}
export function Publicaciones() {
  const r = useRecurso("/plataforma/publicaciones/"); const op = useOperacion();
  return <><TituloPagina titulo="Publicaciones" sub="Información institucional disponible en este momento." /><Aviso error={r.error || op.error} />
    <div className="s2-lista">{r.datos?.map((c) => <article className="s2-publicacion" key={c.id}><h2>{c.titulo}</h2><p>{c.categoria} · {c.desde}</p>
      <p className="s2-texto">{c.cuerpo}</p>{c.materiales.map((m) => <button className="boton boton--claro" key={m.id} disabled={op.ocupado} onClick={() => op.ejecutar(() => descargar(`/plataforma/materiales/${m.id}/archivo/`, m.titulo), "Archivo descargado.")}>Descargar {m.titulo}</button>)}
    </article>)}</div>{r.datos?.length === 0 && <Tarjeta><p className="vacio">No hay publicaciones vigentes.</p></Tarjeta>}</>;
}
