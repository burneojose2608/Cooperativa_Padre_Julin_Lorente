from django.core.files.storage import default_storage
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.usuarios.models import Usuario, Rol, UsuarioRol, Permiso, RolPermiso, Auditoria, HistorialEstado
from apps.usuarios.permissions import tiene_rol
from apps.usuarios.serializers.gestion_serializers import (
    ContactoSerializer, CrearInternoSerializer, CambiarClaveSerializer, EstadoSerializer,
    RolesSerializer, PermisosSerializer,
)
from apps.usuarios.services.gestion_cuentas_service import ServicioGestionCuentas, auditar
from apps.usuarios.services.roles_service import ServicioAutorizacion
from apps.usuarios.services.usuarios_internos_service import ServicioUsuariosInternos


def validar(clase, datos):
    s = clase(data=datos)
    s.is_valid(raise_exception=True)
    return s.validated_data


def perfil(u):
    return {"id": u.pk, "username": u.username, "cedula": u.cedula, "nombre": u.nombre,
            "apellido": u.apellido, "correo": u.correo, "telefono": u.telefono,
            "fecha_nacimiento": u.fecha_nacimiento, "estado": u.estado, "tiene_foto": bool(u.foto),
            **ServicioAutorizacion.identificar_roles(u)}


class PerfilFotoView(APIView):
    def get(self, request):
        u = Usuario.objects.get(pk=request.user.pk)
        if not u.foto or not default_storage.exists(u.foto):
            from rest_framework.exceptions import NotFound
            raise NotFound("No tienes una foto de perfil.")
        respuesta = FileResponse(default_storage.open(u.foto), content_type="image/" +
                                 ("jpeg" if u.foto.endswith((".jpg", ".jpeg")) else u.foto.rsplit(".", 1)[1]))
        respuesta["X-Content-Type-Options"] = "nosniff"
        respuesta["Cache-Control"] = "no-store"
        return respuesta

    def delete(self, request):
        with transaction.atomic():
            u = Usuario.objects.select_for_update().get(pk=request.user.pk)
            vieja = u.foto
            u.foto = ""
            u.save(update_fields=["foto"])
            auditar("QUITAR_FOTO", u, u)
            transaction.on_commit(lambda: default_storage.delete(vieja) if vieja else None)
        return Response(status=204)


class CambiarClaveView(APIView):
    def post(self, request):
        ServicioGestionCuentas.cambiar_clave_autenticada(request.user, **validar(CambiarClaveSerializer, request.data))
        return Response({"mensaje": "Contraseña actualizada. Inicia sesión de nuevo."})


class AdministracionView(APIView):
    permission_classes = [tiene_rol("Administrador")]


class UsuariosView(AdministracionView):
    def get(self, request):
        consulta = Usuario.objects.all().order_by("pk")
        q = request.query_params.get("q", "").strip()[:100]
        if q:
            consulta = consulta.filter(Q(username__icontains=q) | Q(cedula__icontains=q) |
                                       Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(correo__icontains=q))
        if estado := request.query_params.get("estado"):
            consulta = consulta.filter(estado=estado)
        if rol := request.query_params.get("rol"):
            consulta = consulta.filter(roles_asignados__rol__nombre=rol).distinct()
        try:
            pagina = max(1, int(request.query_params.get("pagina", 1)))
        except ValueError:
            raise ValidationError({"pagina": "Usa un número de página."}) from None
        return Response({"total": consulta.count(), "pagina": pagina,
                         "resultados": [perfil(u) for u in consulta[(pagina-1)*20:pagina*20]]})

    def post(self, request):
        datos = validar(CrearInternoSerializer, request.data)
        if datos["rol"] == "Socio" or not Rol.objects.filter(nombre=datos["rol"]).exists():
            raise ValidationError({"rol": "Selecciona un rol interno existente."})
        try:
            with transaction.atomic():
                u = ServicioUsuariosInternos.crear_usuario_interno(**datos)
                auditar("ADMIN_CREAR_CUENTA", request.user, u, {"rol": datos["rol"]})
        except IntegrityError:
            raise ValidationError("La cédula, el usuario o el correo ya están registrados.") from None
        return Response(perfil(u), status=201)


class UsuarioDetalleView(AdministracionView):
    def get(self, request, id_usuario):
        u = get_object_or_404(Usuario, pk=id_usuario)
        datos = perfil(u)
        datos["historial"] = list(HistorialEstado.objects.filter(entidad="usuario", registro_id=u.pk)
                                 .order_by("-fecha").values("estado_anterior", "estado_nuevo", "motivo", "fecha", "usuario_id"))
        return Response(datos)

    def patch(self, request, id_usuario):
        datos = validar(ContactoSerializer, request.data)
        # La fotografía pertenece al perfil personal; el administrador edita contacto.
        if "foto" in datos:
            raise ValidationError({"foto": "La foto debe modificarla su titular."})
        u = ServicioGestionCuentas.actualizar_contacto(get_object_or_404(Usuario, pk=id_usuario),
                                                       responsable=request.user, **datos)
        return Response(perfil(u))


class UsuarioEstadoView(AdministracionView):
    def post(self, request, id_usuario):
        u = get_object_or_404(Usuario, pk=id_usuario)
        ServicioGestionCuentas.cambiar_estado(u, responsable=request.user, **validar(EstadoSerializer, request.data))
        u.refresh_from_db()
        return Response(perfil(u))


class UsuarioRolesView(AdministracionView):
    def put(self, request, id_usuario):
        u = get_object_or_404(Usuario, pk=id_usuario)
        ServicioGestionCuentas.establecer_roles(u, administrador=request.user, **validar(RolesSerializer, request.data))
        return Response(perfil(u))


class RolesView(AdministracionView):
    def get(self, request):
        return Response({"roles": [{"id": r.pk, "nombre": r.nombre,
                                    "permisos": list(RolPermiso.objects.filter(rol=r).values_list("permiso_id", flat=True))}
                                   for r in Rol.objects.order_by("pk")],
                         "permisos": [{"id": p.pk, "codigo": p.codigo, "descripcion": p.descripcion}
                                      for p in Permiso.objects.order_by("modulo", "accion")]})


class RolPermisosView(AdministracionView):
    def put(self, request, id_rol):
        ServicioGestionCuentas.establecer_permisos(get_object_or_404(Rol, pk=id_rol),
                                                  administrador=request.user, **validar(PermisosSerializer, request.data))
        return Response({"mensaje": "Permisos actualizados. Se aplican desde la siguiente petición."})


class AuditoriaView(AdministracionView):
    def get(self, request):
        return Response(list(Auditoria.objects.order_by("-fecha", "-pk")[:100].values(
            "id_auditoria", "usuario_id", "accion", "entidad", "registro_id", "resultado", "fecha", "detalle")))
