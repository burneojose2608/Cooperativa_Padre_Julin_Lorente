import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import AccesosPorRol from "./AccesosPorRol";

function mostrar(areas) {
  render(<MemoryRouter><AccesosPorRol usuario={{ areas }} areaActual="admin" /></MemoryRouter>);
}

test("ofrece la unión de las cinco áreas, incluidas RSE y contenidos", () => {
  mostrar(["admin", "marketing", "rse", "contenidos", "socio"]);
  const destinos = screen.getAllByRole("link").map((enlace) => enlace.getAttribute("href"));
  expect(destinos).toEqual(["/admin", "/marketing", "/responsabilidad-social", "/contenidos", "/panel"]);
  expect(screen.getByRole("link", { name: "Administración" })).toHaveAttribute("aria-current", "page");
});

test("no expone áreas que no estén asignadas ni duplica entradas", () => {
  mostrar(["marketing", "socio", "socio", "desconocida"]);
  expect(screen.getAllByRole("link")).toHaveLength(2);
  expect(screen.queryByRole("link", { name: "Administración" })).not.toBeInTheDocument();
});

test("una cuenta general no recibe accesos protegidos", () => {
  mostrar([]);
  expect(screen.queryByRole("navigation")).not.toBeInTheDocument();
});
