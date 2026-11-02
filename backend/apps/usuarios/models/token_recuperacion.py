from django.db import models


class TokenRecuperacion(models.Model):
    id_token = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey("usuarios.Usuario", on_delete=models.DO_NOTHING,
                                db_column="id_usuario", related_name="+")
    token_hash = models.CharField(max_length=64, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    vence_en = models.DateTimeField()
    usado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "token_recuperacion"
