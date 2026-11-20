import { beforeEach, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { api } from "../../api/cliente";
import { restablecerClave, solicitarRecuperacion } from "../../api/auth";
import RestablecerPage from "../../pages/RestablecerPage";
import RecuperarPage from "../../pages/RecuperarPage";
import Referido from "./Referido";
import Referidos from "./Referidos";
import InicioAdmin from "./InicioAdmin";
import InicioGestor from "./InicioGestor";
import Usuarios from "./Usuarios";
import Reglas from "./Reglas";
import Roles from "./Roles";
import Auditoria from "./Auditoria";
import Materiales from "./Materiales";
import ValidarSocios from "../ValidarSocios";
import { GestionContenidos, Publicaciones } from "./Contenidos";
import Notificaciones from "./Notificaciones";
import Perfil from "./Perfil";

vi.mock("../../api/cliente", () => ({ api: { getProtegido: vi.fn(), postProtegido: vi.fn(), putProtegido: vi.fn(), patchProtegido: vi.fn(), archivoProtegido: vi.fn() } }));
vi.mock("../../api/auth", () => ({ restablecerClave: vi.fn(), solicitarRecuperacion: vi.fn() }));
vi.mock("../../context/AuthContext", () => ({ useAuth: () => ({ usuario: { nombre: "Ana", roles: ["Socio"] }, verificando: false, refrescarPerfil: vi.fn(), salir: vi.fn() }) }));
const mostrar = (el, ruta = "/") => render(<MemoryRouter initialEntries={[ruta]}>{el}</MemoryRouter>);

beforeEach(() => { vi.resetAllMocks(); });

test("contenidos del gestor filtra por estado y envía el contenido sin cambiar campos", async () => {
  api.getProtegido.mockResolvedValue([{ id: 1, titulo: "Fundamentos", cuerpo: "Texto", categoria: "Banco", tipo: "ANUNCIO", estado: "BORRADOR", visible: false, desde: "2026-08-02", hasta: null, autor: 10 }, { id: 2, titulo: "Noticia viva", cuerpo: "Otro", categoria: "Educación", tipo: "NOTICIA", estado: "PUBLICADO", visible: true, desde: "2026-01-01", hasta: null, autor: 10 }]);
  api.postProtegido.mockResolvedValue({});
  mostrar(<GestionContenidos />);
  expect(await screen.findByText("Fundamentos")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: /Publicados/ }));
  expect(screen.queryByText("Fundamentos")).not.toBeInTheDocument(); expect(screen.getByText("Noticia viva")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: /Crear contenido/ }));
  fireEvent.change(screen.getByLabelText("Título"), { target: { value: "Nuevo" } }); fireEvent.change(screen.getByLabelText("Categoría"), { target: { value: "Banco" } });
  fireEvent.change(screen.getByLabelText("Cuerpo"), { target: { value: "Cuerpo" } }); fireEvent.change(screen.getByLabelText("Mostrar desde"), { target: { value: "2026-12-01" } });
  fireEvent.click(screen.getByRole("radio", { name: "Anuncio" }));
  fireEvent.click(screen.getByRole("button", { name: "Guardar borrador" }));
  await waitFor(() => expect(api.postProtegido).toHaveBeenCalledWith("/plataforma/contenidos/", { titulo: "Nuevo", cuerpo: "Cuerpo", categoria: "Banco", tipo: "ANUNCIO", desde: "2026-12-01", hasta: null }));
});

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
  fireEvent.click(screen.getByRole("tab", { name: "Contacto" }));
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

test("perfil sube la foto sola, rechaza tipos no permitidos y pesos excesivos", async () => {
  const perfil = { id: 1, nombre: "Ana", apellido: "Prueba", cedula: "0000000001", username: "ana2026", correo: "ana@ejemplo.com", telefono: "0991111111", fecha_nacimiento: "1995-01-01", tiene_foto: false };
  api.getProtegido.mockImplementation(async () => perfil);
  api.patchProtegido.mockClear(); api.patchProtegido.mockImplementation(async () => perfil);
  mostrar(<Perfil />);
  await screen.findByText("0000000001");
  const entrada = screen.getByLabelText("Elegir foto");
  fireEvent.change(entrada, { target: { files: [new File(["x"], "a.gif", { type: "image/gif" })] } });
  expect(await screen.findByText("La foto debe ser JPG, PNG o WebP.")).toBeInTheDocument();
  const grande = new File(["x"], "g.png", { type: "image/png" }); Object.defineProperty(grande, "size", { value: 11 * 1024 * 1024 });
  fireEvent.change(entrada, { target: { files: [grande] } });
  expect(await screen.findByText("La foto no puede pesar más de 10 MB.")).toBeInTheDocument();
  expect(api.patchProtegido).not.toHaveBeenCalled();
  fireEvent.change(entrada, { target: { files: [new File(["x"], "b.png", { type: "image/png" })] } });
  await waitFor(() => expect(api.patchProtegido).toHaveBeenCalledTimes(1));
  expect([...api.patchProtegido.mock.calls[0][1].keys()]).toEqual(["foto"]);
  expect(await screen.findByText("Foto actualizada.")).toBeInTheDocument();
});

