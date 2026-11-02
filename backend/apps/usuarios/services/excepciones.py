"""Errores de negocio. La capa de vistas los convierte en respuestas HTTP."""


class ErrorDeNegocio(Exception):
    codigo = "error"
    mensaje = "Ocurrió un error."

    def __init__(self, mensaje: str | None = None, campo: str | None = None):
        self.mensaje = mensaje or self.mensaje
        self.campo = campo
        super().__init__(self.mensaje)


class CedulaInvalida(ErrorDeNegocio):
    codigo = "cedula_invalida"
    mensaje = "La cédula ingresada no es válida."


class DatoDuplicado(ErrorDeNegocio):
    codigo = "dato_duplicado"


class ClaveDebil(ErrorDeNegocio):
    codigo = "clave_debil"
    mensaje = "La contraseña debe tener al menos 8 caracteres, con letras y números."


class CredencialesInvalidas(ErrorDeNegocio):
    codigo = "credenciales_invalidas"
    mensaje = "Usuario o contraseña incorrectos."


class CuentaBloqueada(ErrorDeNegocio):
    codigo = "cuenta_bloqueada"
    mensaje = "Cuenta bloqueada temporalmente por intentos fallidos. Intenta más tarde."


class CuentaInactiva(ErrorDeNegocio):
    codigo = "cuenta_inactiva"
    mensaje = "Tu cuenta no está activa. Comunícate con la cooperativa."
