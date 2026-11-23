import { useState } from "react";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { Aviso, CampoPanel } from "../sprint2/comunes";
import { descargar, useOperacion } from "../sprint2/operaciones";
import VistaReferidos from "../sprint2/Referidos";
import "./negocio.css";
import "./capacitaciones.css";

const BASE = "/plataforma/negocio/";
const etiqueta = (v) => v.replaceAll("_", " ").replace(/^./, (c) => c.toUpperCase());
const ETIQUETAS_DATOS = { costo_puntos: "Costo en puntos", umbral_puntos: "Puntos requeridos", duracion: "Duración", id: "ID" };
const TITULOS = { campanas: "Campañas", niveles: "Niveles", insignias: "Insignias", capacitaciones: "Capacitaciones",
  modulos: "Módulos de capacitación", evaluaciones: "Evaluaciones", talleres: "Talleres", convenios: "Convenios de bienestar",
  beneficios: "Beneficios", sorteos: "Sorteos", juegos: "Juegos educativos", retos: "Retos", plantillas: "Plantillas de notificación", gastos: "Gastos de captación" };

function BancoPreguntas({ value = [], onChange }) {
  function cambiar(i, campo, valor) { onChange(value.map((p, n) => n === i ? { ...p, [campo]: valor } : p)); }
  return <fieldset className="neg-banco"><legend>Preguntas y respuestas</legend>
    {value.map((p, i) => <div className="neg-pregunta" key={i}>
      <CampoPanel etiqueta={`Pregunta ${i + 1}`} value={p.enunciado} required onChange={(e) => cambiar(i, "enunciado", e.target.value)} />
      {p.opciones.map((o, j) => <CampoPanel etiqueta={`Opción ${j + 1}`} key={j} value={o} required
        onChange={(e) => cambiar(i, "opciones", p.opciones.map((x, n) => n === j ? e.target.value : x))} />)}
      <CampoPanel etiqueta="Respuesta correcta"><select value={p.correcta} onChange={(e) => cambiar(i, "correcta", Number(e.target.value))}>
        {p.opciones.map((o, j) => <option value={j} key={j}>{o || `Opción ${j + 1}`}</option>)}
      </select></CampoPanel>
      <div className="s2-acciones"><button type="button" onClick={() => cambiar(i, "opciones", [...p.opciones, ""])}>Añadir opción</button>
        <button type="button" onClick={() => onChange(value.filter((_, n) => n !== i))}>Eliminar pregunta</button></div>
    </div>)}
    <button type="button" onClick={() => onChange([...value, { enunciado: "", opciones: ["", ""], correcta: 0 }])}>Añadir pregunta</button>
  </fieldset>;
}

function Segmentacion({ value = {}, onChange }) {
  const [texto, setTexto] = useState(() =>
    Object.fromEntries(["RANGO_EDAD", "TIPO_SOCIO", "PRODUCTO", "AGENCIA"].map((c) => [c, (value[c] || []).join(", ")]))
  );
  return <fieldset className="neg-seg"><legend>Público de la campaña</legend>
    <p className="neg-ayuda">Sin filtros, todos los socios activos pueden verla. Los filtros se combinan.</p>
    <div className="neg-seg__grid">
      {["RANGO_EDAD", "TIPO_SOCIO", "PRODUCTO", "AGENCIA"].map((c) => <CampoPanel etiqueta={etiqueta(c)} key={c}
        placeholder={c === "RANGO_EDAD" ? "Ej. 18, 35" : "Valores separados por comas"}
        value={texto[c] ?? ""} onChange={(e) => {
          const raw = e.target.value;
          setTexto((t) => ({ ...t, [c]: raw }));
          const v = { ...value };
          const partes = raw.split(",").map((x) => x.trim()).filter(Boolean);
          if (partes.length) {
            if (c === "RANGO_EDAD") {
              const nums = partes.map((x) => Number(x)).filter((n) => Number.isInteger(n));
              if (nums.length === 2) v[c] = nums;
              else delete v[c];
            } else {
              v[c] = partes;
            }
          } else {
            delete v[c];
          }
          onChange(v);
        }} />)}
    </div>
  </fieldset>;
}

