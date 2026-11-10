import { act, fireEvent, render } from "@testing-library/react";
import { afterEach, beforeEach, vi } from "vitest";
import useInactividad from "./useInactividad";
import { CLAVE_ACTIVIDAD, INACTIVIDAD_MS } from "../utils/actividad";

function Prueba({ activa = true, expirar, actividad }) {
  useInactividad(activa, expirar, actividad);
  return <button>Trabajar</button>;
}

beforeEach(() => { vi.useFakeTimers(); vi.setSystemTime(new Date("2026-11-10T12:00:00Z")); localStorage.clear(); });
afterEach(() => vi.useRealTimers());

test("cierra exactamente al llegar a quince minutos", () => {
  const expirar = vi.fn();
  render(<Prueba expirar={expirar} actividad={vi.fn()} />);
  act(() => vi.advanceTimersByTime(INACTIVIDAD_MS - 1));
  expect(expirar).not.toHaveBeenCalled();
  act(() => vi.advanceTimersByTime(1));
  expect(expirar).toHaveBeenCalledOnce();
});

test("actividad real aplaza el cierre y notifica sin mantener viva una pestaña inactiva", () => {
  const expirar = vi.fn(), actividad = vi.fn();
  render(<Prueba expirar={expirar} actividad={actividad} />);
  act(() => vi.advanceTimersByTime(10 * 60 * 1000));
  fireEvent.keyDown(window, { key: "a" });
  fireEvent.keyDown(window, { key: "b" });
  expect(actividad).toHaveBeenCalledOnce();
  act(() => vi.advanceTimersByTime(5 * 60 * 1000));
  expect(expirar).not.toHaveBeenCalled();
  act(() => vi.advanceTimersByTime(10 * 60 * 1000));
  expect(expirar).toHaveBeenCalledOnce();
  expect(actividad).toHaveBeenCalledOnce();
});

test("la actividad de otra pestaña aplaza el cierre sin falsificar el futuro", () => {
  const expirar = vi.fn();
  render(<Prueba expirar={expirar} actividad={vi.fn()} />);
  act(() => vi.advanceTimersByTime(10 * 60 * 1000));
  fireEvent(window, new StorageEvent("storage", { key: CLAVE_ACTIVIDAD, newValue: String(Date.now()) }));
  act(() => vi.advanceTimersByTime(5 * 60 * 1000));
  expect(expirar).not.toHaveBeenCalled();
  act(() => vi.advanceTimersByTime(10 * 60 * 1000));
  expect(expirar).toHaveBeenCalledOnce();
});

test("una cuenta cerrada no genera temporizadores de sesión", () => {
  const expirar = vi.fn();
  render(<Prueba activa={false} expirar={expirar} actividad={vi.fn()} />);
  act(() => vi.advanceTimersByTime(INACTIVIDAD_MS * 2));
  expect(expirar).not.toHaveBeenCalled();
});
