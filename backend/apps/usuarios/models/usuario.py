from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Usuario(AbstractBaseUser):
    """Tabla `usuario`. La contraseña se guarda cifrada en `clave_hash`."""

    ACTIVA, SUSPENDIDA, DESACTIVADA = "ACTIVA", "SUSPENDIDA", "DESACTIVADA"

    id_usuario = models.BigAutoField(primary_key=True)
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=254)
    password = models.CharField(max_length=255, db_column="clave_hash")
    estado = models.CharField(max_length=12, default=ACTIVA)
    creado_en = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()
    intentos_fallidos = models.SmallIntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(null=True, blank=True)

    last_login = None  # la tabla no tiene esta columna
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["cedula", "correo"]

    class Meta:
        managed = False  # la tabla la creó tu script SQL, no Django
        db_table = "usuario"

    @property
    def is_active(self) -> bool:
        return self.estado == self.ACTIVA

    @property
    def id(self):
        return self.id_usuario

    def __str__(self):
        return f"{self.username} ({self.cedula})"
