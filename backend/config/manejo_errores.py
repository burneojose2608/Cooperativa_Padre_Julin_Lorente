"""Convierte los errores de negocio de los servicios en respuestas JSON claras."""
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.usuarios.services import excepciones as exc

ESTADOS = {
    exc.CedulaInvalida: 400,
    exc.ClaveDebil: 400,
    exc.DatoDuplicado: 409,
    exc.CredencialesInvalidas: 401,
    exc.CuentaInactiva: 403,
    exc.CuentaBloqueada: 423,
}


def manejador_de_errores(error, contexto):
    if isinstance(error, exc.ErrorDeNegocio):
        estado = ESTADOS.get(type(error), 400)
        return Response(
            {"error": {"codigo": error.codigo, "mensaje": error.mensaje, "campo": error.campo}},
            status=estado,
        )
    return exception_handler(error, contexto)
