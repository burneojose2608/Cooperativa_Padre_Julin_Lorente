import { beforeEach, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { api } from "../../api/cliente";
import { restablecerClave, solicitarRecuperacion } from "../../api/auth";
import RestablecerPage from "../../pages/RestablecerPage";
import RecuperarPage from "../../pages/RecuperarPage";
import Referido from "./Referido";
import { Publicaciones } from "./Contenidos";
import Notificaciones from "./Notificaciones";
import Perfil from "./Perfil";

vi.mock("../../api/cliente", () => ({ api: { getProtegido: vi.fn(), postProtegido: vi.fn(), putProtegido: vi.fn(), patchProtegido: vi.fn(), archivoProtegido: vi.fn() } }));
vi.mock("../../api/auth", () => ({ restablecerClave: vi.fn(), solicitarRecuperacion: vi.fn() }));
vi.mock("../../context/AuthContext", () => ({ useAuth: () => ({ usuario: { nombre: "Ana", roles: ["Socio"] }, verificando: false, refrescarPerfil: vi.fn(), salir: vi.fn() }) }));
const mostrar = (el, ruta = "/") => render(<MemoryRouter initialEntries={[ruta]}>{el}</MemoryRouter>);

beforeEach(() => { vi.resetAllMocks(); });

test("recuperación explica la consola y permite pasar al formulario del código", async () => {
  solicitarRecuperacion.mockResolvedValue({ mensaje: "Si la cuenta existe, consulta la consola del backend." });
  mostrar(<RecuperarPage />);
  fireEvent.change(screen.getByLabelText("Correo, cédula o usuario"), { target: { value: "ana2026" } });
  fireEvent.click(screen.getByRole("button", { name: "Generar código" }));
  expect(await screen.findByRole("heading", { name: "Consulta la consola del backend" })).toBeInTheDocument();
  expect(screen.getByRole("link", { name: "Ingresar el código" })).toHaveAttribute("href", "/restablecer");
});

test("restablecimiento acepta código manual y mantiene las contraseñas ocultas", async () => {
  restablecerClave.mockResolvedValue({});
  mostrar(<RestablecerPage />, "/restablecer");
  fireEvent.change(screen.getByLabelText("Código de recuperación"), { target: { value: "codigo-de-consola" } });
  fireEvent.change(screen.getByLabelText("Nueva contraseña"), { target: { value: "Nueva12345" } });
  fireEvent.change(screen.getByLabelText("Repite la contraseña"), { target: { value: "Nueva12345" } });
  expect(screen.getByLabelText("Nueva contraseña")).toHaveAttribute("type", "password");
  fireEvent.click(screen.getByRole("button", { name: "Guardar contraseña" }));
  expect(await screen.findByText("¡Contraseña actualizada!")).toBeInTheDocument();
  expect(restablecerClave).toHaveBeenCalledWith("codigo-de-consola", "Nueva12345");
});

test("un código rechazado conserva el formulario y explica el error", async () => {
  restablecerClave.mockRejectedValue(new Error("El enlace no es válido o ya venció."));
  mostrar(<RestablecerPage />, "/restablecer?token=viejo");
  fireEvent.change(screen.getByLabelText("Nueva contraseña"), { target: { value: "Nueva12345" } });
  fireEvent.change(screen.getByLabelText("Repite la contraseña"), { target: { value: "Nueva12345" } });
  fireEvent.click(screen.getByRole("button", { name: "Guardar contraseña" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("ya venció");
  expect(screen.getByLabelText("Código de recuperación")).toHaveValue("viejo");
});

test("copia el enlace persistido con confirmación visual y usa fallback al compartir", async () => {
  const writeText = vi.fn().mockResolvedValue();
  Object.defineProperty(navigator, "clipboard", { configurable: true, value: { writeText } });
  Object.defineProperty(navigator, "share", { configurable: true, value: undefined });
  api.getProtegido.mockResolvedValue({ codigo: "ABCDEF0123456789", enlace: "http://localhost:5173/invitacion/ABCDEF0123456789" });
  mostrar(<Referido />);
  fireEvent.click(await screen.findByRole("button", { name: "Copiar enlace" }));
  expect(await screen.findByRole("status")).toHaveTextContent("Copiado al portapapeles");
  fireEvent.click(screen.getByRole("button", { name: "Compartir" }));
  await waitFor(() => expect(writeText).toHaveBeenCalledTimes(2));
});

test("compartir usa el menú nativo del dispositivo", async () => {
  const share = vi.fn().mockResolvedValue();
  Object.defineProperty(navigator, "share", { configurable: true, value: share });
  api.getProtegido.mockResolvedValue({ codigo: "ABC", enlace: "https://ejemplo.com/invitacion/ABC" });
  mostrar(<Referido />);
  fireEvent.click(await screen.findByRole("button", { name: "Compartir" }));
  await waitFor(() => expect(share).toHaveBeenCalledWith(expect.objectContaining({ url: "https://ejemplo.com/invitacion/ABC" })));
});

test("publicaciones trata el HTML recibido como texto sin ejecutar ni inyectar etiquetas", async () => {
  api.getProtegido.mockResolvedValue([{ id: 1, titulo: "Aviso", cuerpo: '<img src=x onerror="alert(1)">', categoria: "Social", desde: "2026-11-17", materiales: [] }]);
  mostrar(<Publicaciones />);
  expect(await screen.findByText('<img src=x onerror="alert(1)">')).toBeInTheDocument();
  expect(document.querySelector("img")).toBeNull();
});

test("la bandeja marca una notificación propia como leída y actualiza el indicador", async () => {
  let leida = false;
  api.getProtegido.mockImplementation(async (ruta) => ruta.includes("preferencias") ? [] : ({ no_leidas: leida ? 0 : 1, resultados: [{ id: 8, titulo: "Perfil actualizado", mensaje: "Cambio", creada_en: "2026-11-17T00:00:00Z", leida_en: leida ? "2026-11-17" : null }] }));
  api.postProtegido.mockImplementation(async () => { leida = true; });
  mostrar(<Notificaciones />);
  fireEvent.click(await screen.findByRole("button", { name: "Marcar como leída" }));
  await waitFor(() => expect(screen.queryByRole("button", { name: "Marcar como leída" })).not.toBeInTheDocument());
  expect(api.postProtegido).toHaveBeenCalledWith("/plataforma/notificaciones/8/leida/", {});
  expect(screen.getByText("0 sin leer")).toBeInTheDocument();
});

test("perfil mantiene identidad sin edición y envía solo contacto autorizado", async () => {
  let perfil = { id: 1, nombre: "Ana", apellido: "Prueba", cedula: "0000000001", username: "ana2026", correo: "ana@ejemplo.com", telefono: "0991111111", fecha_nacimiento: "1995-01-01", tiene_foto: false };
  api.getProtegido.mockImplementation(async () => perfil);
  api.patchProtegido.mockImplementation(async () => { perfil = { ...perfil, telefono: "0992222222" }; return perfil; });
  mostrar(<Perfil />);
  expect(await screen.findByText("0000000001")).toBeInTheDocument();
  expect(screen.queryByRole("textbox", { name: "Cédula" })).toBeNull();
  fireEvent.change(screen.getByLabelText("Teléfono"), { target: { value: "0992222222" } });
  fireEvent.click(screen.getByRole("button", { name: "Guardar contacto" }));
  await waitFor(() => expect(api.patchProtegido).toHaveBeenCalled());
  const datos = api.patchProtegido.mock.calls[0][1];
  expect([...datos.keys()]).toEqual(["correo", "telefono"]);
  expect(datos.get("telefono")).toBe("0992222222");
  expect(await screen.findByText("Cambios guardados.")).toBeInTheDocument();
  await waitFor(() => expect(api.getProtegido).toHaveBeenCalledTimes(2));
  expect(screen.getByLabelText("Teléfono")).toHaveValue("0992222222");
  expect(screen.getByRole("status")).toHaveTextContent("Cambios guardados.");
});
