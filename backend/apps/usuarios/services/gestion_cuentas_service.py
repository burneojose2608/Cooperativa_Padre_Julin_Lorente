"""Casos de uso de cuentas. Todas las mutaciones incluyen auditoría atómica."""
from __future__ import annotations

from django.core.files.uploadedfile import UploadedFile
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.usuarios.models import Usuario, Rol, UsuarioRol, RolPermiso, Permiso, Socio, HistorialEstado
from apps.usuarios.repositories import AuditoriaRepository, UsuarioRepository, RecuperacionRepository
from apps.usuarios.repositories.sesion_repository import SesionRepository
from apps.usuarios.validators.clave import validar_clave
from apps.plataforma.archivos import guardar_archivo, borrar_archivo


def exigir_administrador(usuario):
    if not Usuario.objects.filter(pk=usuario.pk, estado="ACTIVA",
                                  roles_asignados__rol__nombre="Administrador").exists():
        raise PermissionDenied("Se requiere una cuenta administradora activa.")


def auditar(accion, responsable, destino, detalle=None):
    AuditoriaRepository.registrar(accion=accion, resultado="EXITO", usuario=responsable,
                                  registro_id=destino.pk, detalle=detalle)


def bloquear_roles():
    # Evita que dos administradores retiren simultáneamente al último activo.
    list(Rol.objects.select_for_update(no_key=True).order_by("pk"))


def proteger_ultimo_administrador(usuario, *, conserva_rol=True, estado=None):
    es_admin = UsuarioRol.objects.filter(usuario=usuario, rol__nombre="Administrador").exists()
    if es_admin and (not conserva_rol or (estado or usuario.estado) != "ACTIVA"):
        otros = Usuario.objects.filter(estado="ACTIVA", roles_asignados__rol__nombre="Administrador").exclude(pk=usuario.pk)
        if not otros.exists():
            raise ValidationError("Debe permanecer al menos un administrador activo.")


