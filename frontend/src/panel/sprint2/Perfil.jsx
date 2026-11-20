import { useEffect, useRef, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { PICalendario, PICamara, PICandado, PICorreo, PIIdentidad, PIOk, PITelefono, PIUsuarios } from "../IconosPanel";
import { Aviso, CampoPanel } from "./comunes";
import { useOperacion } from "./operaciones";
import Referido from "./Referido";
import "./perfil.css";

const TIPOS_FOTO = ["image/jpeg", "image/png", "image/webp"];
const MAX_FOTO = 10 * 1024 * 1024;
const fechaLarga = (iso) => { try { return new Date(`${iso}T00:00:00`).toLocaleDateString("es-EC", { day: "2-digit", month: "long", year: "numeric" }); } catch { return iso; } };

/** Dato de solo lectura con icono: los administra la cooperativa. */
const Dato = ({ icono: Ico, etiqueta, valor }) => (
  <div className="pf-dato"><span className="pf-dato__etq">{etiqueta}</span>
    <div className="pf-dato__caja"><Ico aria-hidden="true" /><span>{valor || "—"}</span></div></div>
);

/** Campo editable con icono a la izquierda. */
const CampoIcono = ({ icono: Ico, etiqueta, ...props }) => (
  <label className="pf-campo"><span>{etiqueta}</span>
    <div className="pf-campo__caja"><Ico aria-hidden="true" /><input {...props} /></div></label>
);

function Tarjeta({ perfil, usuario, recargar }) {
  const { refrescarPerfil } = useAuth();
  const [url, setUrl] = useState("");
  const entrada = useRef(null);
  const op = useOperacion(recargar);
  useEffect(() => {
    let vigente = true, enlace;
    if (perfil.tiene_foto) api.archivoProtegido("/auth/yo/foto/").then((blob) => {
      enlace = URL.createObjectURL(blob); if (vigente) setUrl(enlace);
    }).catch(() => {});
    else setUrl("");
    return () => { vigente = false; if (enlace) URL.revokeObjectURL(enlace); };
  }, [perfil]);
  async function elegir(e) {
    const archivo = e.target.files[0]; e.target.value = "";
    if (!archivo) return;
    await op.ejecutar(async () => {
      if (!TIPOS_FOTO.includes(archivo.type)) throw new Error("La foto debe ser JPG, PNG o WebP.");
      if (archivo.size > MAX_FOTO) throw new Error("La foto no puede pesar más de 10 MB.");
      const datos = new FormData(); datos.append("foto", archivo);
      await api.patchProtegido("/auth/yo/", datos); await refrescarPerfil();
    }, "Foto actualizada.");
  }
  const ini = `${perfil.nombre?.[0] ?? ""}${perfil.apellido?.[0] ?? ""}`.toUpperCase() || "U";
  return (
    <section className="pf-tarjeta pf-identidad" aria-label="Tu foto y rol">
      <div className="pf-foto">
        {url ? <img src={url} alt="Tu foto de perfil" /> : <span className="pf-foto__ini" aria-hidden="true">{ini}</span>}
        <button type="button" className="pf-foto__camara" aria-label="Cambiar foto de perfil" disabled={op.ocupado} onClick={() => entrada.current?.click()}><PICamara /></button>
        <input ref={entrada} type="file" hidden aria-label="Elegir foto" accept="image/jpeg,image/png,image/webp" onChange={elegir} />
      </div>
      <h2>{perfil.nombre} {perfil.apellido}</h2>
      <span className="pf-rol">{usuario.roles?.join(", ")}</span>
      {usuario.codigo_socio && <p className="pf-linea">Código: {usuario.codigo_socio}</p>}
      <p className="pf-linea">Usuario: {perfil.username}</p>
      <p className="pf-ayuda">JPG, PNG o WebP · máximo 10 MB</p>
      {perfil.tiene_foto && <button type="button" className="pf-quitar" disabled={op.ocupado}
        onClick={() => op.ejecutar(async () => { await api.deleteProtegido("/auth/yo/foto/"); await refrescarPerfil(); }, "Foto eliminada.")}>Quitar foto</button>}
      <Aviso {...op} />
    </section>
  );
}

function Personales({ perfil }) {
  return <div className="pf-panel" role="tabpanel" aria-label="Datos personales">
    <div className="pf-rejilla">
      <Dato icono={PIUsuarios} etiqueta="Nombres" valor={perfil.nombre} />
      <Dato icono={PIUsuarios} etiqueta="Apellidos" valor={perfil.apellido} />
      <Dato icono={PIIdentidad} etiqueta="Cédula" valor={perfil.cedula} />
      <Dato icono={PIUsuarios} etiqueta="Usuario" valor={perfil.username} />
      <Dato icono={PICalendario} etiqueta="Fecha de nacimiento" valor={perfil.fecha_nacimiento && fechaLarga(perfil.fecha_nacimiento)} />
    </div>
    <p className="pf-ayuda">Los datos de identificación los administra la cooperativa. Si hay un error, acércate a una agencia para corregirlo.</p>
  </div>;
}

function Contacto({ perfil, recargar }) {
  const { refrescarPerfil } = useAuth();
  const [correo, setCorreo] = useState(perfil.correo);
  const [telefono, setTelefono] = useState(perfil.telefono);
  const op = useOperacion(recargar);
  async function enviar(e) {
    e.preventDefault();
    const datos = new FormData(); datos.append("correo", correo); datos.append("telefono", telefono);
    await op.ejecutar(async () => {
      const actualizado = await api.patchProtegido("/auth/yo/", datos);
      setCorreo(actualizado.correo); setTelefono(actualizado.telefono);
      await refrescarPerfil();
    });
  }
  return <form className="pf-panel" role="tabpanel" aria-label="Contacto" onSubmit={enviar}>
    <div className="pf-rejilla">
      <CampoIcono icono={PICorreo} etiqueta="Correo electrónico" type="email" required value={correo} onChange={(e) => setCorreo(e.target.value)} />
      <CampoIcono icono={PITelefono} etiqueta="Teléfono" required pattern="[0-9+]{7,15}" title="Solo números, de 7 a 15 dígitos" value={telefono} onChange={(e) => setTelefono(e.target.value)} />
    </div>
    <Aviso {...op} />
    <div className="pf-acciones">
      <button type="button" className="boton boton--claro" disabled={op.ocupado} onClick={() => { setCorreo(perfil.correo); setTelefono(perfil.telefono); }}>Cancelar</button>
      <button className="boton boton--amarillo" disabled={op.ocupado}><PIOk className="boton__ico" />Guardar contacto</button>
    </div>
  </form>;
}

function Clave() {
  const { salir } = useAuth();
  const [actual, setActual] = useState(""); const [nueva, setNueva] = useState(""); const [repetir, setRepetir] = useState("");
  const op = useOperacion();
  async function enviar(e) {
    e.preventDefault();
    await op.ejecutar(async () => {
      if (nueva !== repetir) throw new Error("Las contraseñas no coinciden.");
      await api.postProtegido("/auth/yo/clave/", { actual, nueva });
      await salir();
    }, "Contraseña actualizada. Inicia sesión nuevamente.");
  }
  return <form className="pf-panel" role="tabpanel" aria-label="Seguridad" onSubmit={enviar}>
    <p className="pf-ayuda">Usa al menos ocho caracteres con letras y números. Al guardar, deberás iniciar sesión nuevamente.</p>
    <div className="pf-rejilla">
      <CampoPanel etiqueta="Contraseña actual" type="password" autoComplete="current-password" required value={actual} onChange={(e) => setActual(e.target.value)} />
      <span />
      <CampoPanel etiqueta="Nueva contraseña" type="password" autoComplete="new-password" required minLength={8} value={nueva} onChange={(e) => setNueva(e.target.value)} />
      <CampoPanel etiqueta="Repetir contraseña" type="password" autoComplete="new-password" required value={repetir} onChange={(e) => setRepetir(e.target.value)} />
    </div>
    <Aviso {...op} />
    <div className="pf-acciones"><button className="boton boton--amarillo" disabled={op.ocupado}><PICandado className="boton__ico" />Actualizar contraseña</button></div>
  </form>;
}

const PESTANAS = [["datos", "Datos personales", PIUsuarios], ["contacto", "Contacto", PICorreo], ["seguridad", "Seguridad", PICandado]];

function PerfilAutenticado() {
  const { usuario } = useAuth();
  const recurso = useRecurso("/auth/yo/");
  const [pestana, setPestana] = useState("datos");
  const p = recurso.datos;
  return <div className="pf">
    <div className="pf-cab"><span className="pf-cab__ico"><PIUsuarios /></span>
      <div><h1>Mi perfil</h1><p>Consulta y actualiza tu información personal.</p></div></div>
    <Aviso error={recurso.error} />
    {p ? <div className="pf-cuerpo">
      <Tarjeta perfil={p} usuario={usuario} recargar={recurso.recargar} />
      <section className="pf-tarjeta">
        <div className="pf-pestanas" role="tablist" aria-label="Secciones del perfil">
          {PESTANAS.map(([k, etq, Ico]) => <button key={k} type="button" role="tab" aria-selected={pestana === k}
            className={pestana === k ? "on" : ""} onClick={() => setPestana(k)}><Ico aria-hidden="true" /><span>{etq}</span></button>)}
        </div>
        {pestana === "datos" && <Personales perfil={p} />}
        {pestana === "contacto" && <Contacto key={p.id} perfil={p} recargar={recurso.recargar} />}
        {pestana === "seguridad" && <Clave />}
      </section>
    </div> : !recurso.error && <p role="status">Cargando perfil…</p>}
    {usuario?.roles?.includes("Socio") && usuario?.permisos?.includes("referidos.compartir") && <Referido />}
  </div>;
}
export default function Perfil() {
  const { usuario, verificando } = useAuth();
  if (verificando) return <p>Cargando…</p>;
  return usuario ? <PerfilAutenticado /> : <Navigate to="/ingresar" replace />;
}
