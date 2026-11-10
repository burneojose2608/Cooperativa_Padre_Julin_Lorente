import { PIAuditoria, PIBeneficios, PICampanas, PICapacitacion, PIContenidos, PIInicio, PIJuegos, PINotificaciones,
  PIParametros, PIPuntos, PIReferidos, PIReportes, PIRoles, PISorteos, PIUsuarios } from "./IconosPanel";

// ruta "" = inicio. Las secciones sin pantalla muestran «Próximamente».
export const MENUS = {
  socio: [
    { ruta: "", etq: "Inicio", ico: PIInicio }, { ruta: "referidos", etq: "Referidos", ico: PIReferidos },
    { ruta: "puntos", etq: "Puntos", ico: PIPuntos }, { ruta: "capacitaciones", etq: "Capacitaciones", ico: PICapacitacion },
    { ruta: "juegos", etq: "Juegos", ico: PIJuegos }, { ruta: "sorteos", etq: "Sorteos", ico: PISorteos },
    { ruta: "beneficios", etq: "Beneficios", ico: PIBeneficios }, { ruta: "contenidos", etq: "Contenidos", ico: PIContenidos },
    { ruta: "notificaciones", etq: "Notificaciones", ico: PINotificaciones },
  ],
  marketing: [
    { ruta: "", etq: "Inicio", ico: PIInicio }, { ruta: "campanas", etq: "Campañas", ico: PICampanas },
    { ruta: "referidos", etq: "Referidos", ico: PIReferidos }, { ruta: "contenidos", etq: "Contenidos", ico: PIContenidos },
    { ruta: "sorteos", etq: "Sorteos", ico: PISorteos }, { ruta: "beneficios", etq: "Beneficios", ico: PIBeneficios },
    { ruta: "reportes", etq: "Reportes", ico: PIReportes },
  ],
  admin: [
    { ruta: "", etq: "Inicio", ico: PIInicio }, { ruta: "usuarios", etq: "Usuarios", ico: PIUsuarios },
    { ruta: "validar-socios", etq: "Validar socios", ico: PIUsuarios },
    { ruta: "roles", etq: "Roles y permisos", ico: PIRoles }, { ruta: "parametros", etq: "Parámetros", ico: PIParametros },
    { ruta: "auditoria", etq: "Auditoría", ico: PIAuditoria }, { ruta: "reportes", etq: "Reportes", ico: PIReportes },
  ],
};
export const TITULO_DE_AREA = { socio: "Socio", marketing: "Marketing", admin: "Administración" };
