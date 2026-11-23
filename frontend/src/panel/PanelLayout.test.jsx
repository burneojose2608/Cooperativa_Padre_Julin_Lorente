import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { api, sesion } from "../api/cliente";
import { iniciarSesion, miPerfil } from "../api/auth";
import { AuthProvider, useAuth } from "../context/AuthContext";
import { RUTA_DE_AREA } from "../utils/areas";
import PanelLayout from "./PanelLayout";
import Perfil from "./sprint2/Perfil";

vi.mock("../api/auth", () => ({
  cerrarSesion: vi.fn(), iniciarSesion: vi.fn(), miPerfil: vi.fn(), notificarActividad: vi.fn(),
}));

const cuenta = { id: 1, nombre: "Ana", apellido: "Vega", username: "ana", roles: ["Socio"], tiene_foto: false };

function PanelDePrueba() {
  const { usuario, entrar } = useAuth();
  return usuario ? <PanelLayout area="socio"><h1>Panel</h1></PanelLayout>
    : <button onClick={() => entrar("ana", "clave")}>Ingresar</button>;
}

beforeEach(() => {
  localStorage.clear();
  sesion.guardar({ access: "sesion-prueba", refresh: "refresh-prueba", usuario: cuenta });
  miPerfil.mockResolvedValue(cuenta);
  vi.spyOn(api, "getProtegido").mockImplementation(async (ruta) => ruta === "/auth/yo/" ? miPerfil() : { no_leidas: 0, resultados: [] });
});

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
  localStorage.clear();
});

test("la navegación abre el bloque de la ruta activa y conserva Inicio a la vista", () => {
  render(<MemoryRouter initialEntries={[`${RUTA_DE_AREA.socio}/campanas`]}><AuthProvider>
    <PanelLayout area="socio"><h1>Panel</h1></PanelLayout>
  </AuthProvider></MemoryRouter>);
  const nav = screen.getByRole("navigation", { name: "Secciones del panel" });
  expect(within(nav).getByRole("link", { name: "Inicio" })).toBeVisible();
  expect(within(nav).getByRole("link", { name: "Campañas vigentes" })).toHaveAttribute("aria-current", "page");
  const formacion = within(nav).getByRole("button", { name: "Formación y juegos" });
  expect(formacion).toHaveAttribute("aria-expanded", "false");
  fireEvent.click(formacion);
  expect(formacion).toHaveAttribute("aria-expanded", "true");
  expect(within(nav).getByRole("link", { name: "Capacitaciones" })).toBeVisible();
  expect(within(nav).queryByRole("link", { name: "Campañas vigentes" })).toBeNull();
});

test("subir, reemplazar y quitar la foto del perfil actualiza la barra superior", async () => {
  const primera = new File(["primera"], "foto.png", { type: "image/png" });
  const segunda = new File(["segunda"], "nueva.png", { type: "image/png" });
  let archivo;
  const crearUrl = vi.fn((foto) => `blob:${foto.name}`);
  const liberarUrl = vi.fn();
  vi.stubGlobal("URL", class extends URL {
    static createObjectURL = crearUrl;
    static revokeObjectURL = liberarUrl;
  });
  miPerfil.mockImplementation(async () => ({ ...cuenta, tiene_foto: Boolean(archivo) }));
  vi.spyOn(api, "archivoProtegido").mockImplementation(async () => archivo);
  vi.spyOn(api, "patchProtegido").mockImplementation(async (_ruta, datos) => {
    archivo = datos.get("foto");
    return miPerfil();
  });
  vi.spyOn(api, "deleteProtegido").mockImplementation(async () => { archivo = undefined; });

  render(<MemoryRouter initialEntries={[`${RUTA_DE_AREA.socio}/perfil`]}><AuthProvider>
    <PanelLayout area="socio"><Perfil /></PanelLayout>
  </AuthProvider></MemoryRouter>);
  const perfilNavbar = within(screen.getByRole("banner")).getByRole("link", { name: "Mi perfil" });
  expect(perfilNavbar.querySelector(".avatar")).toHaveTextContent("AV");
  const entrada = await screen.findByLabelText("Elegir foto");
  fireEvent.change(entrada, { target: { files: [primera] } });
  await waitFor(() => expect(perfilNavbar.querySelector("img")).toHaveAttribute("src", "blob:foto.png"));
  fireEvent.change(entrada, { target: { files: [segunda] } });
  await waitFor(() => expect(perfilNavbar.querySelector("img")).toHaveAttribute("src", "blob:nueva.png"));
  fireEvent.click(await screen.findByRole("button", { name: "Quitar foto" }));
  await waitFor(() => expect(perfilNavbar.querySelector(".avatar")).toHaveTextContent("AV"));
  expect(liberarUrl).toHaveBeenCalledWith("blob:nueva.png");
});

test.each(["inicio de sesión", "recarga"])("el avatar guardado aparece después de %s", async (caso) => {
  const usuario = { ...cuenta, tiene_foto: true };
  miPerfil.mockResolvedValue(usuario);
  vi.stubGlobal("URL", class extends URL {
    static createObjectURL = () => "blob:guardada";
    static revokeObjectURL = vi.fn();
  });
  const descargar = vi.spyOn(api, "archivoProtegido").mockResolvedValue(new Blob(["foto"], { type: "image/png" }));
  if (caso === "inicio de sesión") {
    sesion.borrar();
    iniciarSesion.mockImplementationOnce(async () => {
      const nueva = { access: "nueva", refresh: "nuevo", usuario };
      sesion.guardar(nueva);
      return nueva;
    });
  }
  render(<MemoryRouter><AuthProvider><PanelDePrueba /></AuthProvider></MemoryRouter>);
  if (caso === "inicio de sesión") fireEvent.click(screen.getByRole("button", { name: "Ingresar" }));

  const enlace = within(await screen.findByRole("banner")).getByRole("link", { name: "Mi perfil" });
  await waitFor(() => expect(enlace.querySelector("img")).toHaveAttribute("src", "blob:guardada"));
  expect(descargar).toHaveBeenCalledWith("/auth/yo/foto/");
  expect(sesion.leer().usuario.tiene_foto).toBe(true);
});
