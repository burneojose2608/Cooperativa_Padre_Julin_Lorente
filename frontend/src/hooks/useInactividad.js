import { useEffect } from "react";
import { CLAVE_ACTIVIDAD, INACTIVIDAD_MS } from "../utils/actividad";

/** El servidor mantiene el límite real; este temporizador retira la interfaz inactiva. */
export default function useInactividad(activa, alExpirar, alActividad) {
  useEffect(() => {
    if (!activa) return;
    let ultima = Date.now();
    try {
      const guardada = Number(localStorage.getItem(CLAVE_ACTIVIDAD));
      if (guardada > 0) ultima = Math.min(guardada, ultima);
    } catch { /* se mantiene el reloj de esta pestaña */ }
    let temporizador;
    let notificada = 0;
    let terminada = false;
    function comprobar() {
      if (terminada) return;
      clearTimeout(temporizador);
      const restante = INACTIVIDAD_MS - (Date.now() - ultima);
      if (restante <= 0) {
        terminada = true;
        void alExpirar();
      } else {
        temporizador = setTimeout(comprobar, restante);
      }
    }
    function actividad() {
      if (terminada) return;
      if (Date.now() - ultima >= INACTIVIDAD_MS) { comprobar(); return; }
      ultima = Date.now();
      try { localStorage.setItem(CLAVE_ACTIVIDAD, String(ultima)); } catch { /* almacenamiento opcional */ }
      comprobar();
      if (ultima - notificada >= 60_000) {
        notificada = ultima;
        void alActividad();
      }
    }
    function almacenamiento(evento) {
      if (evento.key !== CLAVE_ACTIVIDAD || !evento.newValue) return;
      const instante = Number(evento.newValue);
      if (Number.isFinite(instante) && instante > ultima && instante <= Date.now()) {
        ultima = instante;
        comprobar();
      }
    }
    const eventos = ["pointerdown", "keydown", "scroll", "touchstart"];
    eventos.forEach((evento) => window.addEventListener(evento, actividad, { passive: true }));
    window.addEventListener("storage", almacenamiento);
    document.addEventListener("visibilitychange", comprobar);
    comprobar();
    return () => {
      terminada = true;
      clearTimeout(temporizador);
      eventos.forEach((evento) => window.removeEventListener(evento, actividad));
      window.removeEventListener("storage", almacenamiento);
      document.removeEventListener("visibilitychange", comprobar);
    };
  }, [activa, alExpirar, alActividad]);
}
