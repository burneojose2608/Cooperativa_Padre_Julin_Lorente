from django.db.models import Case, IntegerField, OuterRef, Q, Subquery, Value, When
from django.db.models.functions import Lower, Trim

from apps.usuarios.models import PadronPrueba, Usuario


class UsuarioRepository:
    @staticmethod
    def obtener_por_id(id_usuario):
        return Usuario.objects.get(pk=id_usuario)

    @staticmethod
    def obtener_para_actualizar(id_usuario):
        return Usuario.objects.select_for_update().get(pk=id_usuario)

    @staticmethod
    def listar_cuentas_generales(busqueda=""):
        cuentas = Usuario.objects.filter(socio__isnull=True, roles_asignados__isnull=True)
        if busqueda:
            cuentas = cuentas.filter(Q(username__icontains=busqueda) | Q(nombre__icontains=busqueda)
                                      | Q(apellido__icontains=busqueda) | Q(cedula__icontains=busqueda))
        return cuentas.annotate(activo_padron=Subquery(
            PadronPrueba.objects.filter(cedula=OuterRef("cedula")).values("activo")[:1]
        )).order_by("id_usuario")

    @staticmethod
    def existe_cedula(cedula: str) -> bool:
        return Usuario.objects.filter(cedula=cedula).exists()

    @staticmethod
    def existe_correo(correo: str) -> bool:
        return Usuario.objects.alias(normalizado=Lower(Trim("correo"))).filter(normalizado=correo.strip().lower()).exists()

    @staticmethod
    def existe_username(username: str) -> bool:
        return Usuario.objects.alias(normalizado=Lower(Trim("username"))).filter(normalizado=username.strip().lower()).exists()

    @staticmethod
    def buscar_por_identificador(identificador: str, *, bloquear=False):
        """Busca por cédula, correo o username (sin distinguir mayúsculas)."""
        identificador = identificador.strip()
        normalizado = identificador.lower()
        consulta = Usuario.objects.alias(
            usuario_normalizado=Lower(Trim("username")), correo_normalizado=Lower(Trim("correo")),
        ).filter(
            Q(cedula=identificador) | Q(correo_normalizado=normalizado) | Q(usuario_normalizado=normalizado)
        ).annotate(prioridad_acceso=Case(
            When(usuario_normalizado=normalizado, then=Value(0)),
            When(correo_normalizado=normalizado, then=Value(1)),
            default=Value(2), output_field=IntegerField(),
        )).order_by("prioridad_acceso", "id_usuario")
        return (consulta.select_for_update() if bloquear else consulta).first()

    @staticmethod
    def crear(*, clave: str, **datos) -> Usuario:
        usuario = Usuario(**datos)
        usuario.set_password(clave)  # se guarda cifrada, nunca en texto plano
        usuario.save()
        return usuario

    @staticmethod
    def guardar_intentos(usuario: Usuario, intentos: int, bloqueado_hasta=None) -> None:
        usuario.intentos_fallidos = intentos
        usuario.bloqueado_hasta = bloqueado_hasta
        usuario.save(update_fields=["intentos_fallidos", "bloqueado_hasta"])

    @staticmethod
    def cambiar_clave(usuario: Usuario, clave: str) -> None:
        usuario.set_password(clave)  # se guarda cifrada
        usuario.save(update_fields=["password"])
