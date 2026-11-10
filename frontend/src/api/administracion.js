import { api } from "./cliente";

export const listarCuentasGenerales = (busqueda = "", pagina = 1) =>
  api.getProtegido(`/auth/administracion/cuentas-generales/?${new URLSearchParams({ q: busqueda, page: String(pagina) })}`);

export const convertirCuentaASocio = (id) =>
  api.postProtegido(`/auth/administracion/cuentas/${id}/convertir-socio/`, { confirmar_socio_activo: true });
