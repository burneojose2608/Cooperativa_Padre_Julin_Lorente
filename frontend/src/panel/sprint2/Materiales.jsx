import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Modal, Tarjeta, TituloPagina } from "../ui";
import { Aviso, CampoPanel } from "./comunes";
import { descargar, useOperacion } from "./operaciones";

function SelectorContenido({ valor, cambiar }) {
  const r = useRecurso("/plataforma/contenidos/");
  return <><CampoPanel etiqueta="Contenido asociado (opcional)"><select value={valor} onChange={(e) => cambiar(e.target.value)}>
    <option value="">Sin asociación institucional</option>{r.datos?.map((c) => <option value={c.id} key={c.id}>{c.titulo} · {c.estado}</option>)}
  </select></CampoPanel><Aviso error={r.error} /></>;
}

function FormMaterial({ material, modulos, recargar, alCerrar }) {
  const { usuario } = useAuth();
  const puedeContenido = usuario?.permisos?.includes("contenidos.gestionar");
  const [titulo, setTitulo] = useState(material?.titulo || ""); const [categoria, setCategoria] = useState(material?.categoria || "");
  const [archivo, setArchivo] = useState(null); const [contenido, setContenido] = useState(material?.contenido || "");
  const [ids, setIds] = useState(material?.modulos || []); const op = useOperacion(recargar);
  async function enviar(e) {
    e.preventDefault(); const datos = new FormData(); datos.append("titulo", titulo); datos.append("categoria", categoria);
    if (archivo) datos.append("archivo", archivo);
    if (puedeContenido) datos.append("contenido", String(contenido));
    datos.append("modulos", JSON.stringify(ids));
    if (await op.ejecutar(() => material ? api.putProtegido(`/plataforma/materiales/${material.id}/`, datos) : api.postProtegido("/plataforma/materiales/", datos))) alCerrar();
  }
  return <Modal titulo={material ? "Editar material educativo" : "Agregar material educativo"} alCerrar={alCerrar}><form className="s2-form" onSubmit={enviar}>
    <CampoPanel etiqueta="Título del material" required maxLength={200} value={titulo} onChange={(e) => setTitulo(e.target.value)} />
    <CampoPanel etiqueta="Categoría" required maxLength={100} value={categoria} onChange={(e) => setCategoria(e.target.value)} />
    <CampoPanel etiqueta={`Archivo (PDF, JPG, PNG, WebP o MP4; hasta 10 MB)${material ? " · reemplazo opcional" : ""}`} type="file" required={!material} accept="application/pdf,image/jpeg,image/png,image/webp,video/mp4" onChange={(e) => setArchivo(e.target.files[0])} />
    {puedeContenido && <SelectorContenido valor={contenido} cambiar={setContenido} />}
    <fieldset><legend>Reutilizar en módulos de capacitación</legend>{modulos.length ? modulos.map((m) => <label className="s2-check" key={m.id}><input type="checkbox" checked={ids.includes(m.id)} onChange={(e) => setIds(e.target.checked ? [...ids, m.id] : ids.filter((id) => id !== m.id))} />{m.capacitacion} / {m.titulo}</label>) : <p>Las capacitaciones y sus módulos se crearán en el sprint correspondiente. El material permanece disponible en la biblioteca.</p>}</fieldset>
    <Aviso {...op} /><button className="boton" disabled={op.ocupado}>Guardar material</button>
  </form></Modal>;
}
export default function Materiales() {
  const r = useRecurso("/plataforma/materiales/"); const op = useOperacion(r.recargar); const [editar, setEditar] = useState(null); const [nuevo, setNuevo] = useState(false); const [eliminar, setEliminar] = useState(null);
  return <><TituloPagina titulo="Material educativo" sub="Biblioteca privada con recursos reutilizables para formación."><button className="boton" onClick={() => setNuevo(true)}>Agregar material</button></TituloPagina>
    <Aviso error={r.error || op.error} mensaje={op.mensaje} /><div className="s2-lista">{r.datos?.materiales.map((m) => <article key={m.id}><h2>{m.titulo}</h2>
      <p>{m.categoria} · {m.formato} · {(m.tamano_bytes / 1024).toFixed(1)} KB · {m.modulos.length} módulos</p>{m.contenido && <p>Contenido asociado #{m.contenido}</p>}
      <div className="s2-acciones"><button className="boton boton--claro" onClick={() => setEditar(m)}>Editar</button>
        <button className="boton boton--claro" disabled={op.ocupado} onClick={() => op.ejecutar(() => descargar(`/plataforma/materiales/${m.id}/archivo/`, m.titulo), "Archivo descargado.")}>Descargar</button>
        <button className="boton boton--claro" onClick={() => setEliminar(m)}>Eliminar</button></div>
    </article>)}</div>{r.datos?.materiales.length === 0 && <Tarjeta><p className="vacio">Aún no hay materiales registrados.</p></Tarjeta>}
    {(nuevo || editar) && <FormMaterial material={editar} modulos={r.datos?.modulos || []} recargar={r.recargar} alCerrar={() => { setNuevo(false); setEditar(null); }} />}
    {eliminar && <Modal titulo="Eliminar material" alCerrar={() => setEliminar(null)}><div className="s2-form"><p>¿Eliminar «{eliminar.titulo}» de la biblioteca y de los módulos donde se reutiliza?</p><Aviso {...op} />
      <button className="boton" disabled={op.ocupado} onClick={async () => { if (await op.ejecutar(() => api.deleteProtegido(`/plataforma/materiales/${eliminar.id}/`))) setEliminar(null); }}>Confirmar eliminación</button></div></Modal>}
  </>;
}
