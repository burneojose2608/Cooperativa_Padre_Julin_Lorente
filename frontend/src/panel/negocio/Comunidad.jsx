import { useEffect, useMemo, useState } from "react";
import { api } from "../../api/cliente";
import FotoPerfil from "../../components/FotoPerfil";
import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { Aviso, CampoPanel } from "../sprint2/comunes";
import { useOperacion } from "../sprint2/operaciones";
import { Tabla } from "./Modulos";
import "./comunidad.css";

const BASE = "/plataforma/negocio/";
const fechaComunidad = new Intl.DateTimeFormat("es-EC", { dateStyle: "medium", timeStyle: "short" });

function FotoAutor({ id, comentario, alias, tieneFoto }) {
  const perfil = useMemo(() => ({ nombre: alias, tiene_foto: tieneFoto }), [alias, tieneFoto]);
  const ruta = `${BASE}comunidad/${id}/${comentario ? `comentarios/${comentario}/` : ""}foto-autor/`;
  return <FotoPerfil perfil={perfil} ruta={ruta}
    className="comunidad-inicial comunidad-foto-autor" claseIniciales="comunidad-inicial" />;
}

function ImagenPublicacion({ id }) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState(false);

  useEffect(() => {
    let vigente = true;
    let objeto;
    api.archivoProtegido(`${BASE}comunidad/${id}/imagen/`).then((archivo) => {
      if (!vigente) return;
      objeto = URL.createObjectURL(archivo);
      setUrl(objeto);
    }).catch(() => {
      if (vigente) setError(true);
    });
    return () => {
      vigente = false;
      if (objeto) URL.revokeObjectURL(objeto);
    };
  }, [id]);

  if (error) return <p role="status">No se pudo mostrar la imagen.</p>;
  return url
    ? <img className="comunidad-imagen" src={url} alt="Imagen adjunta a la publicación" draggable={false} />
    : <p role="status">Cargando imagen…</p>;
}

