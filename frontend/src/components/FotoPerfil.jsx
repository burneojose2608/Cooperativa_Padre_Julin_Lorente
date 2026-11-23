import { useEffect, useState } from "react";
import { api } from "../api/cliente";

export default function FotoPerfil({ perfil, className, claseIniciales = className, alt = "", ruta = "/auth/yo/foto/" }) {
  const [foto, setFoto] = useState(null);
  useEffect(() => {
    if (!perfil?.tiene_foto) return;
    let vigente = true;
    let url;
    api.archivoProtegido(ruta).then((archivo) => {
      if (!vigente) return;
      url = URL.createObjectURL(archivo);
      setFoto({ perfil, ruta, url });
    }).catch(() => {});
    return () => {
      vigente = false;
      if (url) URL.revokeObjectURL(url);
    };
  }, [perfil, ruta]);

  const iniciales = `${perfil?.nombre?.[0] ?? ""}${perfil?.apellido?.[0] ?? ""}`.toUpperCase() || "U";
  return foto?.perfil === perfil && foto?.ruta === ruta && perfil?.tiene_foto
    ? <img className={className} src={foto.url} alt={alt} />
    : <span className={claseIniciales} aria-hidden="true">{iniciales}</span>;
}

export function FotoCuentaAdministrada({ cuenta, grande = false }) {
  return <FotoPerfil perfil={cuenta} ruta={`/auth/administracion/usuarios/${cuenta.id}/foto/`}
    className={grande ? "us-avatar us-avatar--grande" : "us-avatar"} />;
}