function Formulario({ campos, inicial, guardar, cancelar, ocupado }) {
  const [datos, setDatos] = useState(inicial || {});
  function cambiar(nombre, valor) { setDatos((d) => ({ ...d, [nombre]: valor })); }
  async function enviar(e) {
    e.preventDefault(); const salida = {};
    for (const c of campos) {
      let v = datos[c.nombre];
      if (v === "" || v == null) { if (c.nulo) salida[c.nombre] = null; else if (c.tipo === "json") salida[c.nombre] = c.nombre === "preguntas" ? [] : {}; continue; }
      salida[c.nombre] = c.tipo === "number" && !c.decimal ? Number(v) : c.tipo === "boolean" ? Boolean(v) : v;
    }
    await guardar(salida);
  }
  return <form className="s2-form neg-form" onSubmit={enviar}>
    <div className="neg-form__grid">
      {campos.map((c) => c.nombre === "preguntas" ? <div key={c.nombre} className="neg-span-2"><BancoPreguntas value={datos[c.nombre] || []} onChange={(v) => cambiar(c.nombre, v)} /></div>
        : c.nombre === "segmentacion" ? <div key={c.nombre} className="neg-span-2"><Segmentacion value={datos[c.nombre] || {}} onChange={(v) => cambiar(c.nombre, v)} /></div>
          : <div key={c.nombre} className={c.tipo === "textarea" ? "neg-span-2" : ""}>
            <CampoPanel etiqueta={etiqueta(c.nombre)}>
              {c.opciones ? <select value={datos[c.nombre] ?? ""} required={c.requerido} onChange={(e) => cambiar(c.nombre, e.target.value)}>
                <option value="">Seleccionar</option>{c.opciones.map((o) => <option key={o.valor} value={o.valor}>{o.etiqueta}</option>)}
              </select> : c.tipo === "textarea" ? <textarea value={datos[c.nombre] ?? ""} required={c.requerido} onChange={(e) => cambiar(c.nombre, e.target.value)} />
                : c.tipo === "boolean" ? <label className="neg-check"><input type="checkbox" checked={Boolean(datos[c.nombre])} onChange={(e) => cambiar(c.nombre, e.target.checked)} /> Activo</label>
                  : <input type={c.tipo} step={c.decimal ? "any" : undefined} value={c.tipo === "datetime-local" ? (datos[c.nombre] || "").slice(0, 16) : datos[c.nombre] ?? ""}
                    required={c.requerido && !c.nulo} onChange={(e) => cambiar(c.nombre, e.target.value)} />}
            </CampoPanel>
          </div>)}
    </div>
    <div className="s2-acciones"><button className="boton boton--amarillo" disabled={ocupado}>Guardar</button>
      <button type="button" className="boton boton--claro" onClick={cancelar}>Cancelar</button></div>
  </form>;
}

const CAMBIOS = { campanas: { BORRADOR: ["ACTIVA"], ACTIVA: ["SUSPENDIDA", "FINALIZADA"], SUSPENDIDA: ["ACTIVA", "FINALIZADA"] },
  capacitaciones: { BORRADOR: ["PUBLICADA"], PUBLICADA: ["RETIRADA"], RETIRADA: ["PUBLICADA"] },
  talleres: { PROGRAMADO: ["REALIZADO", "CANCELADO"] }, juegos: { INACTIVO: ["ACTIVO"], ACTIVO: ["INACTIVO"] }, sorteos: { BORRADOR: ["ACTIVO"], ACTIVO: ["CANCELADO"] } };

