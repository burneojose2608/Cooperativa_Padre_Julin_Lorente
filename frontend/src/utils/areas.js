// Cada "área" es una pantalla distinta según el rol. El servidor decide qué área le toca al usuario.
export const RUTA_DE_AREA = {
  socio: "/panel",
  admin: "/admin",
  marketing: "/marketing",
  rse: "/responsabilidad-social",
  contenidos: "/contenidos",
};

export const rutaDe = (area) => RUTA_DE_AREA[area] || "/mi-cuenta";

// Contenido de cada pantalla. Las opciones se irán activando a medida que se construyan los módulos.
export const AREAS = {
  socio: {
    nombre: "Socio",
    subtitulo: "Tu espacio como socio de la cooperativa.",
    opciones: ["Mi código de referido", "Mis referidos", "Mis puntos", "Capacitaciones", "Sorteos", "Canjes"],
  },
  admin: {
    nombre: "Administración",
    subtitulo: "Gestión general de la plataforma.",
    opciones: ["Usuarios y roles", "Auditoría", "Reglas de puntos", "Convenios"],
  },
  marketing: {
    nombre: "Marketing",
    subtitulo: "Campañas, segmentos y sorteos.",
    opciones: ["Campañas", "Segmentos", "Sorteos", "Reportes de referidos"],
  },
  rse: {
    nombre: "Responsabilidad Social",
    subtitulo: "Convenios y bienestar de los socios.",
    opciones: ["Convenios", "Recursos de bienestar", "Reportes"],
  },
  contenidos: {
    nombre: "Contenidos",
    subtitulo: "Contenidos, capacitaciones y talleres.",
    opciones: ["Contenidos", "Capacitaciones", "Talleres"],
  },
};
