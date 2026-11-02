from django.db import models


class Consentimiento(models.Model):
    id_consentimiento = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey("usuarios.Usuario", on_delete=models.DO_NOTHING,
                                db_column="id_usuario", related_name="consentimientos")
    version = models.CharField(max_length=20)
    fecha_aceptacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "consentimiento"