export function Catalogo({ recurso }) {
  const r = useRecurso(`${BASE}${recurso}/`); const op = useOperacion(r.recargar);
  const [editor, setEditor] = useState(null); const [seleccion, setSeleccion] = useState(null);
  const [confirmacion, setConfirmacion] = useState(null); const [motivo, setMotivo] = useState("");
  const [resultado, setResultado] = useState(null);
  const gestion = r.datos?.puede_gestionar;
  async function guardar(datos) {
    // Los campos de campaña ya activa conservan los incentivos y la segmentación originales.
    const salida = recurso === "campanas" && editor.id && editor.estado !== "BORRADOR"
      ? Object.fromEntries(Object.entries(datos).filter(([k]) => ["nombre", "objetivo", "condiciones"].includes(k))) : datos;
    const ok = await op.ejecutar(() => editor.id ? api.putProtegido(`${BASE}${recurso}/${editor.id}/`, salida) : api.postProtegido(`${BASE}${recurso}/`, salida));
    if (ok) setEditor(null);
  }
  async function accion(item, nombre, datos = {}) {
    let respuesta;
    if (await op.ejecutar(async () => { respuesta = await api.postProtegido(`${BASE}${recurso}/${item.id}/${nombre}/`, datos); })) {
      if (nombre === "iniciar") setSeleccion({ ...respuesta, juego: item.nombre });
      if (nombre === "previsualizar") setResultado(`${respuesta.socios_elegibles} socios cumplen la segmentación y vigencia.`);
      setConfirmacion(null); setMotivo("");
    }
  }
  const catalogoFormacion = recurso === "capacitaciones" && !gestion;
  if (catalogoFormacion && seleccion?.aula) {
    return <Aula key={seleccion.aula} id={seleccion.aula} volver={() => setSeleccion(null)} />;
  }
  return <><TituloPagina titulo={TITULOS[recurso]} sub={catalogoFormacion
    ? "Elige una capacitación, completa sus módulos y rinde la evaluación."
    : undefined}>
    {gestion && <button className="boton" onClick={() => setEditor({})}>Crear {etiqueta(recurso.toLowerCase())}</button>}
  </TituloPagina>
    <Aviso error={r.error || op.error} mensaje={op.mensaje} />{resultado && <p role="status">{resultado}</p>}
    {editor && <Tarjeta titulo={editor.id ? "Editar" : "Nuevo registro"}><Formulario key={editor.id || "nuevo"}
      campos={r.datos.campos} inicial={editor} guardar={guardar} cancelar={() => setEditor(null)} ocupado={op.ocupado} /></Tarjeta>}
    {confirmacion && <Tarjeta titulo={catalogoFormacion ? "Confirmar inscripción" : "Confirmar operación"}><form className="s2-form" onSubmit={(e) => { e.preventDefault(); accion(confirmacion.item, confirmacion.accion,
      confirmacion.accion === "estado" ? { estado: confirmacion.estado, motivo } : confirmacion.accion === "canjear"
        ? { clave: confirmacion.clave, acepta_condiciones: true } : { acepta_requisitos: true }); }}>
      <p>{confirmacion.item.nombre || confirmacion.item.titulo}{!catalogoFormacion && `: ${etiqueta(confirmacion.estado || confirmacion.accion)}`}</p>
      <p>{confirmacion.item.condiciones || confirmacion.item.requisitos}</p>
      {confirmacion.accion === "estado" && <CampoPanel etiqueta="Motivo" value={motivo} required onChange={(e) => setMotivo(e.target.value)} />}
      {confirmacion.accion !== "estado" && <label><input type="checkbox" required /> He leído y acepto las condiciones y requisitos indicados.</label>}
      <div className="s2-acciones"><button className="boton" disabled={op.ocupado}>Confirmar</button><button className="boton boton--claro" type="button" onClick={() => setConfirmacion(null)}>Cancelar</button></div>
    </form></Tarjeta>}
    {!r.datos && !r.error && <p role="status">Cargando…</p>}
    {r.datos?.resultados.length === 0 && (catalogoFormacion
      ? <Tarjeta titulo="Aún no hay capacitaciones disponibles">Las nuevas capacitaciones aparecerán aquí cuando se publiquen.</Tarjeta>
      : <Tarjeta><p className="vacio">No hay registros disponibles.</p></Tarjeta>)}
    <div className={catalogoFormacion ? "formacion-catalogo" : "neg-rejilla"}>{r.datos?.resultados.map((item) => catalogoFormacion
      ? <article className="formacion-curso" key={item.id}>
        <header>
          {item.modalidad && <span className="formacion-estado">{etiqueta(item.modalidad.toLowerCase())}</span>}
          <h2>{item.titulo}</h2>
        </header>
        <div className="formacion-curso__contenido">
          {item.descripcion && <p>{item.descripcion}</p>}
          <dl>
            {item.duracion != null && <div><dt>Duración</dt><dd>{item.duracion} {item.duracion === 1 ? "hora" : "horas"}</dd></div>}
            {item.requisitos && <div><dt>Requisitos</dt><dd>{item.requisitos}</dd></div>}
          </dl>
          <div className="formacion-acciones">
            <button className="boton boton--amarillo" disabled={op.ocupado} onClick={() => setConfirmacion({ item, accion: "inscribir" })}>Inscribirme</button>
            <button className="boton boton--claro" onClick={() => { setConfirmacion(null); setSeleccion({ aula: item.id }); }}>Entrar al aula</button>
          </div>
        </div>
      </article>
      : <Tarjeta key={item.id} titulo={item.nombre || item.titulo || item.entidad || item.objetivo || item.concepto}>
      {item.estado && <p className="etiqueta">{etiqueta(item.estado)}</p>}{item.concepto && <p>{item.concepto} · {item.importe}</p>}
      {(item.descripcion || item.instrucciones || item.condiciones) && <p>{item.descripcion || item.instrucciones || item.condiciones}</p>}
      {item.descripcion && item.condiciones && <p>{item.condiciones}</p>}
      {item.entidad_convenio && <p>Convenio: {item.entidad_convenio}</p>}
      {item.intentos_restantes != null && <p>Intentos disponibles: {item.intentos_restantes}</p>}
      {item.avance != null && <p>Avance: {item.avance} de {item.meta}{item.completado ? " · Completado" : ""}</p>}
      {recurso === "capacitaciones" && item.requisitos && <p><strong>Requisitos</strong> {item.requisitos}</p>}
      <dl className="neg-datos">{["id", "inicio", "fin", "desde", "hasta", "vigencia", "fecha", "costo_puntos", "stock", "umbral_puntos", "modalidad", "duracion", "lugar", "premio", "meta", "incentivos", "criterio", "umbral"]
        .filter((campo) => item[campo] != null && (gestion || campo !== "id"))
        .map((campo) => <div key={campo}><dt>{ETIQUETAS_DATOS[campo] || etiqueta(campo)}</dt><dd>{String(item[campo])}</dd></div>)}</dl>
      {item.indicadores && <dl className="neg-datos">{Object.entries(item.indicadores).map(([k, v]) => <div key={k}><dt>{etiqueta(k)}</dt><dd>{v}</dd></div>)}</dl>}
      {item.evidencia?.sha256 && <dl className="neg-datos">
        <div><dt>Participantes elegibles</dt><dd>{item.evidencia.elegibles?.length ?? 0}</dd></div>
        <div><dt>Hash lista congelada</dt><dd><code>{item.evidencia.sha256}</code></dd></div>
      </dl>}
      {!!item.ganadores?.length && <ol>{item.ganadores.map((g) => <li key={g.posicion}>{g.alias}{g.suplente ? " (suplente)" : ""}</li>)}</ol>}
      <div className="s2-acciones">
        {gestion && <button className="boton boton--claro neg-btn" onClick={() => setEditor(item)}>Editar</button>}
        {gestion && (CAMBIOS[recurso]?.[item.estado] || []).map((estado) => <button className="boton boton--claro neg-btn" key={estado} disabled={op.ocupado}
          onClick={() => setConfirmacion({ item, estado, accion: "estado" })}>{etiqueta(estado)}</button>)}
        {gestion && recurso === "campanas" && <button className="boton boton--claro neg-btn" onClick={() => accion(item, "previsualizar")}>Previsualizar público</button>}
        {gestion && recurso === "sorteos" && item.estado === "ACTIVO" && <button className="boton boton--amarillo neg-btn" onClick={() => accion(item, "ejecutar")}>Ejecutar sorteo</button>}
        {gestion && ["capacitaciones", "talleres"].includes(recurso) && <button className="boton boton--claro neg-btn" onClick={() => setSeleccion({ participantes: item.id })}>Ver participantes</button>}
        {!gestion && recurso === "beneficios" && <button className="boton boton--amarillo neg-btn" disabled={op.ocupado} onClick={() => setConfirmacion({ item, accion: "canjear", clave: crypto.randomUUID() })}>Solicitar canje</button>}
        {!gestion && recurso === "talleres" && <button className="boton boton--amarillo neg-btn" disabled={op.ocupado} onClick={() => setConfirmacion({ item, accion: "inscribir" })}>Inscribirme</button>}
        {!gestion && recurso === "juegos" && <button className="boton boton--amarillo neg-btn" disabled={op.ocupado || item.intentos_restantes === 0 || Boolean(seleccion?.preguntas)} onClick={() => accion(item, "iniciar")}>Iniciar partida</button>}
      </div>
    </Tarjeta>)}</div>
    {seleccion?.preguntas && <Cuestionario titulo={seleccion.juego} tipo={seleccion.tipo} preguntas={seleccion.preguntas} enviar={async (respuestas) => {
      let respuesta; if (await op.ejecutar(async () => { respuesta = await api.postProtegido(`${BASE}partidas/${seleccion.id}/finalizar/`, { respuestas }); })) {
        setResultado(`Puntuación: ${respuesta.puntuacion} / 100`); setSeleccion(null);
      }
    }} ocupado={op.ocupado} />}
    {seleccion?.participantes && <Participantes recurso={recurso} id={seleccion.participantes} />}
  </>;
}

