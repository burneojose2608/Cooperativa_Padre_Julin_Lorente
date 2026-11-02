// Validaciones de formato en el navegador (el backend siempre vuelve a validar).

export function cedulaValida(c) {
  if (!/^\d{10}$/.test(c)) return false;
  const provincia = Number(c.slice(0, 2));
  if (!((provincia >= 1 && provincia <= 24) || provincia === 30)) return false;
  if (Number(c[2]) >= 6) return false;
  const coef = [2, 1, 2, 1, 2, 1, 2, 1, 2];
  let total = 0;
  for (let i = 0; i < 9; i++) {
    let p = Number(c[i]) * coef[i];
    if (p >= 10) p -= 9;
    total += p;
  }
  return (10 - (total % 10)) % 10 === Number(c[9]);
}

export const correoValido = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
export const telefonoValido = (v) => /^[0-9+]{7,15}$/.test(v);
export const claveValida = (v) => v.length >= 8 && /[A-Za-z]/.test(v) && /\d/.test(v);

export function fechaNacimientoValida(v) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) return false;
  const f = new Date(v + "T00:00:00");
  return !Number.isNaN(f.getTime()) && f <= new Date() && f.getFullYear() >= 1900;
}

export const usernameValido = (v) => /^[A-Za-z0-9_.]{4,50}$/.test(v);
