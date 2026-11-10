"""HU-001: Registrar socio con validación de cédula."""

from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError, transaction

from apps.usuarios.repositories import (AuditoriaRepository, ConsentimientoRepository,
                                        RolRepository, UsuarioRepository)
from apps.usuarios.validators.cedula import validar_cedula
from apps.usuarios.validators.clave import validar_clave
from apps.usuarios.repositories.padron_repository import EstadoPadron, Padron, PadronRepository

from .excepciones import (CedulaInvalida, ConsentimientoRequerido,
                         DatoDuplicado, ServicioNoDisponible, SocioNoElegible)
from .codigos_socio import crear_socio_validado

ROL_SOCIO = "Socio"
VERSION_POLITICA = "1.0"

RESTRICCIONES_DUPLICADO = {
    "usuario_cedula_key": "cedula",
    "uq_usuario_correo_ci": "correo",
    "uq_usuario_username_ci": "username",
    "uq_usuario_correo_normalizado": "correo",
    "uq_usuario_username_normalizado": "username",
}
MENSAJES_DUPLICADO = {
    "cedula": "Ya existe una cuenta registrada con esta cédula.",
    "correo": "Ya existe una cuenta registrada con este correo.",
    "username": "Este nombre de usuario ya está en uso.",
}


def registrar_socio(*, cedula, nombre, apellido, correo, username, telefono,
                    fecha_nacimiento, clave, acepta_terminos=False, ip=None,
                    padron: Padron | None = None):
    """Registro atómico: socio activo o cuenta general si no consta en padrón."""
    if acepta_terminos is not True:
        raise ConsentimientoRequerido(campo="acepta_terminos")
    cedula = cedula.strip() if isinstance(cedula, str) else cedula
    correo = correo.strip().lower()
    username = username.strip().lower()

    try:
        validar_cedula(cedula)
    except ValidationError:
        AuditoriaRepository.registrar(accion="REGISTRO", resultado="FALLO", ip=ip)
        raise CedulaInvalida(campo="cedula")

    validar_clave(clave)

    if UsuarioRepository.existe_cedula(cedula):
        raise DatoDuplicado(MENSAJES_DUPLICADO["cedula"], campo="cedula")
    if UsuarioRepository.existe_correo(correo):
        raise DatoDuplicado(MENSAJES_DUPLICADO["correo"], campo="correo")
    if UsuarioRepository.existe_username(username):
        raise DatoDuplicado(MENSAJES_DUPLICADO["username"], campo="username")

    adaptador_padron = padron if padron is not None else PadronRepository()
    try:
        with transaction.atomic():
            try:
                estado_padron = adaptador_padron.consultar_estado(cedula)
            except DatabaseError as error:
                raise ServicioNoDisponible() from error
            if estado_padron is EstadoPadron.INACTIVO:
                raise SocioNoElegible()
            if estado_padron not in (EstadoPadron.ACTIVO, EstadoPadron.NO_ENCONTRADO):
                raise ServicioNoDisponible()
            usuario = UsuarioRepository.crear(
                clave=clave, cedula=cedula, nombre=nombre.strip(), apellido=apellido.strip(),
                correo=correo, username=username, telefono=telefono.strip(),
                fecha_nacimiento=fecha_nacimiento,
            )
            if estado_padron is EstadoPadron.ACTIVO:
                crear_socio_validado(usuario)
                RolRepository.asignar(usuario, RolRepository.obtener_por_nombre(ROL_SOCIO))
            ConsentimientoRepository.registrar(usuario, VERSION_POLITICA)
            AuditoriaRepository.registrar(accion="REGISTRO", resultado="EXITO", usuario=usuario,
                                          registro_id=usuario.id_usuario, ip=ip)
    except IntegrityError as error:
        # La transacción ya se revirtió: no consultar dentro de un atomic roto.
        causa = error.__cause__
        restriccion = getattr(getattr(causa, "diag", None), "constraint_name", None)
        campo = RESTRICCIONES_DUPLICADO.get(restriccion)
        if getattr(causa, "sqlstate", None) == "23505" and campo:
            AuditoriaRepository.registrar(accion="REGISTRO", resultado="FALLO", ip=ip)
            raise DatoDuplicado(MENSAJES_DUPLICADO[campo], campo=campo) from error
        raise
    except SocioNoElegible:
        AuditoriaRepository.registrar(accion="REGISTRO", resultado="FALLO", ip=ip)
        raise
    return usuario