export function Cuestionario({ titulo, tipo, preguntas, enviar, ocupado }) {
  const [respuestas, setRespuestas] = useState({});
  return <Tarjeta titulo={titulo || "Evaluación"}><form className="s2-form" onSubmit={(e) => { e.preventDefault(); enviar(preguntas.map((_, i) => respuestas[i])); }}>
    {preguntas.map((p, i) => <fieldset key={i}><legend>{i + 1}. {p.enunciado}</legend>{tipo === "EMPAREJAR"
      ? <select required aria-label={p.enunciado} value={respuestas[i] ?? ""} onChange={(e) => setRespuestas((d) => ({ ...d, [i]: Number(e.target.value) }))}>
        <option value="">Selecciona el concepto correspondiente</option>{p.opciones.map((o, j) => <option key={j} value={j}>{o}</option>)}</select>
      : p.opciones.map((o, j) =>
      <label className="neg-respuesta" key={j}><input type="radio" name={`pregunta-${i}`} required checked={respuestas[i] === j}
        onChange={() => setRespuestas((d) => ({ ...d, [i]: j }))} />{o}</label>)}</fieldset>)}
    <button className="boton" disabled={ocupado}>Enviar respuestas</button>
  </form></Tarjeta>;
}

function Aula({ id, volver }) {
  const r = useRecurso(`${BASE}capacitaciones/${id}/aula/`); const op = useOperacion(r.recargar); const [resultado, setResultado] = useState("");
  const aula = r.datos;
  return <div className="formacion-aula">
    <button className="boton boton--claro formacion-volver" autoFocus onClick={volver}>← Volver a capacitaciones</button>
    <TituloPagina titulo={aula?.titulo || "Aula de capacitación"} />
    <Aviso error={r.error || op.error} mensaje={resultado || op.mensaje} />
    {!aula && !r.error && <p role="status">Cargando aula…</p>}
    {aula && <>
      <div className="formacion-aula__rejilla">
        <Tarjeta titulo="Módulos">
          <ol className="formacion-modulos">{aula.modulos.map((unidad) => <li key={unidad.id}>
            <div className="formacion-modulos__cabecera">
              <h3>{unidad.titulo}</h3>
              {unidad.completado && <span className="formacion-estado formacion-estado--listo">Completado</span>}
            </div>
            <div className="formacion-acciones">
              {unidad.materiales.map((archivo) => <button className="boton boton--claro" key={archivo.id} disabled={op.ocupado}
                onClick={() => op.ejecutar(() => descargar(`/plataforma/materiales/${archivo.id}/archivo/`, archivo.titulo), "Descarga preparada.")}>{archivo.titulo}</button>)}
              {!unidad.completado && <button className="boton" disabled={op.ocupado}
                onClick={() => op.ejecutar(() => api.postProtegido(`${BASE}capacitaciones/${id}/progreso/`, { unidad: unidad.id }))}>Marcar como completado</button>}
            </div>
          </li>)}</ol>
        </Tarjeta>
        <Tarjeta titulo="Tu avance">
          <p className="formacion-porcentaje">{aula.porcentaje_avance} %</p>
          <progress aria-label="Avance de la capacitación" value={aula.porcentaje_avance} max={100} />
          <dl className="formacion-evaluacion">
            <div><dt>Intentos disponibles</dt><dd>{aula.intentos_restantes}</dd></div>
            <div><dt>Nota mínima</dt><dd>{aula.nota_minima}</dd></div>
          </dl>
          {aula.estado === "APROBADO" && <p className="formacion-estado formacion-estado--listo">Capacitación aprobada</p>}
          {aula.porcentaje_avance < 100 && <p>Completa todos los módulos para rendir la evaluación.</p>}
          {aula.estado !== "APROBADO" && aula.porcentaje_avance === 100 && aula.intentos_restantes === 0 && <p>Agotaste los intentos de la evaluación.</p>}
        </Tarjeta>
      </div>
      {aula.porcentaje_avance === 100 && aula.estado !== "APROBADO" && aula.intentos_restantes > 0 && <Cuestionario preguntas={aula.preguntas} ocupado={op.ocupado} enviar={async (respuestas) => {
        await op.ejecutar(async () => { const x = await api.postProtegido(`${BASE}capacitaciones/${id}/evaluar/`, { respuestas }); setResultado(`Nota: ${x.nota}. ${x.aprobado ? "Aprobaste; tu certificado está disponible en Mis actividades." : "No aprobaste este intento."}`); });
      }} />}
    </>}
  </div>;
}

