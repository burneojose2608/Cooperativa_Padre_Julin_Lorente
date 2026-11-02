import { api, sesion } from "./cliente";

export const registrar = (datos) => api.post("/auth/registro/", datos);

export async function iniciarSesion(identificador, clave) {
  const r = await api.post("/auth/login/", { identificador, clave });
  sesion.guardar(r);
  return r;
}

export const cerrarSesion = () => sesion.borrar();
export const miPerfil = () => api.getProtegido("/auth/yo/");

export const solicitarRecuperacion = (identificador) => api.post("/auth/recuperar/", { identificador });
export const restablecerClave = (token, clave) => api.post("/auth/restablecer/", { token, clave });
