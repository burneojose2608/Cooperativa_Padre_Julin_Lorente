from django.db import models


class Auditoria(models.Model):
    """Bitácora de solo inserción (la base impide editar o borrar filas)."""

    id_auditoria = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey("usuarios.Usuario", null=True, blank=True,
                                on_delete=models.DO_NOTHING, db_column="id_usuario",
                                related_name="+")
    entidad = models.CharField(max_length=60)
    registro_id = models.CharField(max_length=40, null=True, blank=True)
    accion = models.CharField(max_length=60)
    fecha = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=6)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "auditoria"
