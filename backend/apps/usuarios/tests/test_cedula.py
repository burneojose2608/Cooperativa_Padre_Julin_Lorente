from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.usuarios.validators.cedula import es_cedula_valida, validar_cedula


class CedulaTests(SimpleTestCase):
    def test_cedulas_validas(self):
        for c in ("1710034065", "1100000007"):
            self.assertTrue(es_cedula_valida(c), c)

    def test_digito_verificador_incorrecto(self):
        self.assertFalse(es_cedula_valida("1710034066"))

    def test_longitud_y_formato(self):
        for c in ("171003406", "17100340655", "17100340ab", "", None):
            self.assertFalse(es_cedula_valida(c), c)

    def test_provincia_invalida(self):
        self.assertFalse(es_cedula_valida("2500000000"))
        self.assertFalse(es_cedula_valida("0000000000"))

    def test_tercer_digito_mayor_o_igual_a_6(self):
        self.assertFalse(es_cedula_valida("1760000000"))

    def test_validar_lanza_error(self):
        with self.assertRaises(ValidationError):
            validar_cedula("1234567890")
        validar_cedula("1710034065")  # no lanza
