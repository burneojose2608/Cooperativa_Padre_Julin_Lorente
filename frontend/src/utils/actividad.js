export const CLAVE_ACTIVIDAD = "coop_ultima_actividad";
export const INACTIVIDAD_MS = 15 * 60 * 1000;

export function reiniciarActividad() {
  try { localStorage.setItem(CLAVE_ACTIVIDAD, String(Date.now())); } catch { /* sin almacenamiento */ }
}
