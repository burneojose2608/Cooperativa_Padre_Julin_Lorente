import { useState } from "react";
import { registrar } from "../api/auth";
import { cedulaValida, claveValida, correoValido, fechaNacimientoValida, telefonoValido, usernameValido } from "../utils/validaciones";
import Campo from "./Campo";

const CAMPOS_VISIBLES = ["nombre", "apellido", "cedula", "username", "correo", "telefono",
                         "fecha_nacimiento", "clave", "acepta_terminos"];
const VACIO = { nombre: "", apellido: "", cedula: "", username: "", correo: "", telefono: "",
                fecha_nacimiento: "", clave: "", acepta_terminos: false };

function validar(d) {
  const e = {};
  if (!d.nombre.trim()) e.nombre = "Ingresa tus nombres.";
  if (!d.apellido.trim()) e.apellido = "Ingresa tus apellidos.";
  if (!cedulaValida(d.cedula)) e.cedula = "La cédula ingresada no es válida.";
  if (!usernameValido(d.username)) e.username = "Usuario de 4 a 50 caracteres: letras, números, punto o guion bajo.";
  if (!correoValido(d.correo)) e.correo = "Ingresa un correo válido.";
  if (!telefonoValido(d.telefono)) e.telefono = "Usa solo números (7 a 15 dígitos).";
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
    setErrorGeneral("");
    const locales = validar(datos);
    setErrores(locales);
    if (Object.keys(locales).length) return;

    setCargando(true);
    try {
      await registrar({
        ...datos,
        nombre: datos.nombre.trim(), apellido: datos.apellido.trim(),
        cedula: datos.cedula.trim(), username: datos.username.trim(), correo: datos.correo.trim(), telefono: datos.telefono.trim(),
      });
      setDatos(VACIO);
      alRegistrar(datos.correo.trim());
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
      <h2>Crear cuenta</h2>
      <p className="tarjeta__sub">Regístrate como socio</p>
      {errorGeneral && <div className="alerta alerta--error" role="alert">{errorGeneral}</div>}

      <div className="fila">
        <Campo etiqueta="Nombres" autoComplete="given-name" value={datos.nombre}
               onChange={cambiar("nombre")} error={errores.nombre} />
        <Campo etiqueta="Apellidos" autoComplete="family-name" value={datos.apellido}
               onChange={cambiar("apellido")} error={errores.apellido} />
      </div>
      <Campo etiqueta="Cédula" inputMode="numeric" maxLength={10} value={datos.cedula}
             onChange={cambiar("cedula")} error={errores.cedula} />
      <Campo etiqueta="Usuario" autoComplete="username" autoCapitalize="none" value={datos.username}
             onChange={cambiar("username")} error={errores.username}
             ayuda="Con este nombre podrás iniciar sesión." />
      <Campo etiqueta="Correo electrónico" tipo="email" autoComplete="email" value={datos.correo}
             onChange={cambiar("correo")} error={errores.correo} />
      <div className="fila">
        <Campo etiqueta="Teléfono" tipo="tel" inputMode="tel" autoComplete="tel" value={datos.telefono}
               onChange={cambiar("telefono")} error={errores.telefono} />
        <Campo etiqueta="Fecha de nacimiento" tipo="date" autoComplete="bday" value={datos.fecha_nacimiento}
               onChange={cambiar("fecha_nacimiento")} error={errores.fecha_nacimiento} />
      </div>
      <Campo etiqueta="Contraseña" tipo="password" autoComplete="new-password" value={datos.clave}
             onChange={cambiar("clave")} error={errores.clave}
             ayuda="Mínimo 8 caracteres, con letras y números." />

      <label className={`check ${errores.acepta_terminos ? "check--error" : ""}`}>
        <input type="checkbox" checked={datos.acepta_terminos} onChange={cambiar("acepta_terminos")} />
        <span>Acepto los Términos y el tratamiento de datos personales</span>
      </label>
      {errores.acepta_terminos && <small className="campo__error" role="alert">{errores.acepta_terminos}</small>}

      <button className="boton" disabled={cargando}>{cargando ? "Registrando…" : "Registrarme"}</button>
    </form>
  );
}
