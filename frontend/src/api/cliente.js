// Cliente HTTP: único lugar donde el frontend habla con el backend.
import { CLAVE_ACTIVIDAD } from "../utils/actividad";

const API = import.meta.env.VITE_HTTPS === "true" ? "/api" : (import.meta.env.VITE_API_URL || "/api");
export const CLAVE_SESION = "coop_sesion";
export const EVENTO_SESION_CERRADA = "coop:sesion-cerrada";

export const sesion = {
  leer() {
    try { return JSON.parse(localStorage.getItem(CLAVE_SESION)) || null; } catch { return null; }
  },
  guardar(datos) { try { localStorage.setItem(CLAVE_SESION, JSON.stringify(datos)); } catch { /* sin almacenamiento */ } },
  borrar() { try { localStorage.removeItem(CLAVE_SESION); localStorage.removeItem(CLAVE_ACTIVIDAD); } catch { /* sin almacenamiento */ } },
};

/** Error con el formato del backend, listo para mostrarse en pantalla. */
export class ErrorApi extends Error {
  constructor(mensaje, { estado = 0, campos = {} } = {}) {
    super(mensaje);
    this.estado = estado;
    this.campos = campos; // { cedula: "mensaje", ... }
  }
}

function interpretarError(estado, cuerpo) {
  // Error de negocio: { error: { codigo, mensaje, campo } }
  if (cuerpo?.error) {
    const { mensaje, campo } = cuerpo.error;
    return new ErrorApi(mensaje, { estado, campos: campo ? { [campo]: mensaje } : {} });
  }
  // Errores de formato de DRF: { campo: ["mensaje"] }
  if (cuerpo && typeof cuerpo === "object" && !cuerpo.detail) {
    const campos = {};
    for (const [k, v] of Object.entries(cuerpo)) campos[k] = Array.isArray(v) ? v[0] : String(v);
    return new ErrorApi("Revisa los campos marcados.", { estado, campos });
  }
  if (estado === 429) return new ErrorApi("Demasiados intentos. Espera un momento e inténtalo de nuevo.", { estado });
  if (estado === 401) return new ErrorApi("Tu sesión expiró. Inicia sesión de nuevo.", { estado });
  return new ErrorApi(cuerpo?.detail || "Ocurrió un error inesperado.", { estado });
}

async function peticion(ruta, { metodo = "GET", cuerpo, token } = {}) {
  let r;
  try {
    r = await fetch(`${API}${ruta}`, {
      method: metodo,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: cuerpo ? JSON.stringify(cuerpo) : undefined,
    });
  } catch {
    throw new ErrorApi("No se pudo conectar con el servidor. Revisa tu conexión.");
  }
  let datos = null;
  try { datos = await r.json(); } catch { /* respuesta sin cuerpo */ }
  if (!r.ok) throw interpretarError(r.status, datos);
  return datos;
}

/** Operación autenticada; un 401 previo a la ejecución renueva el token una vez. */
async function peticionProtegida(ruta, opciones = {}) {
  const s = sesion.leer();
  if (!s) throw new ErrorApi("Sin sesión.", { estado: 401 });
  try {
    const respuesta = await peticion(ruta, { ...opciones, token: s.access });
    if (sesion.leer()?.refresh !== s.refresh) throw new ErrorApi("La sesión fue cerrada.", { estado: 401 });
    return respuesta;
  } catch (e) {
    if (e.estado !== 401 || sesion.leer()?.refresh !== s.refresh) throw e;
    let nuevo;
    try {
      nuevo = await peticion("/auth/refresh/", { metodo: "POST", cuerpo: { refresh: s.refresh } });
    } catch (error) {
      if (error.estado === 401 && sesion.leer()?.refresh === s.refresh) {
        sesion.borrar();
        window.dispatchEvent(new CustomEvent(EVENTO_SESION_CERRADA));
      }
      throw error;
    }
    if (sesion.leer()?.refresh !== s.refresh) throw new ErrorApi("La sesión fue cerrada.", { estado: 401 });
    sesion.guardar({ ...s, access: nuevo.access });
    const respuesta = await peticion(ruta, { ...opciones, token: nuevo.access });
    if (sesion.leer()?.refresh !== s.refresh) throw new ErrorApi("La sesión fue cerrada.", { estado: 401 });
    return respuesta;
  }
}

export const api = {
  post: (ruta, cuerpo) => peticion(ruta, { metodo: "POST", cuerpo }),
  getProtegido: (ruta) => peticionProtegida(ruta),
  postProtegido: (ruta, cuerpo) => peticionProtegida(ruta, { metodo: "POST", cuerpo }),
};