test("la bandeja filtra por categoría y marca todas las pendientes como leídas", async () => {
  const lista = [
    { id: 1, evento: "CLAVE_ACTUALIZADA", titulo: "Contraseña actualizada", mensaje: "a", creada_en: "2026-11-17T00:00:00Z", leida_en: null },
    { id: 2, evento: "SOCIO_VALIDADO", titulo: "Tu cuenta fue validada como socio", mensaje: "b", creada_en: "2026-11-16T00:00:00Z", leida_en: null },
    { id: 3, evento: "PERFIL_ACTUALIZADO", titulo: "Perfil actualizado", mensaje: "c", creada_en: "2026-11-15T00:00:00Z", leida_en: "2026-11-15" }];
  api.getProtegido.mockImplementation(async (ruta) => ruta.includes("preferencias") ? [] : ({ no_leidas: 2, resultados: lista }));
  api.postProtegido.mockClear(); api.postProtegido.mockResolvedValue({});
  mostrar(<Notificaciones />);
  await screen.findByText("Contraseña actualizada");
  fireEvent.click(screen.getByRole("tab", { name: "Seguridad" }));
  expect(screen.queryByText("Perfil actualizado")).toBeNull();
  expect(screen.getByText("Contraseña actualizada")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("tab", { name: "Todas" }));
  fireEvent.click(screen.getByRole("button", { name: "Marcar todas como leídas" }));
  await waitFor(() => expect(api.postProtegido).toHaveBeenCalledTimes(2));
  expect(api.postProtegido).toHaveBeenCalledWith("/plataforma/notificaciones/1/leida/", {});
  expect(api.postProtegido).toHaveBeenCalledWith("/plataforma/notificaciones/2/leida/", {});
});

