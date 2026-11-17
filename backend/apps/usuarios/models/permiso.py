from django.db import models


class Permiso(models.Model):
    id_permiso = models.BigAutoField(primary_key=True)
    modulo = models.CharField(max_length=50)
    accion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    @property
    def codigo(self) -> str:
        return f"{self.modulo}.{self.accion}"

    class Meta:
        managed = False
        db_table = "permiso"
        unique_together = [("modulo", "accion")]


class RolPermiso(models.Model):
    id_rol_permiso = models.BigAutoField(primary_key=True)
    rol = models.ForeignKey("usuarios.Rol", db_column="id_rol", on_delete=models.DO_NOTHING)
    permiso = models.ForeignKey(Permiso, db_column="id_permiso", on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "rol_permiso"
        unique_together = [("rol", "permiso")]


class HistorialEstado(models.Model):
    id_historial = models.BigAutoField(primary_key=True)
    entidad = models.CharField(max_length=40)
    registro_id = models.BigIntegerField()
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    usuario = models.ForeignKey("usuarios.Usuario", db_column="id_usuario", on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()

    class Meta:
        managed = False
        db_table = "historial_estado"
