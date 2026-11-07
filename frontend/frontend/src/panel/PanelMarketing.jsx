import { useState } from "react";
import { marketingDemo } from "../datos/demo";
import { PIBorrar, PICampanas, PIEditar, PIMas, PIPuntos, PIReferidos, PISorteos } from "./IconosPanel";
import { Barras, Estado, Kpi, Modal, Proximamente, Tarjeta, TituloPagina } from "./ui";

function Inicio() {
  const k = marketingDemo.kpis;
  return (
    <>
      <TituloPagina titulo="Inicio · Marketing" sub="Resumen del programa de referidos." />
      <div className="kpis">
        <Kpi icono={PIReferidos} valor={k.referidos} etiqueta="Referidos" />
        <Kpi icono={PIPuntos} valor={k.puntos} etiqueta="Puntos otorgados" tono="amarillo" />
        <Kpi icono={PICampanas} valor={k.campanas} etiqueta="Campañas" />
        <Kpi icono={PISorteos} valor={k.canjes} etiqueta="Canjes" tono="rojo" />
      </div>
      <Tarjeta titulo="Referidos por campaña"><Barras datos={marketingDemo.porCampana} /></Tarjeta>
    </>
  );
}

const hoy = () => new Date().toISOString().slice(0, 10);
const fmt = (iso) => iso.split("-").reverse().join("/");

function Campanas() {
  const [lista, setLista] = useState(marketingDemo.campanas);
  const [abierto, setAbierto] = useState(false);
  const [f, setF] = useState({ nombre: "", inicio: hoy(), fin: hoy() });
  const guardar = (e) => { e.preventDefault();
    const estado = f.inicio > hoy() ? "Programada" : "Activa";
    setLista([{ id: Date.now(), nombre: f.nombre.trim(), estado, inicio: fmt(f.inicio), fin: fmt(f.fin) }, ...lista]);
    setAbierto(false); setF({ nombre: "", inicio: hoy(), fin: hoy() }); };
  const alternar = (id) => setLista(lista.map((c) => c.id === id && c.estado !== "Finalizada"
    ? { ...c, estado: c.estado === "Activa" ? "Programada" : "Activa" } : c));
  return (
    <>
      <TituloPagina titulo="Gestión de campañas" sub="Crea, activa o pausa las campañas.">
        <button className="boton boton--amarillo" onClick={() => setAbierto(true)}><PIMas className="boton__ico" />Nueva campaña</button>
      </TituloPagina>
      <Tarjeta>
        <div className="tabla-caja"><table className="tabla">
          <thead><tr><th>Campaña</th><th>Estado</th><th>Inicio</th><th>Fin</th><th className="der">Acciones</th></tr></thead>
          <tbody>{lista.map((c) => (
            <tr key={c.id}><td>{c.nombre}</td><td><Estado texto={c.estado} /></td><td>{c.inicio}</td><td>{c.fin}</td>
              <td className="der acciones">
                <button className="icono-btn" aria-label={`Activar o pausar ${c.nombre}`} title="Activar / pausar" onClick={() => alternar(c.id)}><PIEditar /></button>
                <button className="icono-btn icono-btn--rojo" aria-label={`Eliminar ${c.nombre}`} onClick={() => setLista(lista.filter((x) => x.id !== c.id))}><PIBorrar /></button>
              </td></tr>))}</tbody>
        </table></div>
      </Tarjeta>
      {abierto && (
        <Modal titulo="Nueva campaña" alCerrar={() => setAbierto(false)}>
          <form className="form-modal" onSubmit={guardar}>
            <label>Nombre<input value={f.nombre} onChange={(e) => setF({ ...f, nombre: e.target.value })} required autoFocus /></label>
            <div className="dos"><label>Inicio<input type="date" value={f.inicio} onChange={(e) => setF({ ...f, inicio: e.target.value })} required /></label>
              <label>Fin<input type="date" min={f.inicio} value={f.fin} onChange={(e) => setF({ ...f, fin: e.target.value })} required /></label></div>
            <button className="boton boton--azul" type="submit">Crear campaña</button>
          </form>
        </Modal>
      )}
    </>
  );
}

export const RUTAS_MARKETING = {
  "": <Inicio />, campanas: <Campanas />,
  referidos: <Proximamente titulo="Referidos" />, contenidos: <Proximamente titulo="Contenidos" />,
  sorteos: <Proximamente titulo="Sorteos" />, beneficios: <Proximamente titulo="Beneficios" />, reportes: <Proximamente titulo="Reportes" />,
};