test("mis referidos muestra el código real, copia con retroalimentación y deja la lista como próximamente", async () => {
  const writeText = vi.fn().mockResolvedValue();
  Object.defineProperty(navigator, "clipboard", { configurable: true, value: { writeText } });
  Object.defineProperty(navigator, "share", { configurable: true, value: undefined });
  api.getProtegido.mockResolvedValue({ codigo: "ABCDEF0123456789", enlace: "http://localhost:5173/invitacion/ABCDEF0123456789" });
  mostrar(<Referidos />);
  expect(await screen.findByText("ABCDEF0123456789")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Copiar código" }));
  expect(await screen.findByRole("button", { name: "¡Copiado!" })).toBeInTheDocument();
  expect(writeText).toHaveBeenCalledWith("ABCDEF0123456789");
  expect(screen.getByText("Aquí verás a las personas que invites")).toBeInTheDocument();
  expect(screen.getByLabelText("Buscar por alias o campaña")).toBeDisabled();
});

test("el inicio del administrador muestra números reales del backend y tolera que uno falle", async () => {
  const hoy = new Date().toISOString();
  api.getProtegido.mockImplementation(async (ruta) => {
    if (ruta.includes("usuarios")) return { total: 6, pagina: 1, resultados: [] };
    if (ruta.includes("cuentas-generales")) throw new Error("Función temporal deshabilitada.");
    if (ruta.includes("roles")) return { roles: [{ id: 1 }, { id: 2 }, { id: 3 }], permisos: [] };
    return [{ id_auditoria: 1, usuario_id: 4, accion: "ADMIN_CREAR_CUENTA", entidad: "usuario", registro_id: 9, resultado: "OK", fecha: hoy, detalle: {} }];
  });
  mostrar(<InicioAdmin base="/panel/admin" />);
  expect(await screen.findByText("Admin crear cuenta")).toBeInTheDocument();
  expect(screen.getByText("Usuarios activos").previousSibling).toHaveTextContent("6");
  expect(screen.getByText("Roles base").previousSibling).toHaveTextContent("3");
  expect(screen.getByText("Eventos hoy").previousSibling).toHaveTextContent("1");
  expect(screen.getByText("Socios por validar").previousSibling).toHaveTextContent("—");
  expect(screen.getByRole("link", { name: /Validar socios/ })).toHaveAttribute("href", "/panel/admin/validar-socios");
});

const CUENTA = { id: 5, username: "ana01", cedula: "1710034065", nombre: "Ana", apellido: "Perez", correo: "ana@mail.com", telefono: "0991234567", estado: "ACTIVA", roles: ["Socio"] };
function backendUsuarios() {
  api.getProtegido.mockImplementation(async (ruta) => {
    if (ruta.includes("administracion/roles")) return { roles: [{ id: 1, nombre: "Socio" }, { id: 2, nombre: "Administrador" }], permisos: [] };
    if (/usuarios\/5\/$/.test(ruta)) return { historial: [] };
    return { total: 1, pagina: 1, resultados: [CUENTA] };
  });
}

test("usuarios lista cuentas con rol y estado, y administrar abre el panel lateral con su botón de guardar", async () => {
  backendUsuarios(); api.patchProtegido.mockClear(); api.patchProtegido.mockResolvedValue({});
  mostrar(<Usuarios />);
  expect(await screen.findByText("Ana Perez")).toBeInTheDocument();
  expect(screen.getAllByText("Activa").length).toBeGreaterThan(0);
  fireEvent.click(screen.getByRole("button", { name: "Administrar a ana01" }));
  const dialogo = await screen.findByRole("dialog", { name: "Ana Perez" });
  expect(dialogo).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Teléfono"), { target: { value: "0980000000" } });
  fireEvent.click(screen.getByRole("button", { name: "Guardar contacto" }));
  await waitFor(() => expect(api.patchProtegido).toHaveBeenCalledWith("/auth/administracion/usuarios/5/", { correo: "ana@mail.com", telefono: "0980000000" }));
  fireEvent.keyDown(window, { key: "Escape" });
  await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
});

test("crear cuenta interna evita el autocompletado del navegador y solo ofrece roles internos", async () => {
  backendUsuarios(); api.postProtegido.mockClear(); api.postProtegido.mockResolvedValue({});
  mostrar(<Usuarios />);
  fireEvent.click(await screen.findByRole("button", { name: "Crear cuenta interna" }));
  expect(await screen.findByLabelText("Contraseña inicial")).toHaveAttribute("autocomplete", "new-password");
  expect(screen.getByLabelText("Usuario")).toHaveAttribute("autocomplete", "off");
  const opciones = [...screen.getByRole("dialog").querySelector("select").querySelectorAll("option")].map((o) => o.textContent);
  expect(opciones).toContain("Administrador"); expect(opciones).not.toContain("Socio");
});

test("validar socios bloquea cuentas inactivas y convierte solo tras confirmar", async () => {
  const cuentas = { count: 2, next: null, previous: null, results: [
    { id: 7, nombre: "Luis", apellido: "Mora", username: "luis7", cedula: "1100000007", estado: "ACTIVA", estado_padron: "activo" },
    { id: 8, nombre: "Eva", apellido: "Rios", username: "eva8", cedula: "1100000008", estado: "ACTIVA", estado_padron: "inactivo" }] };
  api.getProtegido.mockResolvedValue(cuentas); api.postProtegido.mockClear(); api.postProtegido.mockResolvedValue({ mensaje: "Cuenta convertida.", codigo_socio: "SOC-1" });
  mostrar(<ValidarSocios />);
  const botones = await screen.findAllByRole("button", { name: "Validar socio" });
  expect(botones[0]).toBeEnabled(); expect(botones[1]).toBeDisabled();
  fireEvent.click(botones[0]);
  const convertir = await screen.findByRole("button", { name: "Confirmar que es socio" });
  expect(convertir).toBeDisabled();
  fireEvent.click(screen.getByRole("checkbox"));
  expect(convertir).toBeEnabled(); fireEvent.click(convertir);
  await waitFor(() => expect(api.postProtegido).toHaveBeenCalledWith("/auth/administracion/cuentas/7/convertir-socio/", { confirmar_socio_activo: true }));
  expect(await screen.findByRole("status")).toHaveTextContent("Código: SOC-1");
});

test("roles y permisos guarda los permisos marcados con interruptores", async () => {
  api.getProtegido.mockResolvedValue({ roles: [{ id: 1, nombre: "Socio", permisos: [5] }], permisos: [{ id: 5, codigo: "referidos.compartir", descripcion: "Compartir código" }, { id: 6, codigo: "contenidos.gestionar", descripcion: "Gestionar contenidos" }] });
  api.putProtegido.mockClear(); api.putProtegido.mockResolvedValue({});
  mostrar(<Roles />);
  const sw = await screen.findByRole("switch", { name: "Gestionar contenidos" });
  expect(screen.getByRole("switch", { name: "Compartir código" })).toBeChecked();
  fireEvent.click(sw);
  fireEvent.click(screen.getByRole("button", { name: /Guardar permisos/ }));
  await waitFor(() => expect(api.putProtegido).toHaveBeenCalledWith("/auth/administracion/roles/1/permisos/", { permisos: [5, 6] }));
  expect(await screen.findByRole("status")).toHaveTextContent("Cambios guardados.");
});

test("reglas de puntos muestra estados y crea una versión", async () => {
  api.getProtegido.mockResolvedValue({ actividades: ["CONVERSION_REFERIDO"], reglas: [{ id: 1, version: 2, tipo_actividad: "CONVERSION_REFERIDO", puntos: 10, limite_periodo: 1, periodo: "DIA", vigente_desde: "2026-11-01", vigente_hasta: null, actual: true }, { id: 2, version: 1, tipo_actividad: "CONVERSION_REFERIDO", puntos: 5, limite_periodo: 2, periodo: "MES", vigente_desde: "2026-01-01", vigente_hasta: "2026-10-31", actual: false }] });
  api.postProtegido.mockClear(); api.postProtegido.mockResolvedValue({});
  mostrar(<Reglas />);
  expect(await screen.findByText("Vigente")).toBeInTheDocument(); expect(screen.getByText("Finalizada")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: /Crear versión/ }));
  await waitFor(() => expect(api.postProtegido).toHaveBeenCalledWith("/plataforma/reglas-puntos/", expect.objectContaining({ puntos: 10, limite_periodo: 1, vigente_hasta: null })));
});

