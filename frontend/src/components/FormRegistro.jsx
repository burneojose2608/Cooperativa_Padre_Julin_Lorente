import { useState } from "react";
import { registrar } from "../api/auth";
import { cedulaValida, claveValida, correoValido, fechaNacimientoValida, telefonoValido, usernameValido } from "../utils/validaciones";
import { Link } from "react-router-dom";
import Campo from "./Campo";
import { IcoArroba, IcoCalendario, IcoCandado, IcoCedula, IcoCorreo, IcoFlecha, IcoPersona, IcoTelefono } from "./Iconos";

const CAMPOS_VISIBLES = ["nombre", "apellido", "cedula", "username", "correo", "telefono",
                         "fecha_nacimiento", "clave", "acepta_terminos"];
const VACIO = { nombre: "", apellido: "", cedula: "", username: "", correo: "", telefono: "",
                fecha_nacimiento: "", clave: "", acepta_terminos: false };

function validar(d) {
  const e = {};
  if (!d.nombre.trim()) e.nombre = "Ingresa tus nombres.";
  if (!d.apellido.trim()) e.apellido = "Ingresa tus apellidos.";
  if (!cedulaValida(d.cedula.trim())) e.cedula = "Ingresa exactamente 10 dígitos, del 0 al 9.";
  if (!usernameValido(d.username.trim())) e.username = "Usuario de 4 a 50 caracteres: letras, números, punto o guion bajo.";
  if (!correoValido(d.correo.trim())) e.correo = "Ingresa un correo válido.";
  if (!telefonoValido(d.telefono.trim())) e.telefono = "Usa solo números (7 a 15 dígitos).";
  if (!fechaNacimientoValida(d.fecha_nacimiento)) e.fecha_nacimiento = "Ingresa una fecha de nacimiento válida.";
  if (!claveValida(d.clave)) e.clave = "Mínimo 8 caracteres, con letras y números.";
  if (!d.acepta_terminos) e.acepta_terminos = "Debes aceptar los términos para continuar.";
  return e;
}

export default function FormRegistro({ alRegistrar }) {
  const [datos, setDatos] = useState(VACIO);
  const [errores, setErrores] = useState({});
  const [errorGeneral, setErrorGeneral] = useState("");
  const [cargando, setCargando] = useState(false);

  const cambiar = (campo) => (e) => {
    const valor = e.target.type === "checkbox" ? e.target.checked : e.target.value;
    setDatos((d) => ({ ...d, [campo]: valor }));
    if (errores[campo]) setErrores((er) => ({ ...er, [campo]: undefined }));
  };

  async function enviar(e) {
    e.preventDefault();
    if (cargando) return;
    setErrorGeneral("");
    const locales = validar(datos);
    setErrores(locales);
    if (Object.keys(locales).length) return;

    setCargando(true);
    try {
      const cuenta = await registrar({
        ...datos,
        nombre: datos.nombre.trim(), apellido: datos.apellido.trim(),
        cedula: datos.cedula.trim(), username: datos.username.trim(), correo: datos.correo.trim(), telefono: datos.telefono.trim(),
      });
      setDatos(VACIO);
      alRegistrar(datos.correo.trim(), cuenta.roles.includes("Socio"));
    } catch (err) {
      const campos = err.campos || {};
      setErrores(campos);
      // Si el servidor rechaza algo que no tiene campo en pantalla, se muestra arriba (nunca en silencio).
      const sinCampo = Object.entries(campos).filter(([k]) => !CAMPOS_VISIBLES.includes(k));
      setErrorGeneral(
        sinCampo.length ? sinCampo.map(([k, m]) => `${k}: ${m}`).join(" · ")
        : Object.keys(campos).length ? "" : err.message,
      );
    } finally {
      setCargando(false);
    }
  }

  return (
    <form onSubmit={enviar} noValidate className="tarjeta__form">
      <h1 className="acceso__titulo">Crear cuenta</h1>
      <p className="tarjeta__sub">Regístrate para ser parte de nuestra comunidad.</p>
      <p>Todos los campos son obligatorios.</p>
      {errorGeneral && <div className="alerta alerta--error" role="alert">{errorGeneral}</div>}

      <div className="fila">
        <Campo etiqueta="Nombres" required icono={IcoPersona} autoComplete="given-name" value={datos.nombre}
               onChange={cambiar("nombre")} error={errores.nombre} />
        <Campo etiqueta="Apellidos" required icono={IcoPersona} autoComplete="family-name" value={datos.apellido}
               onChange={cambiar("apellido")} error={errores.apellido} />
      </div>
      <Campo etiqueta="Cédula" required icono={IcoCedula} inputMode="numeric" maxLength={10} value={datos.cedula}
             onChange={(e) => { e.target.value = e.target.value.replace(/\D/g, ""); cambiar("cedula")(e); }} error={errores.cedula} />
      <Campo etiqueta="Usuario" required icono={IcoArroba} autoComplete="username" autoCapitalize="none" value={datos.username}
             onChange={cambiar("username")} error={errores.username}
             ayuda="Con este nombre podrás iniciar sesión." />
      <Campo etiqueta="Correo electrónico" required tipo="email" icono={IcoCorreo} autoComplete="email" value={datos.correo}
             onChange={cambiar("correo")} error={errores.correo} />
      <div className="fila">
        <Campo etiqueta="Teléfono" required tipo="tel" icono={IcoTelefono} inputMode="tel" autoComplete="tel" value={datos.telefono}
               onChange={cambiar("telefono")} error={errores.telefono} />
        <Campo etiqueta="Fecha de nacimiento" required tipo="date" icono={IcoCalendario} autoComplete="bday" value={datos.fecha_nacimiento}
               onChange={cambiar("fecha_nacimiento")} error={errores.fecha_nacimiento} />
      </div>
      <Campo etiqueta="Contraseña" required tipo="password" icono={IcoCandado} autoComplete="new-password" value={datos.clave}
             onChange={cambiar("clave")} error={errores.clave}
             ayuda="Mínimo 8 caracteres, con letras y números. Evita contraseñas comunes." />

      <label className={`check ${errores.acepta_terminos ? "check--error" : ""}`}>
        <input type="checkbox" required checked={datos.acepta_terminos} onChange={cambiar("acepta_terminos")} />
        <span>Acepto los <strong>Términos y Condiciones</strong> y el tratamiento de mis datos personales.</span>
      </label>
      {errores.acepta_terminos && <small className="campo__error" role="alert">{errores.acepta_terminos}</small>}

      <button className="boton boton--amarillo" disabled={cargando}>
        {cargando ? "Registrando…" : <>Registrarme <IcoFlecha className="boton__flecha" /></>}
      </button>
      <p className="tarjeta__pie">¿Ya tienes una cuenta? <Link className="enlace" to="/ingresar">Iniciar sesión</Link></p>
    </form>
  );
}
