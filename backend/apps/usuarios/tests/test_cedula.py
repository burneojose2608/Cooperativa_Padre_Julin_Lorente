from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.usuarios.validators.cedula import es_cedula_valida, validar_cedula


class CedulaTests(SimpleTestCase):
    def test_acepta_diez_digitos_y_conserva_ceros_iniciales(self):
        for c in ("1710034065", "1100000007", "0100000009", "0100000017", "0127805968"):
            self.assertTrue(es_cedula_valida(c), c)

    def test_no_exige_verificador_provincia_ni_tercer_digito(self):
        for c in ("1710034066", "1234567890", "0000000000", "2500000000", "0160000003"):
            self.assertTrue(es_cedula_valida(c), c)

    def test_longitud_y_formato(self):
        for c in ("171003406", "17100340655", "17100340ab", "1710 34065", "1710034065\n",
                  "-123456789", "+123456789", "12345678.9", "１２３４５６７８９０", 1234567890, "", None):
            self.assertFalse(es_cedula_valida(c), c)

    def test_validar_lanza_error(self):
        with self.assertRaises(ValidationError):
            validar_cedula("12345")
        validar_cedula("0100000009")  # no lanza
