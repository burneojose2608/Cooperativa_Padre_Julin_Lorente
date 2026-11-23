"""Caducidad de confirmaciones y minimización de datos con retención configurable."""
import calendar
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from apps.plataforma.models import Prospecto, Referido
from apps.plataforma.negocio import historial, auditar


class Command(BaseCommand):
    help='Revisa prospectos vencidos. --aplicar ejecuta; --solicitud ID anonimiza una solicitud de titular verificada por el operador.'
    def add_arguments(self,parser):
        parser.add_argument('--aplicar',action='store_true')
        parser.add_argument('--solicitud',type=int)

    @transaction.atomic
    def handle(self,*args,**options):
        ahora=timezone.now();meses=getattr(settings,'RETENCION_PROSPECTOS_MESES',12)
        if meses<1: raise CommandError('La retención debe ser de al menos un mes.')
        periodo=ahora.year*12+ahora.month-1-meses;year,month=divmod(periodo,12);month+=1
        corte=ahora.replace(year=year,month=month,day=min(ahora.day,calendar.monthrange(year,month)[1]))
        vencidos=Referido.objects.select_for_update(of=('self',)).filter(estado='REGISTRADO',prospecto__expira_en__lte=ahora)
        cantidad=vencidos.count()
        if options['aplicar']:
            for r in vencidos:
                historial(None,r,r.estado,'EXPIRADO','Plazo de confirmación agotado')
                r.estado='EXPIRADO';r.save(update_fields=['estado'])
        candidatos=Prospecto.objects.select_for_update().filter(creado_en__lte=corte).exclude(referido__estado='CONVERTIDO')
        if options.get('solicitud'):
            candidatos=Prospecto.objects.select_for_update().filter(pk=options['solicitud'])
        candidatos=candidatos.exclude(contacto='ANONIMIZADO')
        anonimos=candidatos.count()
        if options['aplicar']:
            for p in candidatos:
                p.nombre='Anonimizado';p.contacto='ANONIMIZADO';p.correo=None;p.telefono=None
                p.identificacion_hash=None;p.token_hash=None;p.token_nonce=None;p.producto='';p.save()
                auditar(None,p,'ANONIMIZAR_PROSPECTO',solicitud=bool(options.get('solicitud')))
        self.stdout.write(f'Confirmaciones vencidas: {cantidad}. Prospectos para anonimizar: {anonimos}. Aplicado: {options["aplicar"]}.')