function Participantes({ recurso, id }) {
  const r = useRecurso(`${BASE}${recurso}/${id}/participantes/`); const op = useOperacion(r.recargar);
  return <Tarjeta titulo="Participantes"><Aviso error={r.error || op.error} mensaje={op.mensaje} />
    {r.datos && (recurso === "capacitaciones"
      ? <Tabla filas={r.datos.resultados} columnas={["nombre", "estado", "porcentaje_avance", "intentos", "nota_maxima"]} />
      : r.datos.resultados.map((p) => <p key={p.id}>{p.nombre} · {p.asistio ? "Asistencia validada" : "Inscrito"}
        {!p.asistio && <button disabled={op.ocupado} onClick={() => op.ejecutar(() => api.postProtegido(`${BASE}asistencias/${p.id}/confirmar/`, {}))}>Validar asistencia</button>}</p>))}
  </Tarjeta>;
}

export function Puntos() {
  const r = useRecurso(`${BASE}puntos/`);
  return <><TituloPagina titulo="Mis puntos y logros" /><Aviso error={r.error} />{r.datos && <>
    <Tarjeta titulo={`${r.datos.saldo} puntos disponibles`}><p>Nivel: {r.datos.nivel}</p><p>Puntos acumulados para logros: {r.datos.puntos_logro}</p>
      {r.datos.saldo === 0 && r.datos.movimientos.length === 0 && <p>Aún no tienes puntos acumulados. Participa en referidos, capacitaciones, talleres, juegos o retos para ganar puntos.</p>}
      <p>{r.datos.insignias.map((i) => i.nombre).join(" · ") || "Tus próximas actividades te acercarán a nuevas insignias."}</p></Tarjeta>
    <Tarjeta titulo="Movimientos"><Tabla filas={r.datos.movimientos} columnas={["fecha", "tipo", "cantidad", "origen_tipo", "origen_id", "motivo"]} /></Tarjeta>
  </>}</>;
}

export function Tabla({ filas = [], columnas }) {
  if (!filas.length) return <p>No hay registros para mostrar.</p>;
  return <div className="neg-tabla"><table><thead><tr>{columnas.map((c) => <th key={c}>{etiqueta(c)}</th>)}</tr></thead>
    <tbody>{filas.map((f, i) => <tr key={f.id ?? i}>{columnas.map((c) => <td key={c}>{typeof f[c] === "boolean" ? (f[c] ? "Sí" : "No") : String(f[c] ?? "—")}</td>)}</tr>)}</tbody></table></div>;
}

