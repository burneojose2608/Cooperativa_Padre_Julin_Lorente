"""HU-001: Registrar socio con validación de cédula."""
import re
import secrets

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.usuarios.repositories import (AuditoriaRepository, ConsentimientoRepository,
                                        RolRepository, SocioRepository, UsuarioRepository)
from apps.usuarios.validators.cedula import validar_cedula

from .excepciones import CedulaInvalida, ClaveDebil, DatoDuplicado

ROL_SOCIO = "Socio"
VERSION_POLITICA = "1.0"


def _validar_clave(clave: str) -> None:
    if len(clave) < 8 or not re.search(r"[A-Za-z]", clave) or not re.search(r"\d", clave):
        raise ClaveDebil()


def _generar_codigo_socio() -> str:
    while True:
        codigo = f"SOC-{secrets.randbelow(10**6):06d}"
        if not SocioRepository.existe_codigo(codigo):
            return codigo


def registrar_socio(*, cedula, nombre, apellido, correo, username, telefono,
                    fecha_nacimiento, clave, ip=None):
    cedula = cedula.strip()
    correo = correo.strip()
    username = username.strip()

    try:
        validar_cedula(cedula)
    except ValidationError:
        AuditoriaRepository.registrar(accion="REGISTRO", resultado="FALLO", ip=ip)
        raise CedulaInvalida(campo="cedula")

    _validar_clave(clave)

    if UsuarioRepository.existe_cedula(cedula):
        raise DatoDuplicado("Ya existe una cuenta registrada con esta cédula.", campo="cedula")
    if UsuarioRepository.existe_correo(correo):
        raise DatoDuplicado("Ya existe una cuenta registrada con este correo.", campo="correo")
    if UsuarioRepository.existe_username(username):
        raise DatoDuplicado("Este nombre de usuario ya está en uso.", campo="username")

    with transaction.atomic():  # todo o nada: usuario + socio + rol + consentimiento
        usuario = UsuarioRepository.crear(
            clave=clave, cedula=cedula, nombre=nombre.strip(), apellido=apellido.strip(),
            correo=correo, username=username, telefono=telefono.strip(),
            fecha_nacimiento=fecha_nacimiento,
        )
        SocioRepository.crear(usuario, _generar_codigo_socio())
        RolRepository.asignar(usuario, RolRepository.obtener_por_nombre(ROL_SOCIO))
        ConsentimientoRepository.registrar(usuario, VERSION_POLITICA)
        AuditoriaRepository.registrar(accion="REGISTRO", resultado="EXITO", usuario=usuario,
                                      registro_id=usuario.id_usuario, ip=ip)
    return usuario