test("inicio del gestor cuenta borradores, publicados y programados", async () => {
  api.getProtegido.mockImplementation(async (ruta) => ruta.includes("contenidos") ? [
    { id: 1, estado: "BORRADOR", visible: false, desde: "2026-01-10" }, { id: 2, estado: "PUBLICADO", visible: true, desde: "2026-02-10" },
    { id: 3, estado: "PUBLICADO", visible: false, desde: "2999-01-01" }] : { no_leidas: 0, resultados: [] });
  mostrar(<InicioGestor base="/contenidos" />);
  expect(await screen.findByText("Borradores")).toBeInTheDocument();
  await waitFor(() => expect(screen.getByText("Borradores").previousSibling).toHaveTextContent("1"));
  expect(screen.getByText("Publicados").previousSibling).toHaveTextContent("1");
  expect(screen.getByText("Programados").previousSibling).toHaveTextContent("1");
});

test("material educativo lista la biblioteca y envía el archivo con los mismos campos", async () => {
  api.getProtegido.mockResolvedValue({ materiales: [{ id: 1, titulo: "Guía", categoria: "Educación", formato: "PDF", tamano_bytes: 2048, modulos: [], contenido: null }], modulos: [] });
  api.postProtegido.mockResolvedValue({});
  mostrar(<Materiales />);
  expect(await screen.findByText("Guía")).toBeInTheDocument(); expect(screen.getByText(/2\.0 KB/)).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: /Agregar material/ }));
  fireEvent.change(screen.getByLabelText("Título del material"), { target: { value: "Nuevo" } }); fireEvent.change(screen.getByLabelText("Categoría"), { target: { value: "Banco" } });
  fireEvent.change(screen.getByLabelText(/Archivo/), { target: { files: [new File(["x"], "a.pdf", { type: "application/pdf" })] } });
  expect(await screen.findByText("a.pdf")).toBeInTheDocument();
  fireEvent.submit(document.getElementById("form-material"));
  await waitFor(() => expect(api.postProtegido).toHaveBeenCalled());
  const datos = api.postProtegido.mock.calls[0][1];
  expect(api.postProtegido.mock.calls[0][0]).toBe("/plataforma/materiales/"); expect(datos.get("titulo")).toBe("Nuevo"); expect(datos.get("categoria")).toBe("Banco"); expect(datos.get("archivo").name).toBe("a.pdf"); expect(datos.get("modulos")).toBe("[]");
});

test("auditoría muestra los eventos, filtra y abre el detalle", async () => {
  api.getProtegido.mockResolvedValue([{ id_auditoria: 1, fecha: "2026-11-20T10:00:00Z", usuario_id: 3, accion: "CAMBIAR_ESTADO", entidad: "usuario", registro_id: 9, resultado: "EXITO", detalle: { estado: "ACTIVA" } },
    { id_auditoria: 2, fecha: "2026-11-19T10:00:00Z", usuario_id: null, accion: "LOGIN", entidad: "cuenta", registro_id: 1, resultado: "FALLO", detalle: {} }]);
  mostrar(<Auditoria />);
  expect(await screen.findByText("Cambiar estado")).toBeInTheDocument(); expect(screen.getByText("Login")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Filtrar por resultado"), { target: { value: "FALLO" } });
  expect(screen.queryByText("Cambiar estado")).not.toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Filtrar por resultado"), { target: { value: "" } });
  fireEvent.click(screen.getAllByRole("button", { name: /Ver detalle/ })[0]);
  expect(await screen.findByRole("dialog")).toHaveTextContent("ACTIVA");
});
