// =====================================================================================
// DATOS DE EJEMPLO. Los módulos de referidos, puntos, campañas, etc. aún no tienen backend,
// así que las pantallas leen de aquí. Cuando exista cada endpoint, se reemplaza SOLO este archivo
// (o las funciones de abajo) por llamadas a `api` y las pantallas no cambian.
// =====================================================================================
export const ROLES = ["Administrador", "Marketing", "Responsabilidad Social", "Gestor de contenidos", "Socio"];

export const socioDemo = {
  puntos: 1250,
  codigo: "PJL-MLOP26",
  nivel: { nombre: "Plata", siguiente: "Oro", desde: 1000, hasta: 2000 },
  referidos: [
    { nombre: "Carlos Ruiz", fecha: "02/10/2026", estado: "Concretado", puntos: 100 },
    { nombre: "Ana Torres", fecha: "15/10/2026", estado: "En proceso", puntos: 0 },
    { nombre: "Luis Paredes", fecha: "28/10/2026", estado: "En proceso", puntos: 0 },
    { nombre: "Rosa Vega", fecha: "30/10/2026", estado: "Rechazado", puntos: 0 },
  ],
  movimientos: [
    { fecha: "02/11/2026", detalle: "Referido concretado: Carlos Ruiz", puntos: 100 },
    { fecha: "28/10/2026", detalle: "Capacitación completada: Educación Financiera", puntos: 150 },
    { fecha: "20/10/2026", detalle: "Participación en campaña Refiere y Gana", puntos: 50 },
    { fecha: "05/10/2026", detalle: "Canje: Bono de consumo", puntos: -500 },
  ],
  beneficios: [
    { id: 1, nombre: "Bono de consumo", puntos: 500, icono: "regalo" },
    { id: 2, nombre: "Audífonos inalámbricos", puntos: 2000, icono: "audio" },
    { id: 3, nombre: "Kit promocional", puntos: 300, icono: "kit" },
  ],
  capacitaciones: [
    { id: 1, titulo: "Educación Financiera", detalle: "Aprende a gestionar tus finanzas.", horas: 2, modalidad: "Virtual", estado: "Disponible" },
    { id: 2, titulo: "Ahorro y Planificación", detalle: "Buenas prácticas de ahorro.", horas: 3, modalidad: "Presencial", estado: "Disponible" },
    { id: 3, titulo: "Seguridad en canales digitales", detalle: "Protege tu cuenta y tus datos.", horas: 1, modalidad: "Virtual", estado: "En curso", avance: 60 },
    { id: 4, titulo: "Cooperativismo básico", detalle: "Historia y valores de la cooperativa.", horas: 2, modalidad: "Virtual", estado: "Completada" },
  ],
  campana: { nombre: "Refiere y Gana", texto: "Invita a más personas y acumula puntos." },
};

export const marketingDemo = {
  kpis: { referidos: 125, puntos: 24500, campanas: 5, canjes: 67 },
  porCampana: [
    { etq: "Verano Cooperativo", valor: 50 },
    { etq: "Refiere y Gana", valor: 100 },
    { etq: "Ahorro Inteligente", valor: 25 },
    { etq: "Educación 2026", valor: 70 },
  ],
  campanas: [
    { id: 1, nombre: "Refiere y Gana", estado: "Activa", inicio: "01/10/2026", fin: "30/11/2026" },
    { id: 2, nombre: "Ahorro Inteligente", estado: "Programada", inicio: "15/11/2026", fin: "15/12/2026" },
    { id: 3, nombre: "Vive la Cooperativa", estado: "Finalizada", inicio: "01/08/2026", fin: "30/08/2026" },
  ],
};

export const adminDemo = {
  kpis: { usuarios: 1024, roles: 5, modulos: 10, operaciones: 3560 },
  actividad: [250, 430, 380, 520, 480, 620, 700, 910, 990],
  meses: ["Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"],
  usuarios: [
    { id: 1, nombre: "Ana Torres", rol: "Marketing", estado: "Activo" },
    { id: 2, nombre: "Luis Paredes", rol: "Responsabilidad Social", estado: "Activo" },
    { id: 3, nombre: "María López", rol: "Socio", estado: "Activo" },
    { id: 4, nombre: "Carlos Ruiz", rol: "Administrador", estado: "Activo" },
  ],
  auditoria: [
    { fecha: "06/11/2026 19:42", usuario: "mlopez", accion: "LOGIN", resultado: "EXITO" },
    { fecha: "06/11/2026 19:40", usuario: "mlopez", accion: "LOGOUT", resultado: "EXITO" },
    { fecha: "06/11/2026 18:15", usuario: "—", accion: "LOGIN", resultado: "FALLO" },
    { fecha: "06/11/2026 17:02", usuario: "aperez", accion: "RECUPERAR_SOLICITUD", resultado: "EXITO" },
    { fecha: "05/11/2026 11:30", usuario: "cruiz", accion: "ASIGNAR_ROL", resultado: "EXITO" },
  ],
};
