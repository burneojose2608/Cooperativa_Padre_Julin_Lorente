from django.db import models


class Sesion(models.Model):
    """HU-015: estado revocable de una familia de tokens; no guarda tokens."""

    id_sesion = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey("usuarios.Usuario", on_delete=models.DO_NOTHING,
                                db_column="id_usuario", related_name="sesiones_api")
    vence_en = models.DateTimeField()
    revocada_en = models.DateTimeField(null=True, blank=True)
    ultimo_uso = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "sesion"
