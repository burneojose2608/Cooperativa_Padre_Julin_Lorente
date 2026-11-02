import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { cerrarSesion, iniciarSesion, miPerfil } from "../api/auth";
import { sesion } from "../api/cliente";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(() => sesion.leer()?.usuario ?? null);
  const [verificando, setVerificando] = useState(() => Boolean(sesion.leer()));

  // Al abrir la página, confirma con el servidor que la sesión guardada sigue vigente.
  useEffect(() => {
    if (!sesion.leer()) return;
    miPerfil()
      .then((p) => setUsuario((u) => ({ ...u, ...p })))
      .catch(() => { cerrarSesion(); setUsuario(null); })
      .finally(() => setVerificando(false));
  }, []);

  const entrar = useCallback(async (identificador, clave) => {
    const r = await iniciarSesion(identificador, clave);
    setUsuario(r.usuario);
    return r.usuario;
  }, []);

  const salir = useCallback(() => { cerrarSesion(); setUsuario(null); }, []);

  const valor = useMemo(() => ({ usuario, verificando, entrar, salir }), [usuario, verificando, entrar, salir]);
  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext);
