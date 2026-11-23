import { render, screen } from "@testing-library/react";
import { beforeEach, vi } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { api } from "../api/cliente";
import { useAuth } from "../context/AuthContext";
import Invitacion from "./Invitacion";

vi.mock("../api/cliente", () => ({ api: { get: vi.fn() } }));
vi.mock("../context/AuthContext", () => ({ useAuth: vi.fn() }));

beforeEach(() => {
  api.get.mockResolvedValue({ codigo: "DEMO" });
});

function mostrarInvitacion(usuario) {
  useAuth.mockReturnValue({ usuario, verificando: false });
  render(<MemoryRouter initialEntries={["/invitacion/DEMO"]}>
    <Routes><Route path="/invitacion/:codigo" element={<Invitacion />} /></Routes>
  </MemoryRouter>);
}

test("la invitación distingue la solicitud de información del registro", async () => {
  mostrarInvitacion(null);
  expect(await screen.findByRole("button", { name: "Registrar referencia" })).toBeVisible();
  expect(screen.getByRole("link", { name: "Crear mi cuenta" })).toHaveAttribute("href", "/registro");
});

test("con una sesión abierta la invitación ofrece el panel de esa cuenta", async () => {
  mostrarInvitacion({ area: "socio" });
  expect(await screen.findByRole("link", { name: "Ir a mi panel" })).toHaveAttribute("href", "/panel");
  expect(screen.queryByRole("link", { name: "Crear mi cuenta" })).toBeNull();
  expect(screen.getByRole("button", { name: "Registrar referencia" })).toBeVisible();
});