class ServicioGestionCuentas:
    @staticmethod
    def actualizar_contacto(usuario: Usuario, correo: str | None = None, telefono: str | None = None,
                            foto: UploadedFile | None = None, *, responsable: Usuario | None = None) -> Usuario:
        responsable = responsable or usuario
        if responsable.pk != usuario.pk:
            exigir_administrador(responsable)
        ruta = None
        try:
            if foto is not None:
                ruta, _, _ = guardar_archivo(foto, carpeta="fotos", solo_imagen=True)
            with transaction.atomic():
                u = Usuario.objects.select_for_update().get(pk=usuario.pk)
                anterior = {"correo": u.correo, "telefono": u.telefono}
                if correo is not None:
                    u.correo = correo.strip().lower()
                    if Usuario.objects.filter(correo__iexact=u.correo).exclude(pk=u.pk).exists():
                        raise ValidationError({"correo": "Ya existe una cuenta con este correo."})
                if telefono is not None:
                    u.telefono = telefono
                if ruta:
                    vieja = u.foto
                    u.foto = ruta
                    transaction.on_commit(lambda: borrar_archivo(vieja))
                u.save(update_fields=["correo", "telefono", "foto"])
                auditar("ACTUALIZAR_CONTACTO", responsable, u, {"anterior": anterior, "foto_actualizada": bool(ruta)})
                from apps.plataforma.notificaciones import notificar
                notificar(u, "PERFIL_ACTUALIZADO", "Se actualizaron los datos de contacto de tu cuenta.")
            return u
        except Exception as error:
            borrar_archivo(ruta)
            if isinstance(error, IntegrityError):
                raise ValidationError({"correo": "El correo ya está registrado."}) from None
            raise

    @staticmethod
    @transaction.atomic
    def cambiar_clave_autenticada(usuario: Usuario, actual: str, nueva: str) -> bool:
        u = Usuario.objects.select_for_update().get(pk=usuario.pk)
        if not u.check_password(actual):
            raise ValidationError({"actual": "La contraseña actual es incorrecta."})
        validar_clave(nueva)
        if u.check_password(nueva):
            raise ValidationError({"nueva": "Elige una contraseña diferente."})
        UsuarioRepository.cambiar_clave(u, nueva)
        RecuperacionRepository.invalidar_pendientes(u)
        SesionRepository.revocar_del_usuario(u, timezone.now())
        auditar("CAMBIAR_CLAVE", u, u)
        from apps.plataforma.notificaciones import notificar
        notificar(u, "CLAVE_ACTUALIZADA", "Se cambió la contraseña de tu cuenta.")
        return True

    @staticmethod
    @transaction.atomic
    def cambiar_estado(usuario: Usuario, estado: str, motivo: str, responsable: Usuario) -> bool:
        exigir_administrador(responsable)
        if estado not in ("ACTIVA", "SUSPENDIDA", "DESACTIVADA") or not motivo.strip():
            raise ValidationError("Indica un estado válido y el motivo.")
        bloquear_roles()
        u = Usuario.objects.select_for_update().get(pk=usuario.pk)
        proteger_ultimo_administrador(u, estado=estado)
        if u.estado == estado:
            return False
        HistorialEstado.objects.create(entidad="usuario", registro_id=u.pk, estado_anterior=u.estado,
                                       estado_nuevo=estado, motivo=motivo, usuario=responsable)
        u.estado = estado
        u.save(update_fields=["estado"])
        if estado != "ACTIVA":
            SesionRepository.revocar_del_usuario(u, timezone.now())
            RecuperacionRepository.invalidar_pendientes(u)
        auditar("CAMBIAR_ESTADO", responsable, u, {"estado": estado, "motivo": motivo})
        return True

    @staticmethod
    @transaction.atomic
    def establecer_roles(usuario: Usuario, roles: list[int], administrador: Usuario) -> bool:
        exigir_administrador(administrador)
        bloquear_roles()
        u = Usuario.objects.select_for_update().get(pk=usuario.pk)
        destinos = list(Rol.objects.filter(pk__in=set(roles)))
        if len(destinos) != len(set(roles)):
            raise ValidationError({"roles": "Uno de los roles no existe."})
        nombres = {r.nombre for r in destinos}
        if "Socio" in nombres and not Socio.objects.filter(usuario=u, validado_en__isnull=False).exists():
            raise ValidationError({"roles": "Primero valida la condición de socio."})
        proteger_ultimo_administrador(u, conserva_rol="Administrador" in nombres)
        anteriores = list(UsuarioRol.objects.filter(usuario=u).values_list("rol_id", flat=True))
        UsuarioRol.objects.filter(usuario=u).exclude(rol__in=destinos).delete()
        for rol in destinos:
            UsuarioRol.objects.get_or_create(usuario=u, rol=rol)
        auditar("ASIGNAR_ROLES", administrador, u, {"antes": anteriores, "despues": list(roles)})
        return True

    @staticmethod
    def asignar_rol(usuario: Usuario, rol: Rol, administrador: Usuario) -> bool:
        with transaction.atomic():
            bloquear_roles()
            actuales = set(UsuarioRol.objects.filter(usuario=usuario).values_list("rol_id", flat=True))
            return ServicioGestionCuentas.establecer_roles(usuario, actuales | {rol.pk}, administrador)

    @staticmethod
    def revocar_rol(usuario: Usuario, rol: Rol, administrador: Usuario) -> bool:
        with transaction.atomic():
            bloquear_roles()
            actuales = set(UsuarioRol.objects.filter(usuario=usuario).values_list("rol_id", flat=True))
            return ServicioGestionCuentas.establecer_roles(usuario, actuales - {rol.pk}, administrador)

    @staticmethod
    @transaction.atomic
    def establecer_permisos(rol: Rol, permisos: list[int], administrador: Usuario) -> None:
        exigir_administrador(administrador)
        Rol.objects.select_for_update().get(pk=rol.pk)
        if Permiso.objects.filter(pk__in=set(permisos)).count() != len(set(permisos)):
            raise ValidationError({"permisos": "Uno de los permisos no existe."})
        antes = list(RolPermiso.objects.filter(rol=rol).values_list("permiso_id", flat=True))
        RolPermiso.objects.filter(rol=rol).exclude(permiso_id__in=permisos).delete()
        for permiso in set(permisos):
            RolPermiso.objects.get_or_create(rol=rol, permiso_id=permiso)
        AuditoriaRepository.registrar(accion="MODIFICAR_PERMISOS", resultado="EXITO", usuario=administrador,
                                     entidad="rol", registro_id=rol.pk, detalle={"antes": antes, "despues": list(permisos)})