export function Comunidad() {
  const r = useRecurso(`${BASE}comunidad/`);
  const op = useOperacion(r.recargar);
  const [texto, setTexto] = useState("");
  const [imagen, setImagen] = useState(null);
  const [comentarios, setComentarios] = useState({});
  const [reporte, setReporte] = useState(null);
  const [motivo, setMotivo] = useState("");

  async function publicar(e) {
    e.preventDefault();
    const formulario = e.currentTarget;
    const datos = new FormData();
    datos.set("texto", texto);
    if (imagen) datos.set("imagen", imagen);
    if (await op.ejecutar(() => api.postProtegido(`${BASE}comunidad/`, datos), "Publicaci?n compartida.")) {
      setTexto("");
      setImagen(null);
      formulario.reset();
    }
  }

  function abrirReporte(publicacion, comentario) {
    setMotivo("");
    setReporte({ publicacion, comentario });
  }

  async function enviarReporte(e) {
    e.preventDefault();
    const datos = { motivo };
    if (reporte.comentario) datos.comentario = reporte.comentario;
    if (await op.ejecutar(() => api.postProtegido(`${BASE}comunidad/${reporte.publicacion}/reportar/`, datos), "Reporte enviado a moderación.")) {
      setReporte(null);
    }
  }

  return <div className="comunidad">
    <header className="comunidad-cabecera">
      <TituloPagina titulo="Comunidad de socios" sub="Comparte aprendizajes y conversa con otros socios." />
    </header>
    <div className="comunidad-muro">
      <Aviso error={r.error || op.error} mensaje={op.mensaje} />
      <section className="comunidad-tarjeta" aria-labelledby="comunidad-nueva">
        <h2 id="comunidad-nueva">Nueva publicación</h2>
        <form className="comunidad-formulario" onSubmit={publicar}>
          <label className="comunidad-campo">
            Tu publicación
            <textarea required rows={2} maxLength={10000} value={texto}
              placeholder="¿Qué te gustaría compartir?" onChange={(e) => setTexto(e.target.value)} />
          </label>
          <div className="comunidad-acciones comunidad-publicar">
            <label className="comunidad-adjunto">
              Imagen opcional · hasta 10 MB
              <input type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => setImagen(e.target.files[0])} />
            </label>
            <button className="boton boton--amarillo" disabled={op.ocupado || !texto.trim()}>Publicar</button>
          </div>
        </form>
      </section>
      <section className="comunidad-feed" aria-labelledby="comunidad-publicaciones">
        <h2 id="comunidad-publicaciones">Publicaciones de socios</h2>
        {!r.datos && !r.error && <p role="status">Cargando publicaciones…</p>}
        {r.datos?.resultados.length === 0 && <p className="comunidad-tarjeta">Aún no hay publicaciones. Comparte tu primer aprendizaje.</p>}
        {r.datos?.resultados.map((p) => <article className="comunidad-tarjeta" key={p.id}>
          <header className="comunidad-autor">
            <FotoAutor id={p.id} alias={p.alias} tieneFoto={p.tiene_foto} />
            <div>
              <h3>{p.alias}</h3>
              {p.fecha && <time dateTime={p.fecha}>{fechaComunidad.format(new Date(p.fecha))}</time>}
            </div>
          </header>
          <p className="comunidad-texto">{p.texto}</p>
          {p.imagen && <ImagenPublicacion id={p.id} />}
          <div className="comunidad-acciones comunidad-interacciones">
            <button className="boton boton--claro" disabled={op.ocupado} onClick={() => op.ejecutar(
              () => api.postProtegido(`${BASE}comunidad/${p.id}/reaccionar/`, { tipo: "ME_GUSTA" }), "Reacción guardada.")}>Me gusta · {p.reacciones}</button>
            <button className="comunidad-secundario" onClick={() => abrirReporte(p.id)}>Reportar publicación</button>
          </div>
          <details className="comunidad-comentarios">
            <summary>Comentarios ({p.comentarios.length})</summary>
            {p.comentarios.length > 0 && <ul>{p.comentarios.map((c) => <li key={c.id}>
              <FotoAutor id={p.id} comentario={c.id} alias={c.alias} tieneFoto={c.tiene_foto} />
              <div>
                <p className="comunidad-texto"><strong>{c.alias}</strong> {c.texto}</p>
                <button className="comunidad-secundario" onClick={() => abrirReporte(p.id, c.id)}>Reportar comentario</button>
              </div>
            </li>)}</ul>}
            <form className="comunidad-acciones comunidad-respuesta" onSubmit={async (e) => {
              e.preventDefault();
              if (await op.ejecutar(() => api.postProtegido(`${BASE}comunidad/${p.id}/comentar/`, { texto: comentarios[p.id] }), "Comentario publicado.")) {
                setComentarios((actual) => ({ ...actual, [p.id]: "" }));
              }
            }}>
              <CampoPanel etiqueta={`Comentar a ${p.alias}`} required maxLength={2000} value={comentarios[p.id] || ""}
                onChange={(e) => setComentarios((actual) => ({ ...actual, [p.id]: e.target.value }))} />
              <button className="boton" disabled={op.ocupado || !comentarios[p.id]?.trim()}>Comentar</button>
            </form>
          </details>
          {reporte?.publicacion === p.id && <form className="comunidad-formulario comunidad-reporte" onSubmit={enviarReporte}>
            <h4>{reporte.comentario ? "Reportar comentario" : "Reportar publicación"}</h4>
            <CampoPanel etiqueta="Motivo del reporte" required autoFocus value={motivo} onChange={(e) => setMotivo(e.target.value)} />
            <div className="comunidad-acciones">
              <button className="boton" disabled={op.ocupado || !motivo.trim()}>Enviar reporte</button>
              <button className="boton boton--claro" type="button" onClick={() => setReporte(null)}>Cancelar</button>
            </div>
          </form>}
        </article>)}
      </section>
    </div>
  </div>;
}

