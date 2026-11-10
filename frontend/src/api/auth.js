import { api, sesion } from "./cliente";
import { reiniciarActividad } from "../utils/actividad";

export const registrar = (datos) => api.post("/auth/registro/", datos);

export async function iniciarSesion(identificador, clave) {
  const r = await api.post("/auth/login/", { identificador, clave });
  sesion.guardar(r);
  reiniciarActividad();
  return r;
}

export async function cerrarSesion() {
  const actual = sesion.leer();
  if (!actual) return;
  try {
    await api.postProtegido("/auth/logout/", {});
  } catch (error) {
    if (error.estado !== 401) throw error;
  }
  if (sesion.leer()?.refresh === actual.refresh) sesion.borrar();
}
export const miPerfil = () => api.getProtegido("/auth/yo/");
export const notificarActividad = () => api.postProtegido("/auth/actividad/", {});

export const solicitarRecuperacion = (identificador) => api.post("/auth/recuperar/", { identificador });
export const restablecerClave = (token, clave) => api.post("/auth/restablecer/", { token, clave });
