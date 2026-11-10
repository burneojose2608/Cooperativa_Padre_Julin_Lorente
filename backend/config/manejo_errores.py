"""Convierte los errores de negocio de los servicios en respuestas JSON claras."""
import logging

from django.db import InterfaceError, OperationalError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.usuarios.services import excepciones as exc

log = logging.getLogger(__name__)

ESTADOS = {
    exc.CedulaInvalida: 400,
    exc.ClaveDebil: 400,
    exc.DatoDuplicado: 409,
    exc.CredencialesInvalidas: 401,
    exc.CuentaInactiva: 403,
    exc.CuentaBloqueada: 423,
    exc.SocioNoElegible: 403,
    exc.ConsentimientoRequerido: 400,
    exc.ServicioNoDisponible: 503,
    exc.ConversionNoAutorizada: 403,
    exc.ConversionNoPermitida: 409,
    exc.CuentaNoEncontrada: 404,
    exc.ConversionTemporalDeshabilitada: 503,
    exc.ConfirmacionDeSocioRequerida: 400,
}


def manejador_de_errores(error, contexto):
    if isinstance(error, exc.ErrorDeNegocio):
        estado = ESTADOS.get(type(error), 400)
        return Response(
            {"error": {"codigo": error.codigo, "mensaje": error.mensaje, "campo": error.campo}},
            status=estado,
        )
    respuesta = exception_handler(error, contexto)
    if respuesta is not None:
        return respuesta
    # Diagnóstico mínimo: no incluir str(error), traceback, SQL o datos de petición.
    log.error("Fallo de API no controlado; tipo=%s", type(error).__name__)
    if isinstance(error, (OperationalError, InterfaceError)):
        return Response({"error": {"codigo": "servicio_no_disponible",
                                   "mensaje": "El servicio no está disponible temporalmente. Intenta más tarde.",
                                   "campo": None}}, status=503)
    return Response({"error": {"codigo": "error_interno",
                               "mensaje": "Ocurrió un error inesperado. Intenta más tarde.",
                               "campo": None}}, status=500)
