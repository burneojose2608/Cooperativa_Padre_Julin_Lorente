// Validaciones de formato en el navegador (el backend siempre vuelve a validar).

// Regla acordada: diez dígitos, sin provincia ni verificador. El servidor valida de nuevo.
export function cedulaValida(c) {
  return typeof c === "string" && c.length === 10 && /^[0-9]{10}$/.test(c);
}

export const correoValido = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
export const telefonoValido = (v) => /^[0-9+]{7,15}$/.test(v);
export const claveValida = (v) => v.length >= 8 && /[A-Za-z]/.test(v) && /\d/.test(v);

const fechaCooperativa = new Intl.DateTimeFormat("en-CA", {
  timeZone: "America/Guayaquil", year: "numeric", month: "2-digit", day: "2-digit",
});

export function fechaMaximaNacimiento() {
  const partes = Object.fromEntries(fechaCooperativa.formatToParts(new Date()).map(({ type, value }) => [type, value]));
  const anio = Number(partes.year) - 18;
  const diasDelMes = new Date(Date.UTC(anio, Number(partes.month), 0)).getUTCDate();
  return `${anio}-${partes.month}-${String(Math.min(Number(partes.day), diasDelMes)).padStart(2, "0")}`;
}

export function fechaNacimientoValida(v) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) return false;
  const fecha = new Date(v + "T00:00:00Z");
  return !Number.isNaN(fecha.getTime()) && fecha.toISOString().slice(0, 10) === v && v >= "1900-01-01";
}

export const usernameValido = (v) => /^[A-Za-z0-9_.]{4,50}$/.test(v);
