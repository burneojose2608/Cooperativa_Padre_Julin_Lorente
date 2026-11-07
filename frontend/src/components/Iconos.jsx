/** Iconos en SVG (sin librerías). Heredan el color del texto con currentColor. */
const base = { viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.8,
               strokeLinecap: "round", strokeLinejoin: "round", "aria-hidden": true };

export const IcoPersona = (p) => (<svg {...base} {...p}><circle cx="12" cy="8" r="3.6" /><path d="M4.5 20c.8-3.8 3.8-5.6 7.5-5.6s6.7 1.8 7.5 5.6" /></svg>);
export const IcoCandado = (p) => (<svg {...base} {...p}><rect x="4.5" y="10.5" width="15" height="10" rx="2.4" /><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" /></svg>);
export const IcoCorreo = (p) => (<svg {...base} {...p}><rect x="3.5" y="5.5" width="17" height="13" rx="2.4" /><path d="m4.5 7.5 7.5 5.5 7.5-5.5" /></svg>);
export const IcoCedula = (p) => (<svg {...base} {...p}><rect x="3.5" y="5" width="17" height="14" rx="2.4" /><circle cx="9" cy="11" r="2" /><path d="M6.2 16c.5-1.6 1.6-2.4 2.8-2.4s2.3.8 2.8 2.4M14 10h4M14 13.5h3" /></svg>);
export const IcoTelefono = (p) => (<svg {...base} {...p}><rect x="7" y="3" width="10" height="18" rx="2.4" /><path d="M11 18h2" /></svg>);
export const IcoCalendario = (p) => (<svg {...base} {...p}><rect x="4" y="5.5" width="16" height="14.5" rx="2.4" /><path d="M8 3.5v4M16 3.5v4M4 10.5h16" /></svg>);
export const IcoArroba = (p) => (<svg {...base} {...p}><circle cx="12" cy="12" r="3.6" /><path d="M15.6 12v1.4a2.4 2.4 0 0 0 4.8 0V12a8.4 8.4 0 1 0-3.3 6.7" /></svg>);
export const IcoFlecha = (p) => (<svg {...base} strokeWidth="2.2" {...p}><path d="M5 12h14M13 6l6 6-6 6" /></svg>);
export const IcoOjo = (p) => (<svg {...base} {...p}><path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z" /><circle cx="12" cy="12" r="2.8" /></svg>);
export const IcoOjoCerrado = (p) => (<svg {...base} {...p}><path d="M3 3l18 18M10.6 5.7A9.6 9.6 0 0 1 12 5.5c6 0 9.5 6.5 9.5 6.5a16 16 0 0 1-3 3.7M6.6 7.2A16 16 0 0 0 2.5 12S6 18.5 12 18.5a9.4 9.4 0 0 0 4.2-1M9.9 9.9a2.8 2.8 0 0 0 4.2 3.7" /></svg>);

/* Iconos grandes del inicio */
export const IcoRegalo = (p) => (<svg {...base} {...p}><rect x="3.5" y="9" width="17" height="4" rx="1" /><path d="M5 13v7h14v-7M12 9v11M12 9c-1.5-4-6-4.5-6-1.8C6 9 9 9 12 9Zm0 0c1.5-4 6-4.5 6-1.8C18 9 15 9 12 9Z" /></svg>);
export const IcoMedalla = (p) => (<svg {...base} {...p}><circle cx="12" cy="9" r="5.5" /><path d="m12 6.5.9 1.9 2 .3-1.5 1.4.4 2-1.8-1-1.8 1 .4-2-1.5-1.4 2-.3ZM8.5 14l-1.5 6.5 5-2.5 5 2.5-1.5-6.5" /></svg>);
export const IcoGrupo = (p) => (<svg {...base} {...p}><circle cx="12" cy="8" r="3.2" /><circle cx="5.5" cy="9.5" r="2.4" /><circle cx="18.5" cy="9.5" r="2.4" /><path d="M6.5 19c.6-3.3 2.8-5 5.5-5s4.9 1.7 5.5 5M1.8 18c.3-2.2 1.7-3.6 3.7-3.8M22.2 18c-.3-2.2-1.7-3.6-3.7-3.8" /></svg>);
export const IcoApreton = (p) => (<svg {...base} {...p}><path d="m3 11 4-3.5 4 1.5 3.5-1.5L21 11M3 11l5 6c.8 1 2 1 2.8.2l.7-.7M21 11l-5 6c-.8 1-2 1-2.8.2M12.5 14.5 10 12M9 17.5 6.5 15" /></svg>);
export const IcoGorro = (p) => (<svg {...base} {...p}><path d="m2.5 9.5 9.5-4.5 9.5 4.5-9.5 4.5Z" /><path d="M6.5 11.5v4.2c0 1.2 2.5 2.8 5.5 2.8s5.5-1.6 5.5-2.8v-4.2M21.5 9.5v6" /></svg>);
export const IcoCopa = (p) => (<svg {...base} {...p}><path d="M7.5 4h9v5a4.5 4.5 0 0 1-9 0ZM7.5 6H4.5c0 3 1.2 4.5 3.2 4.8M16.5 6h3c0 3-1.2 4.5-3.2 4.8M12 13.5V17M8.5 20.5h7M9.5 17h5v3.5h-5Z" /></svg>);
export const IcoTelefonoGrande = (p) => (<svg {...base} {...p}><rect x="7" y="2.5" width="10" height="19" rx="2.6" /><path d="M10.5 5h3" /></svg>);
