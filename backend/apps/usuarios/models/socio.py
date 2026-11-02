from django.db import models


class Socio(models.Model):
    """Un usuario puede ser (o no) socio de la cooperativa."""

    usuario = models.OneToOneField("usuarios.Usuario", on_delete=models.DO_NOTHING,
                                   primary_key=True, db_column="id_usuario",
                                   related_name="socio")
    codigo_socio = models.CharField(max_length=20, unique=True)
    validado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "socio"