export function Canjes() {
  const [estadoFiltro, setEstadoFiltro] = useState("");
  const r = useRecurso(`${BASE}canjes/${estadoFiltro ? `?estado=${estadoFiltro}` : ""}`); const op = useOperacion(r.recargar); const [decision, setDecision] = useState(null); const [motivo, setMotivo] = useState("");
  return <><TituloPagina titulo="Solicitudes de canje" /><Aviso error={r.error || op.error} mensaje={op.mensaje} />
    <CampoPanel etiqueta="Filtrar por estado"><select value={estadoFiltro} onChange={(e) => setEstadoFiltro(e.target.value)}><option value="">Todos</option>
      {["PENDIENTE", "APROBADA", "RECHAZADA", "ENTREGADA"].map((v) => <option key={v}>{v}</option>)}</select></CampoPanel>
    <Tabla filas={r.datos?.resultados} columnas={["id", "beneficio", "puntos", "estado", "fecha", "entrega"]} />
    {r.datos?.puede_gestionar && r.datos.resultados.map((c) => <div className="s2-acciones" key={c.id}><span>Solicitud {c.id}</span>
      {(c.estado === "PENDIENTE" ? ["APROBADA", "RECHAZADA"] : c.estado === "APROBADA" ? ["ENTREGADA"] : []).map((estado) =>
        <button key={estado} onClick={() => setDecision({ id: c.id, estado })}>{etiqueta(estado)}</button>)}</div>)}
    {decision && <form className="s2-form" onSubmit={async (e) => { e.preventDefault(); if (await op.ejecutar(() => api.postProtegido(`${BASE}canjes/${decision.id}/estado/`, { estado: decision.estado, motivo }))) { setDecision(null); setMotivo(""); } }}>
      <h3>{etiqueta(decision.estado)} solicitud {decision.id}</h3><CampoPanel etiqueta="Motivo o constancia de entrega" value={motivo} required onChange={(e) => setMotivo(e.target.value)} />
      <button disabled={op.ocupado} className="boton">Confirmar</button><button type="button" onClick={() => setDecision(null)}>Cancelar</button></form>}
  </>;
}

export function FormReferido({ codigo, publico = false, terminado, campanas = [] }) {
  const op = useOperacion(); const [datos, setDatos] = useState({ nombre: "", cedula: "", correo: "", telefono: "", producto: "", acepta_terminos: false });
  const cambiar = (k, v) => setDatos((d) => ({ ...d, [k]: v }));
  if (publico && op.mensaje) return <Aviso mensaje={op.mensaje} />;
  return <form className="s2-form referido-form" onSubmit={async (e) => { e.preventDefault(); const salida = { ...datos, codigo }; if (!salida.correo) delete salida.correo; if (!salida.telefono) delete salida.telefono;
    if (salida.campana) salida.campana = Number(salida.campana); else delete salida.campana;
    const ok = await op.ejecutar(() => publico ? api.post(`/plataforma/invitaciones/${encodeURIComponent(codigo)}/referir/`, salida) : api.postProtegido(`${BASE}referidos/`, salida),
      publico
        ? (salida.correo ? "Solicitud registrada. Cuando recibas el correo de confirmación, abre el enlace y autoriza el contacto."
          : "Solicitud registrada. La cooperativa requiere tu confirmación antes de iniciar el seguimiento.")
        : "Solicitud registrada. La persona invitada debe confirmar el contacto."); if (ok) terminado?.(); }}>
    <div className="s2-form referido-form__campos">
    {[['nombre', 'Nombres completos'], ['cedula', 'Cédula de diez dígitos'], ['correo', 'Correo electrónico'], ['telefono', 'Teléfono'], ['producto', 'Producto de interés']].map(([k, titulo]) =>
      <CampoPanel key={k} etiqueta={titulo} value={datos[k]} required={["nombre", "cedula", "producto"].includes(k)}
        type={k === "correo" ? "email" : k === "telefono" ? "tel" : "text"}
        inputMode={k === "cedula" ? "numeric" : undefined} pattern={k === "cedula" ? "[0-9]{10}" : undefined} onChange={(e) => cambiar(k, e.target.value)} />)}
    </div>
    {!!campanas.length && <CampoPanel etiqueta="Campaña de la referencia"><select value={datos.campana || ""} onChange={(e) => cambiar("campana", e.target.value)}>
      <option value="">Sin campaña específica</option>{campanas.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}</select></CampoPanel>}
    {publico && <p>Indica al menos un correo electrónico o un teléfono. Si indicas un correo, allí se enviará el enlace de confirmación.</p>}
    <label className="referido-form__consentimiento"><input type="checkbox" required checked={datos.acepta_terminos} onChange={(e) => cambiar("acepta_terminos", e.target.checked)} />
      <span>Autorizo el tratamiento de estos datos para gestionar esta referencia según la política 1.0. El titular confirmará el contacto antes del seguimiento.</span></label>
    <Aviso {...op} /><button className="boton" disabled={op.ocupado}>Registrar referencia</button>
  </form>;
}

