from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.test import SimpleTestCase
import os
import subprocess
import sys

from apps.usuarios.services.excepciones import ClaveDebil
from apps.usuarios.validators.clave import validar_clave


class PoliticaClaveTests(SimpleTestCase):
    def test_validador_se_importa_en_proceso_limpio_sin_ciclo(self):
        codigo = ("import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings'); "
                  "import django; django.setup(); "
                  "from apps.usuarios.validators.clave import validar_clave; "
                  "validar_clave('CooperativaTemporal2026!'); print('OK')")
        resultado = subprocess.run([sys.executable, "-c", codigo], cwd=settings.BASE_DIR,
                                   env=os.environ.copy(), capture_output=True, text=True, timeout=15)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("OK", resultado.stdout)

    def test_rechaza_claves_comunes_aunque_cumplan_longitud_y_composicion(self):
        for clave in ("password123", "Password123", "qwerty123"):
            with self.subTest(tipo="comun"), self.assertRaises(ClaveDebil):
                validar_clave(clave)

    def test_acepta_clave_no_comun(self):
        validar_clave("CooperativaTemporal2026!")

    def test_argon2id_usa_sal_individual(self):
        primero = make_password("CooperativaTemporal2026!")
        segundo = make_password("CooperativaTemporal2026!")
        self.assertTrue(primero.startswith("argon2$argon2id$"))
        self.assertNotEqual(primero, segundo)
