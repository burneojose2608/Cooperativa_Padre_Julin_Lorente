import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { api } from "../../api/cliente";
import useRecurso from "../../hooks/useRecurso";
import { Tarjeta, TituloPagina } from "../ui";
import { Aviso, CampoPanel } from "./comunes";
import { useOperacion } from "./operaciones";
import Referido from "./Referido";

function Contacto({ perfil, recargar }) {
  const { refrescarPerfil } = useAuth();
  const [correo, setCorreo] = useState(perfil.correo);
  const [telefono, setTelefono] = useState(perfil.telefono);
  const [foto, setFoto] = useState(null);
  const [url, setUrl] = useState("");
  const op = useOperacion(recargar);
  useEffect(() => {
    let vigente = true, enlace;
    if (perfil.tiene_foto) api.archivoProtegido("/auth/yo/foto/").then((blob) => {
      enlace = URL.createObjectURL(blob); if (vigente) setUrl(enlace);
    }).catch(() => {});
    return () => { vigente = false; if (enlace) URL.revokeObjectURL(enlace); };
  }, [perfil]);
  async function enviar(e) {
    e.preventDefault();
    const datos = new FormData(); datos.append("correo", correo); datos.append("telefono", telefono);
    if (foto) datos.append("foto", foto);
    await op.ejecutar(async () => {
      const actualizado = await api.patchProtegido("/auth/yo/", datos);
      setCorreo(actualizado.correo); setTelefono(actualizado.telefono); setFoto(null);
      await refrescarPerfil();
    });
  }
  return <Tarjeta titulo="Datos personales">
    <dl className="s2-identidad"><dt>Nombres y apellidos</dt><dd>{perfil.nombre} {perfil.apellido}</dd>
      <dt>Cédula</dt><dd>{perfil.cedula}</dd><dt>Usuario</dt><dd>{perfil.username}</dd>
      <dt>Fecha de nacimiento</dt><dd>{perfil.fecha_nacimiento}</dd></dl>
    <p>Los datos de identificación los administra la cooperativa.</p>
    {perfil.tiene_foto && url && <img className="s2-foto" src={url} alt="Tu foto de perfil" />}
    <form className="s2-form" onSubmit={enviar}>
      <CampoPanel etiqueta="Correo electrónico" type="email" required value={correo} onChange={(e) => setCorreo(e.target.value)} />
      <CampoPanel etiqueta="Teléfono" required pattern="[0-9+]{7,15}" value={telefono} onChange={(e) => setTelefono(e.target.value)} />
      <CampoPanel etiqueta="Foto (JPG, PNG o WebP; máximo 10 MB)" type="file" accept="image/jpeg,image/png,image/webp" onChange={(e) => setFoto(e.target.files[0])} />
      <Aviso {...op} /><button className="boton" disabled={op.ocupado}>Guardar contacto</button>
      {perfil.tiene_foto && <button className="boton boton--claro" type="button" disabled={op.ocupado}
        onClick={() => op.ejecutar(() => api.deleteProtegido("/auth/yo/foto/"))}>Quitar foto</button>}
    </form>
  </Tarjeta>;
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
  return <Tarjeta titulo="Cambiar contraseña"><form className="s2-form" onSubmit={enviar}>
    <p>Usa al menos ocho caracteres con letras y números. Al guardar, deberás iniciar sesión nuevamente.</p>
    <CampoPanel etiqueta="Contraseña actual" type="password" autoComplete="current-password" required value={actual} onChange={(e) => setActual(e.target.value)} />
    <CampoPanel etiqueta="Nueva contraseña" type="password" autoComplete="new-password" required minLength={8} value={nueva} onChange={(e) => setNueva(e.target.value)} />
    <CampoPanel etiqueta="Repetir contraseña" type="password" autoComplete="new-password" required value={repetir} onChange={(e) => setRepetir(e.target.value)} />
    <Aviso {...op} /><button className="boton" disabled={op.ocupado}>Actualizar contraseña</button>
  </form></Tarjeta>;
}

function PerfilAutenticado() {
  const { usuario } = useAuth();
  const recurso = useRecurso("/auth/yo/");
  return <><TituloPagina titulo="Mi perfil" sub="Consulta tus datos y mantén actualizado tu contacto." />
    <Aviso error={recurso.error} />{recurso.datos ? <div className="s2-columnas">
      <Contacto key={recurso.datos.id} perfil={recurso.datos} recargar={recurso.recargar} /><Clave />
    </div> : !recurso.error && <p role="status">Cargando perfil…</p>}
    {usuario?.roles?.includes("Socio") && usuario?.permisos?.includes("referidos.compartir") && <Referido />}</>;
}
export default function Perfil() {
  const { usuario, verificando } = useAuth();
  if (verificando) return <p>Cargando…</p>;
  return usuario ? <PerfilAutenticado /> : <Navigate to="/ingresar" replace />;
}
