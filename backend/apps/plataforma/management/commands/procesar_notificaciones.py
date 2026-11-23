import time
from django.core.management.base import BaseCommand
from django.core.management import call_command
from io import StringIO
from apps.plataforma.notificaciones import ServicioNotificaciones


class Command(BaseCommand):
    help = "Procesa la cola persistente de notificaciones; --continuo mantiene el trabajador activo."

    def add_arguments(self, parser):
        parser.add_argument("--continuo", action="store_true")
        parser.add_argument("--limite", type=int, default=100)
        parser.add_argument("--mantenimiento", action="store_true", help="Caduca confirmaciones cada hora y crea un respaldo diario.")

    def handle(self, *args, **opciones):
        procesadas = 0
        ultimo_mantenimiento = None
        ultimo_respaldo = None
        try:
            while True:
                instante = time.monotonic()
                if opciones["mantenimiento"]:
                    if ultimo_mantenimiento is None or instante - ultimo_mantenimiento >= 3600:
                        call_command("mantener_prospectos", aplicar=True, stdout=StringIO())
                        ultimo_mantenimiento = instante
                    if ultimo_respaldo is None or instante - ultimo_respaldo >= 86400:
                        try:
                            call_command("respaldar_base", stdout=StringIO())
                        except Exception as error:
                            self.stderr.write(f"Respaldo pendiente: {type(error).__name__}. Revise PG_DUMP_BIN y RESPALDOS_DIR.")
                        ultimo_respaldo = instante
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
