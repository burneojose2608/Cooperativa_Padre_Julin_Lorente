from apps.usuarios.models import Sesion


class SesionRepository:
    @staticmethod
    def crear(usuario, vence_en, ahora):
        return Sesion.objects.create(usuario=usuario, vence_en=vence_en, ultimo_uso=ahora)

    @staticmethod
    def obtener_para_actualizar(id_sesion, id_usuario):
        return Sesion.objects.select_for_update().filter(pk=id_sesion, usuario_id=id_usuario).first()

    @staticmethod
    def guardar(sesion, campos):
        sesion.save(update_fields=campos)

    @staticmethod
    def revocar_del_usuario(usuario, ahora):
        return Sesion.objects.filter(usuario=usuario, revocada_en__isnull=True).update(revocada_en=ahora)