export function Referidos({ socio = false }) {
  const [filtros, setFiltros] = useState({ estado: "", campana: "", socio: "", desde: "", hasta: "" }); const [consulta, setConsulta] = useState("");
  const r = useRecurso(`${BASE}referidos/${consulta}`); const codigo = useRecurso(socio ? "/plataforma/referidos/codigo/" : `${BASE}referidos/`);
  const campanas = useRecurso(`${BASE}campanas/`);
  const op = useOperacion(r.recargar); const [seleccion, setSeleccion] = useState(null); const [motivo, setMotivo] = useState(""); const [evento, setEvento] = useState("APERTURA_CUENTA"); const [monto, setMonto] = useState("");
  const seguimiento = <>{!socio && <TituloPagina titulo="Seguimiento comercial" />}<Aviso error={r.error || op.error} mensaje={op.mensaje} />
    {socio && codigo.datos?.codigo && <Tarjeta titulo="Registrar una referencia"><FormReferido codigo={codigo.datos.codigo} terminado={r.recargar} campanas={campanas.datos?.resultados || []} /></Tarjeta>}
    <form className="s2-form" onSubmit={(e) => { e.preventDefault(); setConsulta(`?${new URLSearchParams(Object.entries(filtros).filter(([, v]) => v))}`); }}>
      <CampoPanel etiqueta="Estado de referencia"><select value={filtros.estado} onChange={(e) => setFiltros({ ...filtros, estado: e.target.value })}><option value="">Todos</option>
        {["REGISTRADO", "CONFIRMADO", "EN_SEGUIMIENTO", "CONVERTIDO", "RECHAZADO", "EXPIRADO"].map((v) => <option key={v}>{v}</option>)}</select></CampoPanel>
      <CampoPanel etiqueta="Campaña"><select value={filtros.campana} onChange={(e) => setFiltros({ ...filtros, campana: e.target.value })}><option value="">Todas</option>
        {campanas.datos?.resultados.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}</select></CampoPanel>
      <CampoPanel etiqueta="Registrado desde" type="date" value={filtros.desde} onChange={(e) => setFiltros({ ...filtros, desde: e.target.value })} />
      {r.datos?.puede_gestionar && <CampoPanel etiqueta="Socio referente, identificador" type="number" min="1" value={filtros.socio} onChange={(e) => setFiltros({ ...filtros, socio: e.target.value })} />}
      <CampoPanel etiqueta="Registrado hasta" type="date" value={filtros.hasta} onChange={(e) => setFiltros({ ...filtros, hasta: e.target.value })} /><button>Aplicar filtros</button>
    </form>
    <Tabla filas={r.datos?.resultados} columnas={["id", "nombre", "contacto", "producto", "estado", "creado_en"]} />
    {r.datos?.puede_gestionar && r.datos.resultados.map((p) => <div className="s2-acciones" key={p.id}><span>Referencia {p.id}</span>
      {(p.estado === "CONFIRMADO" ? ["EN_SEGUIMIENTO", "RECHAZADO"] : p.estado === "EN_SEGUIMIENTO" ? ["CONVERTIDO", "RECHAZADO"] : p.estado === "REGISTRADO" ? ["EXPIRADO"] : []).map((estado) =>
        <button key={estado} onClick={() => setSeleccion({ id: p.id, estado })}>{etiqueta(estado)}</button>)}</div>)}
    {seleccion && <form className="s2-form" onSubmit={async (e) => { e.preventDefault(); const d = { estado: seleccion.estado, motivo }; if (seleccion.estado === "CONVERTIDO") d.tipo_evento = evento;
      if (seleccion.estado === "CONVERTIDO" && monto !== "") d.monto_captado = monto;
      if (await op.ejecutar(() => api.postProtegido(`${BASE}referidos/${seleccion.id}/estado/`, d))) setSeleccion(null); }}>
      <h3>{etiqueta(seleccion.estado)} referencia {seleccion.id}</h3><CampoPanel etiqueta="Motivo" value={motivo} required onChange={(e) => setMotivo(e.target.value)} />
      {seleccion.estado === "CONVERTIDO" && <CampoPanel etiqueta="Evento comercial"><select value={evento} onChange={(e) => setEvento(e.target.value)}>
        <option value="APERTURA_CUENTA">Apertura de cuenta validada</option><option value="PRODUCTO_CREDITICIO">Producto crediticio validado</option>
        <option value="TARJETA_ENTREGADA">Tarjeta entregada</option><option value="SEGURO_CONTRATADO">Seguro contratado</option></select></CampoPanel>}
      {seleccion.estado === "CONVERTIDO" && <CampoPanel etiqueta="Monto captado confirmado, opcional" type="number" min="0" step="0.01" value={monto} onChange={(e) => setMonto(e.target.value)} />}
      <button className="boton" disabled={op.ocupado}>Confirmar</button><button type="button" onClick={() => setSeleccion(null)}>Cancelar</button>
    </form>}
  </>;
  return socio ? <VistaReferidos>{seguimiento}</VistaReferidos> : seguimiento;
}

