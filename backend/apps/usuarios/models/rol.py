from django.db import models


class Rol(models.Model):
    id_rol = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=60, unique=True)

    class Meta:
        managed = False
        db_table = "rol"

    def __str__(self):
        return self.nombre


class UsuarioRol(models.Model):
    id_usuario_rol = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey("usuarios.Usuario", on_delete=models.DO_NOTHING,
                                db_column="id_usuario", related_name="roles_asignados")
    rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING, db_column="id_rol")

    class Meta:
        managed = False
        db_table = "usuario_rol"
        unique_together = [("usuario", "rol")]
