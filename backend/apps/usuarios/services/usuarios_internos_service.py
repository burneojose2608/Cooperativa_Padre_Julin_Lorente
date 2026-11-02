"""Creación de cuentas internas (Administrador, Marketing, etc.). No son socios."""
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.usuarios.repositories import (AuditoriaRepository, RolRepository, UsuarioRepository)
from apps.usuarios.validators.cedula import validar_cedula
from apps.usuarios.validators.clave import validar_clave

from .excepciones import CedulaInvalida, DatoDuplicado


def crear_usuario_interno(*, cedula, nombre, apellido, correo, username, telefono,
                          fecha_nacimiento, clave, rol):
    try:
        validar_cedula(cedula)
    except ValidationError:
        raise CedulaInvalida(campo="cedula")
    validar_clave(clave)

    if UsuarioRepository.existe_cedula(cedula):
        raise DatoDuplicado("Ya existe una cuenta con esta cédula.", campo="cedula")
    if UsuarioRepository.existe_correo(correo):
        raise DatoDuplicado("Ya existe una cuenta con este correo.", campo="correo")
    if UsuarioRepository.existe_username(username):
        raise DatoDuplicado("Este nombre de usuario ya está en uso.", campo="username")

    rol_obj = RolRepository.obtener_por_nombre(rol)  # lanza Rol.DoesNotExist si no existe
    with transaction.atomic():
        usuario = UsuarioRepository.crear(
            clave=clave, cedula=cedula, nombre=nombre, apellido=apellido, correo=correo,
            username=username, telefono=telefono, fecha_nacimiento=fecha_nacimiento,
        )
        RolRepository.asignar(usuario, rol_obj)
        AuditoriaRepository.registrar(accion="CREAR_USUARIO_INTERNO", resultado="EXITO",
                                      usuario=usuario, registro_id=usuario.id_usuario)
    return usuario
