// Validaciones de formato en el navegador (el backend siempre vuelve a validar).

// La cédula solo debe tener 10 dígitos (no se calcula el dígito verificador).
export const cedulaValida = (c) => /^\d{10}$/.test(c);

export const correoValido = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
export const telefonoValido = (v) => /^[0-9+]{7,15}$/.test(v);
export const claveValida = (v) => v.length >= 8 && /[A-Za-z]/.test(v) && /\d/.test(v);

export function fechaNacimientoValida(v) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) return false;
  const f = new Date(v + "T00:00:00");
  return !Number.isNaN(f.getTime()) && f <= new Date() && f.getFullYear() >= 1900;
}

export const usernameValido = (v) => /^[A-Za-z0-9_.]{4,50}$/.test(v);
