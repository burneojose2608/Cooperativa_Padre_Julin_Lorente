import { useEffect, useState } from "react";
import { convertirCuentaASocio, listarCuentasGenerales } from "../api/administracion";
import { Modal, Tarjeta, TituloPagina } from "./ui";

const ESTADO_PADRON = { activo: "Activo", inactivo: "Inactivo", no_encontrado: "Sin validar" };

export default function ValidarSocios() {
  const [busqueda, setBusqueda] = useState("");
  const [filtro, setFiltro] = useState("");
  const [pagina, setPagina] = useState(1);
  const [revision, setRevision] = useState(0);
  const [datos, setDatos] = useState({ results: [], count: 0 });
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [aviso, setAviso] = useState("");
  const [seleccion, setSeleccion] = useState(null);
  const [confirmado, setConfirmado] = useState(false);
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    let vigente = true;
    listarCuentasGenerales(filtro, pagina)
      .then((respuesta) => { if (vigente) setDatos(respuesta); })
      .catch((err) => { if (vigente) setError(err.message); })
      .finally(() => { if (vigente) setCargando(false); });
    return () => { vigente = false; };
  }, [filtro, pagina, revision]);

  function buscar(e) {
    e.preventDefault();
    setCargando(true);
    setError("");
    setPagina(1);
    setFiltro(busqueda.trim());
    setRevision((r) => r + 1);
  }

  function cambiarPagina(nuevaPagina) {
    setCargando(true);
    setError("");
    setPagina(nuevaPagina);
  }

  async function convertir(e) {
    e.preventDefault();
    if (!confirmado || guardando || !seleccion) return;
    setGuardando(true);
    setError("");
    try {
      const resultado = await convertirCuentaASocio(seleccion.id);
      setAviso(`${seleccion.username}: ${resultado.mensaje} Código: ${resultado.codigo_socio}.`);
      setSeleccion(null);
      setCargando(true);
      setPagina(1);
      setRevision((r) => r + 1);
    } catch (err) {
      setError(err.message);
    } finally {
      setGuardando(false);
    }
  }

  return (
    <>
      <TituloPagina titulo="Validar socios" sub="Proceso temporal de validación manual de cuentas generales." />
      <p>Confirma la condición de socio activo antes de habilitar sus funciones. La conversión conserva el usuario y la contraseña.</p>
      {aviso && <p role="status">{aviso}</p>}
      {!seleccion && error && <div className="alerta alerta--error" role="alert">{error}</div>}
      <Tarjeta>
        <form className="form-modal" onSubmit={buscar}>
          <label>Buscar por usuario, nombre o cédula
            <input value={busqueda} onChange={(e) => setBusqueda(e.target.value)} maxLength={100} />
          </label>
          <button className="boton boton--azul" type="submit" disabled={cargando}>Buscar</button>
        </form>
        {cargando ? <p role="status">Cargando cuentas…</p> : !error && (
          <>
            <div className="tabla-caja"><table className="tabla">
              <thead><tr><th>Persona</th><th>Usuario</th><th>Cédula</th><th>Cuenta</th><th>Padrón</th><th>Acción</th></tr></thead>
              <tbody>{datos.results.map((cuenta) => (
                <tr key={cuenta.id}>
                  <td>{cuenta.nombre} {cuenta.apellido}</td><td>{cuenta.username}</td><td>{cuenta.cedula}</td>
                  <td>{cuenta.estado === "ACTIVA" ? "Activa" : cuenta.estado}</td>
                  <td>{ESTADO_PADRON[cuenta.estado_padron]}</td>
                  <td><button className="boton boton--azul" disabled={cuenta.estado !== "ACTIVA" || cuenta.estado_padron === "inactivo"}
                    onClick={() => { setSeleccion(cuenta); setConfirmado(false); setError(""); }}>Revisar y convertir</button></td>
                </tr>
              ))}</tbody>
            </table></div>
            {!datos.results.length && <p className="vacio">No hay cuentas generales que coincidan con la búsqueda.</p>}
            <p>{datos.count} cuentas · Página {pagina}</p>
            <button className="boton boton--claro" disabled={!datos.previous} onClick={() => cambiarPagina(pagina - 1)}>Anterior</button>{" "}
            <button className="boton boton--claro" disabled={!datos.next} onClick={() => cambiarPagina(pagina + 1)}>Siguiente</button>
          </>
        )}
      </Tarjeta>
      {seleccion && <Modal titulo="Confirmar condición de socio" alCerrar={() => { if (!guardando) setSeleccion(null); }}>
        <form className="form-modal" onSubmit={convertir}>
          <p><strong>{seleccion.nombre} {seleccion.apellido}</strong> · {seleccion.username}</p>
          <p>Cédula: {seleccion.cedula}</p>
          <p>Esta aprobación temporal registrará su condición activa en el padrón y habilitará las funciones de socio. Quedará registrada en auditoría.</p>
          <label className="check"><input type="checkbox" checked={confirmado} disabled={guardando} onChange={(e) => setConfirmado(e.target.checked)} />
            <span>Confirmo que revisé esta cuenta y que la persona es socia activa.</span></label>
          {error && <div className="alerta alerta--error" role="alert">{error}</div>}
          <button className="boton boton--azul" type="submit" disabled={!confirmado || guardando}>
            {guardando ? "Convirtiendo…" : "Validar y convertir a socio"}
          </button>
        </form>
      </Modal>}
    </>
  );
}
