import { beforeEach, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { api } from "../../api/cliente";
import { Catalogo, FormReferido, Canjes, Referidos, Reportes, Puntos } from "./Modulos";
import { Comunidad } from "./Comunidad";

vi.mock("../../api/cliente", () => ({ api: { getProtegido: vi.fn(), postProtegido: vi.fn(), putProtegido: vi.fn(), post: vi.fn(), archivoProtegido: vi.fn() } }));
beforeEach(() => { vi.resetAllMocks(); });

test("el canje conserva su clave cuando falla y permite reintentar la misma solicitud", async () => {
  api.getProtegido.mockResolvedValue({ puede_gestionar: false, resultados: [{ id: 5, nombre: "Libro", descripcion: "Lectura", costo_puntos: 70, stock: 1, condiciones: "Retiro presencial" }] });
  api.postProtegido.mockRejectedValueOnce(new Error("Conexión interrumpida")).mockResolvedValue({ id: 9 });
  render(<Catalogo recurso="beneficios" />);
  fireEvent.click(await screen.findByRole("button", { name: "Solicitar canje" }));
  fireEvent.click(screen.getByRole("checkbox"));
  fireEvent.click(screen.getByRole("button", { name: "Confirmar" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("Conexión interrumpida");
  const primera = api.postProtegido.mock.calls[0][1].clave;
  fireEvent.click(screen.getByRole("button", { name: "Confirmar" }));
  await waitFor(() => expect(api.postProtegido).toHaveBeenCalledTimes(2));
  expect(api.postProtegido.mock.calls[1][1].clave).toBe(primera);
  expect(api.postProtegido.mock.calls[1][1]).not.toHaveProperty("puntos");
});

test("un juego envía respuestas y muestra la puntuación recibida del servidor", async () => {
  api.getProtegido.mockResolvedValue({ puede_gestionar: false, resultados: [{ id: 3, nombre: "Trivia de ahorro", estado: "ACTIVO", instrucciones: "Elige una opción" }] });
  api.postProtegido.mockImplementation(async (ruta) => ruta.endsWith("iniciar/")
    ? { id: 7, preguntas: [{ enunciado: "¿Conviene ahorrar?", opciones: ["Sí", "No"] }] } : { puntuacion: "100.00" });
  render(<Catalogo recurso="juegos" />);
  fireEvent.click(await screen.findByRole("button", { name: "Iniciar partida" }));
  fireEvent.click(await screen.findByLabelText("Sí"));
  fireEvent.click(screen.getByRole("button", { name: "Enviar respuestas" }));
  expect(await screen.findByText("Puntuación: 100.00 / 100")).toBeInTheDocument();
  expect(api.postProtegido).toHaveBeenLastCalledWith("/plataforma/negocio/partidas/7/finalizar/", { respuestas: [0] });
});

test("el aula muestra el avance del servidor y habilita la evaluación al completar los módulos", async () => {
  const rutaAula = "/plataforma/negocio/capacitaciones/3/aula/";
  let avance = 50;
  api.getProtegido.mockImplementation(async (ruta) => ruta === rutaAula ? {
    titulo: "Ahorro", estado: "INSCRITO", porcentaje_avance: avance,
    nota_minima: 100, intentos_restantes: 2,
    modulos: [
      { id: 1, titulo: "Presupuesto", completado: true, materiales: [] },
      { id: 2, titulo: "Ahorro mensual", completado: avance === 100, materiales: [] },
    ],
    preguntas: [{ enunciado: "¿Conviene ahorrar?", opciones: ["Sí", "No"] }],
  } : {
    puede_gestionar: false,
    resultados: [{ id: 3, titulo: "Ahorro", estado: "PUBLICADA", requisitos: "Ser socio activo", modalidad: "VIRTUAL", duracion: 2 }],
  });
  api.postProtegido.mockImplementation(async (ruta) => {
    if (ruta.endsWith("/progreso/")) avance = 100;
    return { nota: 100, aprobado: true };
  });
  render(<Catalogo recurso="capacitaciones" />);
  expect(await screen.findByText(/Ser socio activo/)).toBeInTheDocument();
  expect(screen.getByText("2 horas")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Entrar al aula" }));
  expect(await screen.findByRole("progressbar", { name: "Avance de la capacitación" })).toHaveValue(50);
  expect(screen.queryByRole("button", { name: "Enviar respuestas" })).toBeNull();
  fireEvent.click(screen.getByRole("button", { name: "Marcar como completado" }));
  await waitFor(() => expect(screen.getByRole("progressbar")).toHaveValue(100));
  expect(api.postProtegido).toHaveBeenCalledWith("/plataforma/negocio/capacitaciones/3/progreso/", { unidad: 2 });
  fireEvent.click(screen.getByLabelText("Sí"));
  fireEvent.click(screen.getByRole("button", { name: "Enviar respuestas" }));
  expect(await screen.findByText(/tu certificado está disponible/)).toBeInTheDocument();
  expect(api.postProtegido).toHaveBeenLastCalledWith("/plataforma/negocio/capacitaciones/3/evaluar/", { respuestas: [0] });
  fireEvent.click(screen.getByRole("button", { name: /Volver a capacitaciones/ }));
  expect(screen.getByRole("heading", { name: "Capacitaciones" })).toBeInTheDocument();
  expect(screen.queryByRole("progressbar")).toBeNull();
});

test("el formulario público conserva el consentimiento y no cambia al socio del código", async () => {
  api.post.mockResolvedValue({});
  render(<FormReferido codigo="CODIGO12345678901" publico />);
  for (const [nombre, valor] of [["Nombres completos", "Persona"], ["Cédula de diez dígitos", "1234567890"], ["Correo electrónico", "persona@example.com"], ["Producto de interés", "Cuenta"]])
    fireEvent.change(screen.getByLabelText(nombre), { target: { value: valor } });
  fireEvent.click(screen.getByRole("checkbox"));
  fireEvent.click(screen.getByRole("button", { name: "Registrar referencia" }));
  await waitFor(() => expect(api.post).toHaveBeenCalled());
  expect(api.post.mock.calls[0][1]).toMatchObject({ codigo: "CODIGO12345678901", acepta_terminos: true });
  expect(api.post.mock.calls[0][1]).not.toHaveProperty("socio");
});

test("mis referidos muestra un estado vacío con el código disponible", async () => {
  api.getProtegido.mockImplementation(async (ruta) => ruta.endsWith("/codigo/")
    ? { codigo: "ABCDEF0123456789", enlace: "https://ejemplo.com/invitacion/ABCDEF0123456789" }
    : { resultados: [], puede_gestionar: false });
  render(<Referidos socio />);
  expect(await screen.findByRole("link", { name: /ABCDEF0123456789/ })).toBeInTheDocument();
  expect(screen.getByText("No hay registros para mostrar.")).toBeInTheDocument();
  expect(screen.queryByText("Próximamente")).not.toBeInTheDocument();
});

test("la comunidad presenta texto escapado y no ejecuta etiquetas del usuario", async () => {
  api.getProtegido.mockResolvedValue({ resultados: [{ id: 1, alias: "Socio", texto: '<img src=x onerror="alert(1)">', comentarios: [], reacciones: 0 }] });
  const { container } = render(<Comunidad />);
  expect(await screen.findByText('<img src=x onerror="alert(1)">')).toBeInTheDocument();
  expect(container.querySelector("img[onerror]")).toBeNull();
});

test("la comunidad reporta un comentario desde su publicación", async () => {
  api.getProtegido.mockResolvedValue({ resultados: [
    { id: 1, alias: "Socio", texto: "Una publicación", comentarios: [{ id: 2, alias: "Otro socio", texto: "Un comentario" }], reacciones: 0 },
  ] });
  api.postProtegido.mockResolvedValue({});
  render(<Comunidad />);
  fireEvent.click(await screen.findByText("Comentarios (1)"));
  fireEvent.click(screen.getByRole("button", { name: "Reportar comentario" }));
  fireEvent.change(screen.getByLabelText("Motivo del reporte"), { target: { value: "Contenido inapropiado" } });
  fireEvent.click(screen.getByRole("button", { name: "Enviar reporte" }));
  expect(await screen.findByText("Reporte enviado a moderación.")).toBeInTheDocument();
  expect(api.postProtegido).toHaveBeenCalledWith("/plataforma/negocio/comunidad/1/reportar/", {
    motivo: "Contenido inapropiado", comentario: 2,
  });
});

test("el socio consulta canjes sin controles para aprobar solicitudes", async () => {
  api.getProtegido.mockResolvedValue({ puede_gestionar: false, resultados: [{ id: 1, beneficio: "Libro", puntos: 70, estado: "PENDIENTE" }] });
  render(<Canjes />);
  expect(await screen.findByText("Libro")).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Aprobada" })).toBeNull();
});

test("el reporte de responsabilidad social utiliza su alcance y aplica las fechas", async () => {
  api.getProtegido.mockResolvedValue({ resultados: [], generado_en: "2026-11-20" });
  render(<Reportes area="rse" />);
  await waitFor(() => expect(api.getProtegido).toHaveBeenCalledWith("/plataforma/negocio/reportes/?tipo=social"));
  fireEvent.change(screen.getByLabelText("Desde"), { target: { value: "2026-11-01" } });
  fireEvent.click(screen.getByRole("button", { name: "Aplicar período" }));
  await waitFor(() => expect(api.getProtegido).toHaveBeenCalledWith("/plataforma/negocio/reportes/?tipo=social&desde=2026-11-01"));
});

test("el reporte de Marketing conserva campaña, segmento y período al descargar CSV", async () => {
  api.getProtegido.mockResolvedValue({ resultados: [], generado_en: "2026-11-20" });
  api.archivoProtegido.mockRejectedValue(new Error("Descarga interrumpida"));
  render(<Reportes area="marketing" />);
  fireEvent.change(screen.getByLabelText("Desde"), { target: { value: "2026-11-01" } });
  fireEvent.change(screen.getByLabelText("Identificador de campaña"), { target: { value: "7" } });
  fireEvent.change(screen.getByLabelText("Criterio de segmentación"), { target: { value: "AGENCIA" } });
  fireEvent.click(screen.getByRole("button", { name: "Aplicar filtros" }));
  const ruta = "/plataforma/negocio/reportes/?tipo=referidos&desde=2026-11-01&campana=7&segmento=AGENCIA";
  await waitFor(() => expect(api.getProtegido).toHaveBeenCalledWith(ruta));
  fireEvent.click(screen.getByRole("button", { name: "Descargar CSV" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("Descarga interrumpida");
  expect(api.archivoProtegido).toHaveBeenCalledWith(`${ruta}&formato=csv`);
});

test("mis puntos muestra mensaje informativo cuando el socio aún no tiene puntos ni movimientos", async () => {
  api.getProtegido.mockResolvedValue({ saldo: 0, puntos_logro: 0, nivel: "Inicial", insignias: [], movimientos: [] });
  render(<Puntos />);
  expect(await screen.findByText(/Aún no tienes puntos acumulados/)).toBeInTheDocument();
  expect(screen.getByText("No hay registros para mostrar.")).toBeInTheDocument();
});

test("el historial de sorteos muestra al personal autorizado el hash de la lista congelada y ganadores", async () => {
  api.getProtegido.mockResolvedValue({
    puede_gestionar: true, campos: [],
    resultados: [{
      id: 4, nombre: "Sorteo Anual", premio: "Tablet", estado: "EJECUTADO",
      ganadores: [{ posicion: 1, alias: "Ahorrador", suplente: false }],
      evidencia: { sha256: "a".repeat(64), elegibles: [{ participacion: 1, socio: 2 }] },
    }],
  });
  render(<Catalogo recurso="sorteos" />);
  expect(await screen.findByText("a".repeat(64))).toBeInTheDocument();
  expect(screen.getByText("Ahorrador")).toBeInTheDocument();
});
