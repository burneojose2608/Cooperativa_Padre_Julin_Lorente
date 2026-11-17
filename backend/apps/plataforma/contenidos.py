"""Servicios de contenidos y biblioteca, con autorización y archivos privados."""
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.usuarios.permissions import permisos_de
from apps.usuarios.repositories import AuditoriaRepository
from .archivos import guardar_archivo, borrar_archivo
from .models import ContenidoInstitucional, MaterialEducativo, ModuloCapacitacion, MaterialModulo
from .notificaciones import notificar_contenido


def exigir_permiso(usuario, modulo, accion):
    from apps.usuarios.repositories import RolRepository
    roles_admitidos = {"contenidos": {"Gestor de contenidos"},
                      "materiales": {"Gestor de contenidos", "Responsable de Responsabilidad Social"}}
    if modulo in roles_admitidos and not set(RolRepository.nombres_de(usuario)) & roles_admitidos[modulo]:
        raise PermissionDenied("Tu rol no está autorizado para gestionar este recurso.")
    if not usuario.is_active or not permisos_de(usuario).filter(modulo=modulo, accion=accion).exists():
        raise PermissionDenied("No tienes permiso para realizar esta operación.")


def registrar(accion, usuario, entidad):
    AuditoriaRepository.registrar(accion=accion, resultado="EXITO", usuario=usuario,
                                  entidad=entidad._meta.db_table, registro_id=entidad.pk)


@transaction.atomic
def guardar_contenido(usuario, datos, id_contenido=None):
    exigir_permiso(usuario, "contenidos", "gestionar")
    if id_contenido:
        c = ContenidoInstitucional.objects.select_for_update().get(pk=id_contenido)
        c.actualizar_datos(datos)
    else:
        c = ContenidoInstitucional.registrar_borrador(usuario, datos)
    registrar("GUARDAR_CONTENIDO", usuario, c)
    return c


@transaction.atomic
def publicar_contenido(usuario, id_contenido):
    exigir_permiso(usuario, "contenidos", "publicar")
    c = ContenidoInstitucional.objects.select_for_update().get(pk=id_contenido)
    if c.estado == "PUBLICADO":
        return c
    c.publicar(usuario)
    registrar("PUBLICAR_CONTENIDO", usuario, c)
    notificar_contenido(c)
    return c


@transaction.atomic
def retirar_contenido(usuario, id_contenido, motivo):
    exigir_permiso(usuario, "contenidos", "publicar")
    c = ContenidoInstitucional.objects.select_for_update().get(pk=id_contenido)
    c.retirar(motivo)
    registrar("RETIRAR_CONTENIDO", usuario, c)
    return c


def guardar_material(usuario, datos, id_material=None):
    exigir_permiso(usuario, "materiales", "gestionar")
    datos = dict(datos)
    cambiar_contenido = "contenido" in datos
    archivo = datos.pop("archivo", None)
    modulos = datos.pop("modulos", None)
    id_contenido = datos.pop("contenido", None)
    if modulos is not None and ModuloCapacitacion.objects.filter(pk__in=set(modulos)).count() != len(set(modulos)):
        raise ValidationError({"modulos": "Uno de los módulos no existe."})
    if id_contenido is not None:
        exigir_permiso(usuario, "contenidos", "gestionar")
        if not ContenidoInstitucional.objects.filter(pk=id_contenido).exists():
            raise ValidationError({"contenido": "El contenido no existe."})
    if not id_material and archivo is None:
        raise ValidationError({"archivo": "Adjunta un archivo."})
    ruta = None
    try:
        if archivo:
            ruta, formato, tamano = guardar_archivo(archivo, carpeta="materiales")
            datos.update(recurso=ruta, formato=formato, tamano_bytes=tamano)
        with transaction.atomic():
            material = MaterialEducativo.objects.select_for_update().get(pk=id_material) if id_material else None
            ids_contenido = {c for c in (id_contenido, material.contenido_id if material else None) if c is not None}
            # Orden único de bloqueo: material, luego contenidos por PK. Publicar también
            # bloquea el contenido, evitando retirar un adjunto mientras se publica.
            asociados = list(ContenidoInstitucional.objects.select_for_update().filter(pk__in=ids_contenido).order_by("pk"))
            if any(c.estado == "PUBLICADO" for c in asociados):
                raise ValidationError("Edita el contenido como borrador antes de modificar sus materiales.")
            if id_material:
                vieja = material.recurso
                for clave, valor in datos.items():
                    setattr(material, clave, valor)
                if cambiar_contenido:
                    material.contenido_id = id_contenido
                material.save()
                if ruta:
                    transaction.on_commit(lambda: borrar_archivo(vieja))
            else:
                material = MaterialEducativo.objects.create(autor=usuario, contenido_id=id_contenido, **datos)
            if modulos is not None:
                MaterialModulo.objects.filter(material=material).exclude(modulo_id__in=modulos).delete()
                for modulo in set(modulos):
                    MaterialModulo.objects.get_or_create(material=material, modulo_id=modulo)
            registrar("GUARDAR_MATERIAL", usuario, material)
        return material
    except Exception:
        borrar_archivo(ruta)
        raise


@transaction.atomic
def eliminar_material(usuario, id_material):
    exigir_permiso(usuario, "materiales", "gestionar")
    material = MaterialEducativo.objects.select_for_update().get(pk=id_material)
    if material.contenido_id:
        asociado = ContenidoInstitucional.objects.select_for_update().get(pk=material.contenido_id)
        if asociado.estado == "PUBLICADO":
            raise ValidationError("Retira o edita el contenido asociado antes de eliminar este material.")
    registrar("ELIMINAR_MATERIAL", usuario, material)
    ruta = material.recurso
    material.delete()
    transaction.on_commit(lambda: borrar_archivo(ruta))
