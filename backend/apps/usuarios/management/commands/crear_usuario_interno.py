"""Crea una cuenta interna con un rol (Administrador, Responsable de Marketing, etc.).

Ejemplo:
  python manage.py crear_usuario_interno --cedula 1710034065 --nombre Ana --apellido Pérez \
      --correo ana@coop.com --username admin.ana --telefono 0991234567 \
      --nacimiento 1990-05-01 --rol "Administrador"
La contraseña se pide por teclado (no queda en el historial de la terminal).
"""
from datetime import date
from getpass import getpass

from django.core.management.base import BaseCommand, CommandError

from apps.usuarios.models import Rol
from apps.usuarios.services.excepciones import ErrorDeNegocio
from apps.usuarios.services.usuarios_internos_service import crear_usuario_interno


class Command(BaseCommand):
    help = "Crea una cuenta interna (no socio) con el rol indicado."

    def add_arguments(self, p):
        p.add_argument("--cedula", required=True)
        p.add_argument("--nombre", required=True)
        p.add_argument("--apellido", required=True)
        p.add_argument("--correo", required=True)
        p.add_argument("--username", required=True)
        p.add_argument("--telefono", required=True)
        p.add_argument("--nacimiento", required=True, help="AAAA-MM-DD")
        p.add_argument("--rol", required=True, help='Ej: "Administrador"')
        p.add_argument("--clave", help="Opcional. Si no se indica, se pide por teclado.")

    def handle(self, *a, **o):
        try:
            nacimiento = date.fromisoformat(o["nacimiento"])
        except ValueError:
            raise CommandError("La fecha debe tener el formato AAAA-MM-DD.")
        clave = o["clave"]
        if not clave:
            clave = getpass("Contraseña: ")
            if clave != getpass("Repite la contraseña: "):
                raise CommandError("Las contraseñas no coinciden.")
        try:
            u = crear_usuario_interno(
                cedula=o["cedula"], nombre=o["nombre"], apellido=o["apellido"], correo=o["correo"],
                username=o["username"], telefono=o["telefono"], fecha_nacimiento=nacimiento,
                clave=clave, rol=o["rol"],
            )
        except Rol.DoesNotExist:
            roles = ", ".join(Rol.objects.values_list("nombre", flat=True))
            raise CommandError(f'El rol "{o["rol"]}" no existe. Roles disponibles: {roles}')
        except ErrorDeNegocio as e:
            raise CommandError(e.mensaje)
        self.stdout.write(self.style.SUCCESS(f'Cuenta creada: {u.username} con el rol "{o["rol"]}".'))
