"""Solicitud de consentimiento a prospectos, procesada fuera de la petición HTTP."""
from datetime import timedelta
from uuid import uuid4
from django.conf import settings
from django.core.mail import send_mail
from django.db import models, transaction
from django.utils import timezone
from .models import SolicitudContacto


def procesar_contacto():
    ahora=timezone.now()
    with transaction.atomic():
        solicitud=SolicitudContacto.objects.select_for_update(skip_locked=True).filter(disponible_en__lte=ahora).filter(
            models.Q(estado='PENDIENTE')|models.Q(estado='PROCESANDO',reservado_hasta__lt=ahora)).order_by('pk').first()
        if solicitud is None:return False
        if solicitud.intentos>=4:
            solicitud.estado='FALLIDA';solicitud.save(update_fields=['estado']);return True
        solicitud.estado='PROCESANDO';solicitud.intentos+=1;solicitud.reserva=uuid4()
        solicitud.reservado_hasta=ahora+timedelta(minutes=5);solicitud.save()
    p=solicitud.prospecto
    filtro=SolicitudContacto.objects.filter(pk=solicitud.pk,reserva=solicitud.reserva)
    if p.confirmado_en or not p.token_nonce or not p.expira_en or p.expira_en<=ahora:
        filtro.update(estado='OMITIDA',reserva=None,reservado_hasta=None);return True
    from .negocio import huella
    token=huella('contacto:'+p.token_nonce)
    enlace=f'{settings.FRONTEND_URL}/confirmar-referido/{token}'
    try:
        if p.correo:
            send_mail('Confirma tu referencia',f'Confirma tu consentimiento de contacto: {enlace}',
                      settings.DEFAULT_FROM_EMAIL,[p.correo],fail_silently=False)
        else:
            # Simulación local del canal telefónico; no se presenta como SMS entregado.
            print(f'Confirmación de referido por canal local: {enlace}')
        filtro.update(estado='ENVIADA',reserva=None,reservado_hasta=None)
    except Exception:
        filtro.update(estado='PENDIENTE' if solicitud.intentos<4 else 'FALLIDA',
                      disponible_en=ahora+timedelta(seconds=30*2**(solicitud.intentos-1)),reserva=None,reservado_hasta=None)
    return True
