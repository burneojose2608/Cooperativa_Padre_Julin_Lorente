import { beforeEach, afterEach, vi } from "vitest";
import { api, EVENTO_SESION_CERRADA, sesion } from "./cliente";
import { cerrarSesion } from "./auth";

const respuesta = (status, cuerpo = {}) => ({ ok: status < 400, status, json: async () => cuerpo });

beforeEach(() => {
  localStorage.clear();
  sesion.guardar({ access: "acceso-prueba", refresh: "renovacion-prueba", usuario: { username: "prueba" } });
  vi.stubGlobal("fetch", vi.fn());
});
afterEach(() => vi.unstubAllGlobals());

test("logout solicita la revocación del servidor antes de borrar la sesión", async () => {
  let terminar;
  fetch.mockImplementation(() => new Promise((resolve) => { terminar = resolve; }));
  const cierre = cerrarSesion();
  expect(sesion.leer()).not.toBeNull();
  expect(fetch.mock.calls[0][0]).toContain("/auth/logout/");
  expect(fetch.mock.calls[0][1].headers.Authorization).toBe("Bearer acceso-prueba");
  terminar(respuesta(204));
  await cierre;
  expect(sesion.leer()).toBeNull();
});

test("un fallo de red al cerrar no se presenta como revocación confirmada", async () => {
  fetch.mockRejectedValue(new Error("sin red"));
  await expect(cerrarSesion()).rejects.toThrow();
  expect(sesion.leer()).not.toBeNull();
});

test("refresh rechazado retira la sesión y notifica a la interfaz", async () => {
  const evento = vi.fn();
  window.addEventListener(EVENTO_SESION_CERRADA, evento);
  fetch.mockResolvedValue(respuesta(401, { detail: "Sesión inválida" }));
  await expect(api.getProtegido("/auth/yo/")).rejects.toMatchObject({ estado: 401 });
  expect(sesion.leer()).toBeNull();
  expect(evento).toHaveBeenCalledOnce();
  window.removeEventListener(EVENTO_SESION_CERRADA, evento);
});

test("un refresh tardío no restaura una sesión cerrada", async () => {
  let terminar;
  fetch.mockResolvedValueOnce(respuesta(401)).mockImplementationOnce(() => new Promise((resolve) => { terminar = resolve; }));
  const peticion = api.getProtegido("/auth/yo/");
  await vi.waitFor(() => expect(terminar).toBeTypeOf("function"));
  sesion.borrar();
  terminar(respuesta(200, { access: "nuevo-acceso" }));
  await expect(peticion).rejects.toMatchObject({ estado: 401 });
  expect(sesion.leer()).toBeNull();
});

test("una respuesta de perfil tardía no se entrega después de cerrar la sesión", async () => {
  let terminar;
  fetch.mockImplementation(() => new Promise((resolve) => { terminar = resolve; }));
  const peticion = api.getProtegido("/auth/yo/");
  sesion.borrar();
  terminar(respuesta(200, { username: "usuario-anterior" }));
  await expect(peticion).rejects.toMatchObject({ estado: 401 });
  expect(sesion.leer()).toBeNull();
  expect(fetch).toHaveBeenCalledOnce();
});