export function PerfilPublico() {
  const r = useRecurso(`${BASE}perfil-publico/`); const op = useOperacion(r.recargar);
  const [alias, setAlias] = useState(null); const [publico, setPublico] = useState(null);
  return <><TituloPagina titulo="Privacidad y perfil público" /><Aviso error={r.error || op.error} mensaje={op.mensaje} />
    <p>La comunidad muestra tu alias. Si no has configurado uno, tus comentarios muestran tu primer nombre. Tu cédula, correo y teléfono permanecen privados. La clasificación pública requiere tu elección.</p>
    {r.datos && <form className="s2-form" onSubmit={(e) => { e.preventDefault(); op.ejecutar(() => api.putProtegido(`${BASE}perfil-publico/`,
      { alias: alias ?? r.datos.alias, ranking_publico: publico ?? r.datos.ranking_publico })); }}>
      <CampoPanel etiqueta="Alias público" required maxLength={60} value={alias ?? r.datos.alias} onChange={(e) => setAlias(e.target.value)} />
      <label><input type="checkbox" checked={publico ?? r.datos.ranking_publico} onChange={(e) => setPublico(e.target.checked)} /> Aparecer con mi alias en la clasificación</label>
      <button disabled={op.ocupado} className="boton">Guardar preferencias</button></form>}
  </>;
}

export function Ranking() {
  const [desde, setDesde] = useState(""); const [hasta, setHasta] = useState("");
  const [consulta, setConsulta] = useState("");
  const r = useRecurso(`${BASE}ranking/${consulta}`);
  return <><TituloPagina titulo="Clasificación de socios" /><Aviso error={r.error} />
    <form className="s2-form" onSubmit={(e) => {
      e.preventDefault();
      const filtros = new URLSearchParams(Object.entries({ desde, hasta }).filter(([, valor]) => valor));
      setConsulta(filtros.size ? `?${filtros}` : "");
    }}>
      <CampoPanel etiqueta="Desde" type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
      <CampoPanel etiqueta="Hasta" type="date" value={hasta} min={desde || undefined} onChange={(e) => setHasta(e.target.value)} />
      <button className="boton">Aplicar período</button>
    </form>
    <p>Tu posición: {r.datos?.mi_posicion ?? "Completa actividades para entrar a la clasificación"}.</p>
    <Tabla filas={r.datos?.resultados} columnas={["posicion", "alias", "puntos"]} />
  </>;
}

export function Moderacion() {
  const r = useRecurso(`${BASE}moderacion/`); const op = useOperacion(r.recargar); const [seleccion, setSeleccion] = useState(null);
  const [motivo, setMotivo] = useState(""); const [accion, setAccion] = useState("OCULTAR"); const [dias, setDias] = useState(0);
  return <><TituloPagina titulo="Moderación de comunidad" /><Aviso error={r.error || op.error} mensaje={op.mensaje} />
    {r.datos?.resultados.map((p) => <Tarjeta key={p.id} titulo={`Reporte ${p.id}`}><p>{p.motivo}</p><p className="neg-post">{p.texto}</p><button onClick={() => setSeleccion(p)}>Resolver</button></Tarjeta>)}
    {seleccion && <form className="s2-form" onSubmit={async (e) => { e.preventDefault(); if (await op.ejecutar(() => api.postProtegido(`${BASE}moderacion/`,
      { reporte: seleccion.id, accion, motivo, suspension_dias: Number(dias) }))) setSeleccion(null); }}>
      <CampoPanel etiqueta="Decisión"><select value={accion} onChange={(e) => setAccion(e.target.value)}>{["OCULTAR", "ELIMINAR", "DESCARTAR"].map((a) => <option key={a}>{a}</option>)}</select></CampoPanel>
      <CampoPanel etiqueta="Justificación" value={motivo} required onChange={(e) => setMotivo(e.target.value)} />
      <CampoPanel etiqueta="Días de suspensión de participación (0 para no suspender)" type="number" min="0" max="365" value={dias} onChange={(e) => setDias(e.target.value)} />
      <button className="boton" disabled={op.ocupado}>Confirmar resolución</button><button type="button" onClick={() => setSeleccion(null)}>Cancelar</button>
    </form>}
  </>;
}
