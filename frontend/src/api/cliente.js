// Cliente HTTP: único lugar donde el frontend habla con el backend.
const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";
const CLAVE = "coop_sesion";

export const sesion = {
  leer() {
    try { return JSON.parse(localStorage.getItem(CLAVE)) || null; } catch { return null; }
  },
  guardar(datos) { try { localStorage.setItem(CLAVE, JSON.stringify(datos)); } catch { /* sin almacenamiento */ } },
  borrar() { try { localStorage.removeItem(CLAVE); } catch { /* sin almacenamiento */ } },
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

export const api = {
  post: (ruta, cuerpo) => peticion(ruta, { metodo: "POST", cuerpo }),
  /** GET autenticado; si el token venció, lo renueva una vez. */
  async getProtegido(ruta) {
    const s = sesion.leer();
    if (!s) throw new ErrorApi("Sin sesión.", { estado: 401 });
    try {
      return await peticion(ruta, { token: s.access });
    } catch (e) {
      if (e.estado !== 401) throw e;
      const nuevo = await peticion("/auth/refresh/", { metodo: "POST", cuerpo: { refresh: s.refresh } });
      sesion.guardar({ ...s, access: nuevo.access });
      return peticion(ruta, { token: nuevo.access });
    }
  },
};