export function Actividades() {
  const r = useRecurso(`${BASE}mis-actividades/`); const op = useOperacion();
  return <><TituloPagina titulo="Mis actividades y certificados" /><Aviso error={r.error || op.error} mensaje={op.mensaje} />{r.datos && <>
    <Tarjeta titulo="Capacitaciones"><Tabla filas={r.datos.inscripciones} columnas={["titulo", "estado"]} /></Tarjeta>
    <Tarjeta titulo="Certificados">{r.datos.certificados.map((c) => <p key={c.id}>{c.titulo} <button onClick={() => op.ejecutar(() => descargar(`${BASE}certificados/${c.id}/pdf/`, `certificado-${c.id}`))}>Descargar PDF</button></p>)}</Tarjeta>
    <Tarjeta titulo="Talleres"><Tabla filas={r.datos.talleres} columnas={["titulo", "asistio"]} /></Tarjeta>
    <Tarjeta titulo="Resultados de juegos"><Tabla filas={r.datos.partidas} columnas={["juego", "puntuacion", "fecha"]} /></Tarjeta>
    <Tarjeta titulo="Progreso de retos"><Tabla filas={r.datos.retos} columnas={["objetivo", "avance", "meta", "completado_en"]} /></Tarjeta>
  </>}</>;
}

export function Reportes({ area }) {
  const [tipo, setTipo] = useState(area === "marketing" ? "referidos" : area === "rse" ? "social" : "general");
  const [desde, setDesde] = useState(""); const [hasta, setHasta] = useState("");
  const [campana, setCampana] = useState(""); const [segmento, setSegmento] = useState("");
  const [filtros, setFiltros] = useState({});
  const parametros = new URLSearchParams({ tipo });
  for (const [clave, valor] of Object.entries(filtros)) {
    if (valor && (tipo === "referidos" || clave === "desde" || clave === "hasta")) parametros.set(clave, valor);
  }
  const ruta = `${BASE}reportes/?${parametros}`; const r = useRecurso(ruta); const op = useOperacion();
  return <><TituloPagina titulo="Reportes y estadísticas" /><Aviso error={r.error || op.error} mensaje={op.mensaje} />
    <form className="s2-form" onSubmit={(e) => { e.preventDefault(); setFiltros({ desde, hasta, campana, segmento }); }}>
      {area === "admin" && <CampoPanel etiqueta="Reporte"><select value={tipo} onChange={(e) => setTipo(e.target.value)}>{["general", "referidos", "social", "gamificacion"].map((v) => <option key={v} value={v}>{etiqueta(v)}</option>)}</select></CampoPanel>}
      <CampoPanel etiqueta="Desde" type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
      <CampoPanel etiqueta="Hasta" type="date" value={hasta} min={desde || undefined} onChange={(e) => setHasta(e.target.value)} />
      {tipo === "referidos" && <>
        <CampoPanel etiqueta="Identificador de campaña" type="number" min="1" value={campana} onChange={(e) => setCampana(e.target.value)} />
        <CampoPanel etiqueta="Criterio de segmentación"><select value={segmento} onChange={(e) => setSegmento(e.target.value)}>
          <option value="">Todos</option>
          <option value="AGENCIA">Agencia</option>
          <option value="TIPO_SOCIO">Tipo de socio</option>
          <option value="PRODUCTO">Producto</option>
          <option value="RANGO_EDAD">Rango de edad</option>
        </select></CampoPanel>
      </>}
      <button className="boton">{tipo === "referidos" ? "Aplicar filtros" : "Aplicar período"}</button>
    </form>
    <Tabla filas={r.datos?.resultados} columnas={["indicador", "valor"]} />
    {r.datos && <section className="neg-grafico" aria-label="Gráfico de actividad"><h2>Volumen de actividad</h2>
      {r.datos.resultados.filter((f) => ["Usuarios activos", "Referidos", "Conversiones", "Inscritos", "Aprobados", "Certificados", "Sorteos ejecutados"].includes(f.indicador)).map((f) => <label key={f.indicador}>{f.indicador}: {String(f.valor)}
        <progress value={Number(f.valor)} max={Math.max(1, ...r.datos.resultados.filter((x) => ["Usuarios activos", "Referidos", "Conversiones", "Inscritos", "Aprobados", "Certificados", "Sorteos ejecutados"].includes(x.indicador)).map((x) => Number(x.valor)))} /></label>)}
    </section>}
    <div className="s2-acciones">{["csv", "pdf"].map((formato) => <button key={formato} disabled={op.ocupado} onClick={() => op.ejecutar(() => descargar(`${ruta}&formato=${formato}`, `reporte-${tipo}${formato === "csv" ? ".csv" : ""}`))}>Descargar {formato.toUpperCase()}</button>)}</div>
    {r.datos && <><p>Generado: {r.datos.generado_en}</p>
      <dl className="neg-datos">{Object.entries(r.datos.filtros || {}).map(([clave, valor]) => <div key={clave}>
        <dt>{etiqueta(clave)}</dt><dd>{etiqueta(valor)}</dd>
      </div>)}</dl>
    </>}
  </>;
}
