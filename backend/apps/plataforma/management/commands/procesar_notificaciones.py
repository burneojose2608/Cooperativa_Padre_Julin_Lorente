import time
from django.core.management.base import BaseCommand
from apps.plataforma.notificaciones import ServicioNotificaciones


class Command(BaseCommand):
    help = "Procesa la cola persistente de notificaciones; --continuo mantiene el trabajador activo."

    def add_arguments(self, parser):
        parser.add_argument("--continuo", action="store_true")
        parser.add_argument("--limite", type=int, default=100)

    def handle(self, *args, **opciones):
        procesadas = 0
        try:
            while True:
                hubo = ServicioNotificaciones.procesar_pendiente()
                if hubo:
                    procesadas += 1
                if not opciones["continuo"] and (not hubo or procesadas >= opciones["limite"]):
                    break
                if not hubo:
                    time.sleep(2)
        except KeyboardInterrupt:
            pass
        self.stdout.write(f"Entregas procesadas: {procesadas}")
