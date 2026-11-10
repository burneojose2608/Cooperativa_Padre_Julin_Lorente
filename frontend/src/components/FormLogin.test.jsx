import { act, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, vi } from "vitest";
import FormLogin from "./FormLogin";
import { useAuth } from "../context/AuthContext";

vi.mock("../context/AuthContext", () => ({ useAuth: vi.fn() }));
const entrar = vi.fn();

beforeEach(() => { entrar.mockReset(); useAuth.mockReturnValue({ entrar }); });
function mostrar() {
  render(<MemoryRouter initialEntries={["/ingresar"]}><Routes>
    <Route path="/ingresar" element={<FormLogin />} />
    <Route path="/marketing" element={<p>Panel de Marketing</p>} />
  </Routes></MemoryRouter>);
}
function completar() {
  fireEvent.change(screen.getByLabelText("Correo, cédula o usuario"), { target: { value: " correo@example.test " } });
  fireEvent.change(screen.getByLabelText("Contraseña"), { target: { value: "ClavePrueba123" } });
}

test("campos obligatorios y contraseña oculta con control accesible", () => {
  mostrar();
  expect(screen.getByLabelText("Correo, cédula o usuario")).toBeRequired();
  expect(screen.getByLabelText("Contraseña")).toHaveAttribute("type", "password");
  fireEvent.click(screen.getByRole("button", { name: "Mostrar contraseña" }));
  expect(screen.getByLabelText("Contraseña")).toHaveAttribute("type", "text");
});

test("valida obligatorios antes de enviar credenciales", () => {
  mostrar();
  fireEvent.click(screen.getByRole("button", { name: /Iniciar sesión/ }));
  expect(entrar).not.toHaveBeenCalled();
  expect(screen.getAllByRole("alert")).toHaveLength(2);
});

test("envía el identificador normalizado y muestra el rechazo genérico", async () => {
  entrar.mockRejectedValue(new Error("Usuario o contraseña incorrectos."));
  mostrar(); completar();
  fireEvent.click(screen.getByRole("button", { name: /Iniciar sesión/ }));
  expect(await screen.findByRole("alert")).toHaveTextContent("Usuario o contraseña incorrectos.");
  expect(entrar).toHaveBeenCalledWith("correo@example.test", "ClavePrueba123");
});

test("no duplica un envío pendiente y dirige al área del rol", async () => {
  let terminar;
  entrar.mockImplementation(() => new Promise((resolve) => { terminar = resolve; }));
  mostrar(); completar();
  const boton = screen.getByRole("button", { name: /Iniciar sesión/ });
  fireEvent.click(boton); fireEvent.click(boton);
  expect(entrar).toHaveBeenCalledOnce();
  expect(boton).toBeDisabled();
  await act(async () => terminar({ area: "marketing" }));
  expect(screen.getByText("Panel de Marketing")).toBeInTheDocument();
});
