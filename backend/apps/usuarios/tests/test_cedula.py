from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.usuarios.validators.cedula import es_cedula_valida, validar_cedula


class CedulaTests(SimpleTestCase):
    def test_acepta_cualquier_numero_de_diez_digitos(self):
        for c in ("1710034065", "1710034066", "1234567890", "0000000000", "2500000000"):
            self.assertTrue(es_cedula_valida(c), c)

    def test_longitud_y_formato(self):
        for c in ("171003406", "17100340655", "17100340ab", "1710 34065", "", None):
            self.assertFalse(es_cedula_valida(c), c)

    def test_validar_lanza_error(self):
        with self.assertRaises(ValidationError):
            validar_cedula("12345")
        validar_cedula("1234567890")  # no lanza
