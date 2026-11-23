import { beforeEach, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { api } from "../api/cliente";
import { Catalogo, Puntos, Canjes, FormReferido, Reportes } from "./negocio/Modulos";
import { Comunidad, PerfilPublico, Ranking } from "./negocio/Comunidad";
import Notificaciones from "./sprint2/Notificaciones";

vi.mock("../api/cliente", () => ({
  api: { getProtegido: vi.fn(), postProtegido: vi.fn(), putProtegido: vi.fn(), post: vi.fn(), archivoProtegido: vi.fn() },
}));
vi.mock("../context/AuthContext", () => ({
  useAuth: () => ({ usuario: { nombre: "Ana", roles: ["Socio"] }, verificando: false }),
}));

beforeEach(() => {
  vi.resetAllMocks();
});

test("RNF-07 / T-042: formularios de negocio y privacidad tienen controles etiquetados y roles accesibles", async () => {
  api.getProtegido.mockResolvedValue({ alias: "Ahorrador", ranking_publico: false });
  render(<MemoryRouter><PerfilPublico /></MemoryRouter>);
  expect(await screen.findByLabelText("Alias público")).toBeInTheDocument();
  expect(screen.getByRole("checkbox", { name: /Aparecer con mi alias/ })).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Guardar preferencias" })).toBeInTheDocument();
});

test("RNF-07 / T-042: el formulario de referidos exige campos obligatorios y consentimiento etiquetado", () => {
  render(<FormReferido codigo="ABC1234567890123" publico />);
  expect(screen.getByLabelText("Nombres completos")).toBeRequired();
  expect(screen.getByLabelText("Cédula de diez dígitos")).toHaveAttribute("pattern", "[0-9]{10}");
  expect(screen.getByLabelText("Producto de interés")).toBeRequired();
  expect(screen.getByRole("checkbox")).toBeRequired();
});

test("RNF-07 / T-042: la bandeja de notificaciones expone pestañas accesibles, categoría Participación e interruptores role=switch", async () => {
  api.getProtegido.mockImplementation(async (ruta) => ruta.includes("preferencias")
    ? [
        { evento: "PUNTOS", titulo: "Puntos acreditados", canal: "INTERNA", obligatoria: false, habilitada: true },
        { evento: "CLAVE_ACTUALIZADA", titulo: "Contraseña actualizada", canal: "CORREO", obligatoria: true, habilitada: true },
      ]
    : {
        no_leidas: 1,
        resultados: [{ id: 1, evento: "PUNTOS", titulo: "Puntos acreditados", mensaje: "Recibiste 100 puntos", creada_en: "2026-11-21T00:00:00Z", leida_en: null }],
      });
  render(<MemoryRouter><Notificaciones /></MemoryRouter>);
  expect(await screen.findByRole("tab", { name: "Participación" })).toBeInTheDocument();
  const configuracion = screen.getByRole("button", { name: "Configuración" });
  expect(configuracion).toHaveAttribute("aria-expanded", "false");
  expect(api.getProtegido).not.toHaveBeenCalledWith("/plataforma/preferencias/");
  fireEvent.click(configuracion);
  expect(configuracion).toHaveAttribute("aria-expanded", "true");
  expect(await screen.findByRole("switch", { name: "Puntos acreditados · Plataforma" })).toBeEnabled();
  expect(screen.getByRole("switch", { name: "Contraseña actualizada · Correo" })).toBeDisabled();
  fireEvent.click(configuracion);
  expect(screen.queryByRole("switch")).toBeNull();
});

test("RNF-07 / T-042: reportes, canjes, puntos, comunidad y ranking renderizan encabezados y regiones accesibles", async () => {
  api.getProtegido.mockImplementation(async (ruta) => {
    if (ruta.includes("puntos")) return { saldo: 0, puntos_logro: 0, nivel: "Inicial", insignias: [], movimientos: [] };
    if (ruta.includes("ranking")) return { mi_posicion: null, resultados: [] };
    if (ruta.includes("reportes")) return { resultados: [{ indicador: "Referidos", valor: 2 }], generado_en: "2026-11-21", filtros: { tipo: "referidos" } };
    return { resultados: [], puede_gestionar: false };
  });
  const { unmount } = render(<Puntos />);
  expect(await screen.findByRole("heading", { name: "Mis puntos y logros" })).toBeInTheDocument();
  unmount();

  const r2 = render(<Ranking />);
  expect(await screen.findByRole("heading", { name: "Clasificación de socios" })).toBeInTheDocument();
  r2.unmount();

  const r3 = render(<Reportes area="marketing" />);
  expect(await screen.findByRole("region", { name: "Gráfico de actividad" })).toBeInTheDocument();
  r3.unmount();

  const r4 = render(<Canjes />);
  expect(await screen.findByLabelText("Filtrar por estado")).toBeInTheDocument();
  r4.unmount();

  const r5 = render(<Comunidad />);
  expect(await screen.findByLabelText("Tu publicación")).toBeInTheDocument();
  r5.unmount();

  render(<Catalogo recurso="campanas" />);
  expect(await screen.findByRole("heading", { name: "Campañas" })).toBeInTheDocument();
});
