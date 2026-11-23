import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { registrar } from "../api/auth";
import FormRegistro from "./FormRegistro";

vi.mock("../api/auth", () => ({ registrar: vi.fn() }));

test("el formulario limita la fecha y rechaza el registro de menores de edad", () => {
  render(<MemoryRouter><FormRegistro alRegistrar={vi.fn()} /></MemoryRouter>);
  const fecha = screen.getByLabelText("Fecha de nacimiento");
  expect(fecha).toHaveAttribute("max", expect.stringMatching(/^\d{4}-\d{2}-\d{2}$/));
  fireEvent.change(fecha, { target: { value: new Date().toISOString().slice(0, 10) } });
  fireEvent.submit(fecha.closest("form"));
  expect(screen.getByText("Debes tener al menos 18 años para crear una cuenta.")).toBeVisible();
  expect(registrar).not.toHaveBeenCalled();
});
