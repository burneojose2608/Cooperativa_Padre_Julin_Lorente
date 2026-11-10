import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, vi } from "vitest";
import { AuthProvider, useAuth } from "./AuthContext";
import { sesion } from "../api/cliente";
import { cerrarSesion, iniciarSesion, miPerfil } from "../api/auth";
import { INACTIVIDAD_MS } from "../utils/actividad";

vi.mock("../api/auth", () => ({ cerrarSesion: vi.fn(), iniciarSesion: vi.fn(), miPerfil: vi.fn(), notificarActividad: vi.fn() }));

const cuenta = (nombre) => ({ access: `acceso-${nombre}`, refresh: `refresh-${nombre}`, usuario: { username: nombre, areas: [] } });

function Pantalla() {
  const { usuario, entrar, salir } = useAuth();
  return <><span>{usuario?.username || "sin sesión"}</span>
    <button onClick={() => entrar("nuevo", "clave")}>Entrar nuevo</button>
    <button onClick={salir}>Salir</button></>;
}

beforeEach(() => {
  vi.resetAllMocks();
  localStorage.clear();
  sesion.guardar(cuenta("anterior"));
  miPerfil.mockResolvedValue(cuenta("anterior").usuario);
  iniciarSesion.mockImplementation(async () => { const nueva = cuenta("nuevo"); sesion.guardar(nueva); return nueva; });
});

test("un cierre pendiente de la cuenta anterior no cierra una sesión nueva", async () => {
  let terminar;
  cerrarSesion.mockImplementation(() => new Promise((resolve) => { terminar = resolve; }));
  render(<AuthProvider><Pantalla /></AuthProvider>);
  await screen.findByText("anterior");
  fireEvent.click(screen.getByRole("button", { name: "Salir" }));
  fireEvent.click(screen.getByRole("button", { name: "Entrar nuevo" }));
  await screen.findByText("nuevo");
  await act(async () => terminar());
  expect(screen.getByText("nuevo")).toBeInTheDocument();
});

test("el perfil de la sesión inicial no sobrescribe un login posterior", async () => {
  let terminar;
  miPerfil.mockImplementation(() => new Promise((resolve) => { terminar = resolve; }));
  render(<AuthProvider><Pantalla /></AuthProvider>);
  fireEvent.click(screen.getByRole("button", { name: "Entrar nuevo" }));
  await screen.findByText("nuevo");
  await act(async () => terminar(cuenta("anterior").usuario));
  expect(screen.getByText("nuevo")).toBeInTheDocument();
});

test("el fallo de logout mantiene la cuenta y permite reintentar", async () => {
  cerrarSesion.mockRejectedValue(new Error("sin conexión"));
  render(<AuthProvider><Pantalla /></AuthProvider>);
  fireEvent.click(screen.getByRole("button", { name: "Salir" }));
  await waitFor(() => expect(screen.getByRole("alert")).toHaveTextContent("No se pudo confirmar"));
  expect(screen.getByText("anterior")).toBeInTheDocument();
});

test("la inactividad retira la cuenta y solicita el cierre al servidor", async () => {
  vi.useFakeTimers();
  try {
    cerrarSesion.mockResolvedValue(undefined);
    render(<AuthProvider><Pantalla /></AuthProvider>);
    await act(async () => { await Promise.resolve(); });
    await act(async () => { vi.advanceTimersByTime(INACTIVIDAD_MS); await Promise.resolve(); });
    expect(cerrarSesion).toHaveBeenCalledOnce();
    expect(screen.getByText("sin sesión")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveTextContent("15 minutos de inactividad");
    expect(sesion.leer()).toBeNull();
  } finally {
    vi.useRealTimers();
  }
});
