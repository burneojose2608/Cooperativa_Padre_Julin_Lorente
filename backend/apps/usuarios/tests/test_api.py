from django.core.cache import cache
from rest_framework.test import APIClient
from django.test import TestCase

DATOS = {"cedula": "1710034065", "nombre": "Ana", "apellido": "Pérez", "correo": "ana@mail.com",
         "username": "ana01", "telefono": "0991234567", "fecha_nacimiento": "2000-05-01",
         "clave": "Clave1234"}


class ApiAuthTests(TestCase):
    def setUp(self):
        cache.clear()
        self.c = APIClient()

    def registrar(self, **cambios):
        return self.c.post("/api/auth/registro/", {**DATOS, **cambios}, format="json")

    def test_registro_201_no_devuelve_clave(self):
        r = self.registrar()
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["roles"], ["Socio"])
        self.assertTrue(r.json()["codigo_socio"].startswith("SOC-"))
        self.assertNotIn("clave", r.json())

    def test_registro_cedula_invalida_400(self):
        r = self.registrar(cedula="1710034066")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["error"]["codigo"], "cedula_invalida")

    def test_registro_cedula_duplicada_409(self):
        self.registrar()
        r = self.registrar(correo="otro@mail.com", username="otro")
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json()["error"]["campo"], "cedula")

    def test_registro_formato_invalido_400(self):
        r = self.registrar(correo="no-es-correo", telefono="abc", fecha_nacimiento="2999-01-01")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(set(r.json()), {"correo", "telefono", "fecha_nacimiento"})

    def test_login_devuelve_tokens_y_rol(self):
        self.registrar()
        r = self.c.post("/api/auth/login/", {"identificador": "ana01", "clave": "Clave1234"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["usuario"]["roles"], ["Socio"])
        self.assertIn("access", r.json())

    def test_login_incorrecto_401(self):
        self.registrar()
        r = self.c.post("/api/auth/login/", {"identificador": "ana01", "clave": "mala"}, format="json")
        self.assertEqual(r.status_code, 401)

    def test_login_bloqueado_423(self):
        self.registrar()
        for _ in range(5):
            self.c.post("/api/auth/login/", {"identificador": "ana01", "clave": "mala"}, format="json")
        r = self.c.post("/api/auth/login/", {"identificador": "ana01", "clave": "Clave1234"}, format="json")
        self.assertEqual(r.status_code, 423)

    def test_perfil_requiere_token(self):
        self.assertEqual(self.c.get("/api/auth/yo/").status_code, 401)

    def test_flujo_completo_con_token_y_refresh(self):
        self.registrar()
        login = self.c.post("/api/auth/login/", {"identificador": "1710034065", "clave": "Clave1234"},
                            format="json").json()
        self.c.credentials(HTTP_AUTHORIZATION=f"Bearer {login['access']}")
        yo = self.c.get("/api/auth/yo/")
        self.assertEqual(yo.status_code, 200)
        self.assertEqual(yo.json()["roles"], ["Socio"])
        self.c.credentials()
        nuevo = self.c.post("/api/auth/refresh/", {"refresh": login["refresh"]}, format="json")
        self.assertEqual(nuevo.status_code, 200)
        self.assertIn("access", nuevo.json())
