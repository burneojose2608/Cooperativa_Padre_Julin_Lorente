from django.db import models


class PadronPrueba(models.Model):
    """Datos sintéticos independientes de las cuentas de la plataforma (HU-006)."""

    cedula = models.CharField(max_length=10, primary_key=True)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = "padron_prueba"
