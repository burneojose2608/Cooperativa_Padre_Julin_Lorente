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
    mensaje = "La cédula debe contener exactamente 10 dígitos, del 0 al 9."


class DatoDuplicado(ErrorDeNegocio):
    codigo = "dato_duplicado"


class ClaveDebil(ErrorDeNegocio):
    codigo = "clave_debil"
    mensaje = "Usa al menos 8 caracteres, con letras y números, y evita contraseñas comunes."


class CredencialesInvalidas(ErrorDeNegocio):
    codigo = "credenciales_invalidas"
    mensaje = "Usuario o contraseña incorrectos."


class CuentaBloqueada(ErrorDeNegocio):
    codigo = "cuenta_bloqueada"
    mensaje = "Cuenta bloqueada temporalmente por intentos fallidos. Intenta más tarde."


class CuentaInactiva(ErrorDeNegocio):
    codigo = "cuenta_inactiva"
    mensaje = "Tu cuenta no está activa. Comunícate con la cooperativa."


class SocioNoElegible(ErrorDeNegocio):
    codigo = "socio_no_elegible"
    mensaje = "No se pudo habilitar el registro. Comunícate con la cooperativa."


class ConsentimientoRequerido(ErrorDeNegocio):
    codigo = "consentimiento_requerido"
    mensaje = "Debes aceptar los términos y el tratamiento de datos para continuar."


class ServicioNoDisponible(ErrorDeNegocio):
    codigo = "servicio_no_disponible"
    mensaje = "El registro no está disponible temporalmente. Intenta más tarde."


class ConversionNoAutorizada(ErrorDeNegocio):
    codigo = "conversion_no_autorizada"
    mensaje = "Solo un administrador activo puede validar y convertir cuentas."


class ConversionNoPermitida(ErrorDeNegocio):
    codigo = "conversion_no_permitida"
    mensaje = "Solo se puede convertir una cuenta general activa y sin roles asignados."


class CuentaNoEncontrada(ErrorDeNegocio):
    codigo = "cuenta_no_encontrada"
    mensaje = "La cuenta indicada no existe."


class ConversionTemporalDeshabilitada(ErrorDeNegocio):
    codigo = "conversion_temporal_deshabilitada"
    mensaje = "La validación manual temporal está deshabilitada."


class ConfirmacionDeSocioRequerida(ErrorDeNegocio):
    codigo = "confirmacion_socio_requerida"
    mensaje = "Confirma que revisaste la cuenta y que la persona es socia activa."
