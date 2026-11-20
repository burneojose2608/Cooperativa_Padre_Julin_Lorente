import { useRef, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { PIAlerta, PIBorrar, PIBuscar, PICalendario, PICamara, PICapacitacion, PIContenidos, PIEditar, PIGuardar, PIJuegos, PIMas, PIModulos, PIOk, PICompartir } from "../IconosPanel";
import Lateral from "./Lateral";
import { descargar, useOperacion } from "./operaciones";
import "./usuarios.css";
import "./contenidos.css";
import "./materiales.css";

const tamano = (b) => b >= 1048576 ? `${(b / 1048576).toFixed(1)} MB` : `${(b / 1024).toFixed(1)} KB`;
const iconoDe = (formato = "") => /mp4|video/i.test(formato) ? PIJuegos : /jpe?g|png|webp|image/i.test(formato) ? PICamara : PIContenidos;
function Campo({ etiqueta, icono: Icono, children }) {
  return <label className="gc-campo"><span>{etiqueta}</span><div className="gc-input">{Icono && <Icono aria-hidden="true" />}{children}</div></label>;
}

function SelectorContenido({ valor, cambiar }) {
  const r = useRecurso("/plataforma/contenidos/");
  return <><Campo etiqueta="Contenido asociado (opcional)" icono={PIContenidos}><select value={valor} onChange={(e) => cambiar(e.target.value)}>
    <option value="">Sin asociación institucional</option>{Array.isArray(r.datos) && r.datos.map((c) => <option value={c.id} key={c.id}>{c.titulo} · {c.estado}</option>)}
  </select></Campo>{r.error && <p className="alerta alerta--error" role="alert">{r.error}</p>}</>;
}

function FormMaterial({ material, modulos, recargar, alCerrar }) {
  const { usuario } = useAuth();
  const puedeContenido = usuario?.permisos?.includes("contenidos.gestionar");
  const [titulo, setTitulo] = useState(material?.titulo || ""); const [categoria, setCategoria] = useState(material?.categoria || "");
  const [archivo, setArchivo] = useState(null); const [contenido, setContenido] = useState(material?.contenido || "");
  const [ids, setIds] = useState(material?.modulos || []); const op = useOperacion(recargar); const entrada = useRef(null);
  async function enviar(e) {
    e.preventDefault(); const datos = new FormData(); datos.append("titulo", titulo); datos.append("categoria", categoria);
    if (archivo) datos.append("archivo", archivo);
    if (puedeContenido) datos.append("contenido", String(contenido));
    datos.append("modulos", JSON.stringify(ids));
    if (await op.ejecutar(() => material ? api.putProtegido(`/plataforma/materiales/${material.id}/`, datos) : api.postProtegido("/plataforma/materiales/", datos))) alCerrar();
  }
  return <Lateral titulo={material ? "Editar material educativo" : "Agregar material educativo"} subtitulo="Súbelo una vez y reutilízalo en tus capacitaciones." alCerrar={alCerrar}
    cabeza={<span className="us-cab-ico"><PICapacitacion /></span>}
    pie={<><button type="button" className="boton boton--claro" disabled={op.ocupado} onClick={alCerrar}>Cancelar</button>
      <button form="form-material" className="boton boton--amarillo" type="submit" disabled={op.ocupado}><PIGuardar className="boton__ico" />{op.ocupado ? "Guardando…" : "Guardar material"}</button></>}>
    <form id="form-material" className="gc-form" onSubmit={enviar}>
      <Campo etiqueta="Título del material" icono={PICapacitacion}><input required maxLength={200} value={titulo} onChange={(e) => setTitulo(e.target.value)} placeholder="Ej. Guía de ahorro" /></Campo>
      <Campo etiqueta="Categoría" icono={PIModulos}><input required maxLength={100} value={categoria} onChange={(e) => setCategoria(e.target.value)} placeholder="Ej. Educación financiera" /></Campo>
      <div className="gc-campo"><span id="et-archivo">Archivo{material ? " · reemplazo opcional" : ""}</span>
        <label className={archivo ? "mg-zona mg-zona--lleno" : "mg-zona"}>
          <input ref={entrada} type="file" aria-labelledby="et-archivo" required={!material} accept="application/pdf,image/jpeg,image/png,image/webp,video/mp4" onChange={(e) => setArchivo(e.target.files[0] ?? null)} />
          <span className="mg-zona__ico">{archivo ? <PIOk /> : <PICompartir />}</span>
          <strong>{archivo ? archivo.name : "Selecciona un archivo"}</strong>
          <small>{archivo ? tamano(archivo.size) : "PDF, JPG, PNG, WebP o MP4 · hasta 10 MB"}</small></label></div>
      {puedeContenido && <SelectorContenido valor={contenido} cambiar={setContenido} />}
      <fieldset className="mg-modulos"><legend>Reutilizar en módulos de capacitación</legend>
        {modulos.length ? modulos.map((m) => <label className="us-rol" key={m.id}><input type="checkbox" checked={ids.includes(m.id)} onChange={(e) => setIds(e.target.checked ? [...ids, m.id] : ids.filter((id) => id !== m.id))} /><span>{m.capacitacion} / {m.titulo}</span></label>)
          : <p className="mg-nota">Las capacitaciones y sus módulos se crearán en el sprint correspondiente. El material permanece disponible en la biblioteca.</p>}</fieldset>
      {op.error && <p className="alerta alerta--error" role="alert">{op.error}</p>}
    </form>
  </Lateral>;
}

export default function Materiales() {
  const r = useRecurso("/plataforma/materiales/"); const op = useOperacion(r.recargar); const [editar, setEditar] = useState(null); const [nuevo, setNuevo] = useState(false); const [eliminar, setEliminar] = useState(null);
  const [q, setQ] = useState("");
  const lista = r.datos?.materiales ?? [];
  const vista = lista.filter((m) => `${m.titulo} ${m.categoria}`.toLowerCase().includes(q.trim().toLowerCase()));
  return <div className="us gc">
    <div className="us-cab"><span className="us-cab__ico"><PICapacitacion /></span><div className="us-cab__txt"><h1>Material educativo</h1><p>Biblioteca privada con recursos reutilizables para formación.</p></div>
      <button className="boton boton--amarillo" onClick={() => setNuevo(true)}><PIMas className="boton__ico" />Agregar material</button></div>
    {(r.error || op.error) && <p className="alerta alerta--error" role="alert">{r.error || op.error}</p>}
    {op.mensaje && <p className="gc-exito" role="status"><PIOk aria-hidden="true" />{op.mensaje}</p>}
    {lista.length > 0 && <div className="us-filtros"><label className="us-buscar"><PIBuscar aria-hidden="true" /><input type="search" placeholder="Buscar por título o categoría" aria-label="Buscar por título o categoría" value={q} onChange={(e) => setQ(e.target.value)} /></label>
      <span className="mg-total">{lista.length} {lista.length === 1 ? "material" : "materiales"}</span></div>}
    {!r.datos && !r.error ? <p className="us-vacio" role="status">Cargando materiales…</p> : vista.length === 0 ? <div className="us-tarjeta gc-vacio"><span><PICapacitacion /></span><h2>{lista.length ? "Sin resultados" : "Aún no hay materiales registrados"}</h2>
      <p>{lista.length ? "Prueba con otra búsqueda." : "Agrega el primero con el botón «Agregar material»."}</p></div> :
    <div className="gc-grid">{vista.map((m) => { const Ico = iconoDe(m.formato); return <article key={m.id} className="gc-card">
      <header><span className="gc-card__ico"><Ico /></span><div><h2>{m.titulo}</h2><small>{m.categoria}</small></div><span className="us-estado mg-formato">{m.formato}</span></header>
      <p className="gc-card__fechas"><PIModulos aria-hidden="true" />{tamano(m.tamano_bytes)} · {m.modulos.length} {m.modulos.length === 1 ? "módulo" : "módulos"}</p>
      {m.contenido && <p className="gc-card__fechas"><PIContenidos aria-hidden="true" />Contenido asociado #{m.contenido}</p>}
      <div className="gc-card__acc"><button className="boton boton--claro" onClick={() => setEditar(m)}><PIEditar className="boton__ico" />Editar</button>
        <button className="boton boton--azul" disabled={op.ocupado} onClick={() => op.ejecutar(() => descargar(`/plataforma/materiales/${m.id}/archivo/`, m.titulo), "Archivo descargado.")}>Descargar</button>
        <button className="boton boton--claro" onClick={() => setEliminar(m)}><PIBorrar className="boton__ico" />Eliminar</button></div>
    </article>; })}</div>}
    {(nuevo || editar) && <FormMaterial material={editar} modulos={r.datos?.modulos || []} recargar={r.recargar} alCerrar={() => { setNuevo(false); setEditar(null); }} />}
    {eliminar && <Lateral titulo="Eliminar material" subtitulo={eliminar.titulo} alCerrar={() => setEliminar(null)} cabeza={<span className="us-cab-ico"><PIAlerta /></span>}
      pie={<><button type="button" className="boton boton--claro" onClick={() => setEliminar(null)}>Cancelar</button>
        <button className="boton boton--amarillo" disabled={op.ocupado} onClick={async () => { if (await op.ejecutar(() => api.deleteProtegido(`/plataforma/materiales/${eliminar.id}/`))) setEliminar(null); }}>Confirmar eliminación</button></>}>
      <div className="gc-form"><p className="us-nota"><PIAlerta aria-hidden="true" />¿Eliminar «{eliminar.titulo}» de la biblioteca y de los módulos donde se reutiliza? Esta acción no se puede deshacer.</p>
        {op.error && <p className="alerta alerta--error" role="alert">{op.error}</p>}</div></Lateral>}
  </div>;
}
