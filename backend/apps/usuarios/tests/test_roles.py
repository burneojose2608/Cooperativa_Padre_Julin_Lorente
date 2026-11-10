from datetime import date
from io import StringIO

from django.core.cache import cache
from django.core.management import CommandError, call_command
from django.test import TestCase
from rest_framework.test import APIClient

from apps.usuarios.repositories import RolRepository, UsuarioRepository
from apps.usuarios.services import iniciar_sesion
from apps.usuarios.services.roles_service import identificar_roles
from apps.usuarios.validators.cedula import es_cedula_valida

CLAVE = "Clave1234"
_CEDULAS = [c for c in (f"11{n:08d}" for n in range(1, 400)) if es_cedula_valida(c)]


def crear(n, *roles):
    """Crea un usuario con los roles indicados (sin pasar por el registro)."""
    u = UsuarioRepository.crear(
        clave=CLAVE, cedula=_CEDULAS[n], nombre=f"Nombre{n}", apellido="Prueba",
        correo=f"u{n}@mail.com", username=f"usuario{n}", telefono="0991234567",
        fecha_nacimiento=date(1995, 1, 1),
    )
    for r in roles:
        RolRepository.asignar(u, RolRepository.obtener_por_nombre(r))
    return u


class IdentificarRolesTests(TestCase):
    def test_socio(self):
        i = identificar_roles(crear(0, "Socio"))
        self.assertEqual((i["rol_principal"], i["area"], i["areas"]), ("Socio", "socio", ["socio"]))

    def test_cada_rol_va_a_su_area(self):
        esperado = {"Administrador": "admin", "Responsable de Marketing": "marketing",
                    "Responsable de Responsabilidad Social": "rse", "Gestor de contenidos": "contenidos"}
        for n, (rol, area) in enumerate(esperado.items(), start=1):
            self.assertEqual(identificar_roles(crear(n, rol))["area"], area, rol)

    def test_varios_roles_manda_el_de_mayor_prioridad(self):
        i = identificar_roles(crear(5, "Socio", "Administrador"))
        self.assertEqual(i["rol_principal"], "Administrador")
        self.assertEqual(i["area"], "admin")
        self.assertEqual(i["areas"], ["admin", "socio"])

    def test_sin_rol(self):
        i = identificar_roles(crear(6))
        self.assertIsNone(i["area"])
        self.assertEqual((i["roles"], i["areas"]), ([], []))

    def test_login_devuelve_el_area_del_usuario(self):
        crear(7, "Administrador")
        r = iniciar_sesion(identificador="usuario7", clave=CLAVE)
        self.assertEqual((r["usuario"]["area"], r["usuario"]["rol_principal"]), ("admin", "Administrador"))


class AreasApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.c = APIClient()
        crear(10, "Socio")
        crear(11, "Administrador")

    def entrar(self, n):
        r = self.c.post("/api/auth/login/", {"identificador": f"usuario{n}", "clave": CLAVE}, format="json")
        self.c.credentials(HTTP_AUTHORIZATION=f"Bearer {r.json()['access']}")
        return r.json()

    def test_admin_puede_entrar_a_su_area(self):
        self.entrar(11)
        self.assertEqual(self.c.get("/api/auth/areas/admin/").status_code, 200)

    def test_socio_no_puede_entrar_al_area_de_admin(self):
        self.entrar(10)
        self.assertEqual(self.c.get("/api/auth/areas/admin/").status_code, 403)
        self.assertEqual(self.c.get("/api/auth/areas/socio/").status_code, 200)

    def test_area_inexistente_404_y_sin_token_401(self):
        self.entrar(10)
        self.assertEqual(self.c.get("/api/auth/areas/inventada/").status_code, 404)
        self.c.credentials()
        self.assertEqual(self.c.get("/api/auth/areas/admin/").status_code, 401)

    def test_yo_incluye_el_area(self):
        self.entrar(11)
        self.assertEqual(self.c.get("/api/auth/yo/").json()["area"], "admin")


class CrearUsuarioInternoTests(TestCase):
    def args(self, **cambios):
        base = dict(cedula=_CEDULAS[20], nombre="Ana", apellido="Pérez", correo="admin@coop.com",
                    username="admin.ana", telefono="0991234567", nacimiento="1990-05-01",
                    rol="Administrador", clave=CLAVE)
        return {**base, **cambios}

    def ejecutar(self, **cambios):
        a = self.args(**cambios)
        call_command("crear_usuario_interno", *[x for k, v in a.items() for x in (f"--{k}", v)], stdout=StringIO())

    def test_crea_administrador_que_no_es_socio_y_puede_entrar(self):
        self.ejecutar()
        r = iniciar_sesion(identificador="admin.ana", clave=CLAVE)
        self.assertEqual(r["usuario"]["area"], "admin")
        self.assertEqual(r["usuario"]["areas"], ["admin"])  # no es socio

    def test_rechaza_cedula_invalida_duplicados_rol_inexistente_y_clave_debil(self):
        with self.assertRaises(CommandError):
            self.ejecutar(cedula="17100340ab")
        self.ejecutar()
        with self.assertRaises(CommandError):
            self.ejecutar(username="otro", correo="otro@coop.com")           # cédula repetida
        with self.assertRaises(CommandError):
            self.ejecutar(cedula=_CEDULAS[21], username="otro", correo="otro@coop.com", rol="Dios")
        with self.assertRaises(CommandError):
            self.ejecutar(cedula=_CEDULAS[22], username="otro", correo="otro@coop.com", clave="corta")
