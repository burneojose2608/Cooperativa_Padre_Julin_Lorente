import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { cerrarSesion, iniciarSesion, miPerfil, notificarActividad } from "../api/auth";
import { CLAVE_SESION, EVENTO_SESION_CERRADA, sesion } from "../api/cliente";
import useInactividad from "../hooks/useInactividad";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(() => sesion.leer()?.usuario ?? null);
  const [verificando, setVerificando] = useState(() => Boolean(sesion.leer()));
  const [errorSesion, setErrorSesion] = useState("");

  // Al abrir la página, confirma con el servidor que la sesión guardada sigue vigente.
  useEffect(() => {
    const inicial = sesion.leer();
    if (!inicial) return;
    let vigente = true;
    miPerfil()
      .then((p) => { if (vigente && sesion.leer()?.refresh === inicial.refresh) setUsuario((u) => u ? { ...u, ...p } : null); })
      .catch(() => { if (vigente && sesion.leer()?.refresh === inicial.refresh) { sesion.borrar(); setUsuario(null); } })
      .finally(() => { if (vigente) setVerificando(false); });
    return () => { vigente = false; };
  }, []);

  useEffect(() => {
    const invalidada = () => {
      setUsuario(null);
      setErrorSesion("Tu sesión venció o fue cerrada. Inicia sesión nuevamente.");
    };
    const almacenamiento = (evento) => {
      if (evento.key === CLAVE_SESION) {
        setUsuario(sesion.leer()?.usuario ?? null);
      }
    };
    window.addEventListener(EVENTO_SESION_CERRADA, invalidada);
    window.addEventListener("storage", almacenamiento);
    return () => {
      window.removeEventListener(EVENTO_SESION_CERRADA, invalidada);
      window.removeEventListener("storage", almacenamiento);
    };
  }, []);

  const entrar = useCallback(async (identificador, clave) => {
    const r = await iniciarSesion(identificador, clave);
    setUsuario(r.usuario);
    setErrorSesion("");
    return r.usuario;
  }, []);

  const salir = useCallback(async () => {
    const anterior = sesion.leer()?.refresh;
    try {
      await cerrarSesion();
      if (!sesion.leer() || sesion.leer()?.refresh === anterior) {
        setUsuario(null);
        setErrorSesion("");
      }
    } catch (error) {
      if (sesion.leer()?.refresh === anterior) setErrorSesion(`No se pudo confirmar el cierre en el servidor. ${error.message}`);
    }
  }, []);

  const expirar = useCallback(async () => {
    const anterior = sesion.leer()?.refresh;
    try { await cerrarSesion(); } catch { /* el límite del servidor sigue vigente sin conexión */ }
    if (!sesion.leer() || sesion.leer()?.refresh === anterior) {
      sesion.borrar();
      setUsuario(null);
      setErrorSesion("La sesión se cerró por 15 minutos de inactividad.");
    }
  }, []);

  const actividad = useCallback(async () => {
    const anterior = sesion.leer()?.refresh;
    try { await notificarActividad(); } catch (error) {
      if (error.estado === 401 && sesion.leer()?.refresh === anterior) { sesion.borrar(); setUsuario(null); }
    }
  }, []);

  useInactividad(Boolean(usuario), expirar, actividad);

  const refrescarPerfil = useCallback(async () => {
    const anterior = sesion.leer()?.refresh;
    const perfil = await miPerfil();
    const actual = sesion.leer();
    if (actual?.refresh === anterior) {
      sesion.guardar({ ...actual, usuario: { ...actual.usuario, ...perfil } });
      setUsuario((u) => u ? { ...u, ...perfil } : null);
    }
    return perfil;
  }, []);

  const valor = useMemo(() => ({ usuario, verificando, entrar, salir, refrescarPerfil }), [usuario, verificando, entrar, salir, refrescarPerfil]);
  return <AuthContext.Provider value={valor}>
    {errorSesion && <div className="alerta alerta--error" role="alert">{errorSesion}</div>}
    {children}
  </AuthContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext);
