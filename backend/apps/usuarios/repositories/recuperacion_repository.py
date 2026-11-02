from datetime import timedelta

from django.utils import timezone

from apps.usuarios.models import TokenRecuperacion


class RecuperacionRepository:
    @staticmethod
    def crear(usuario, token_hash: str, vence_en) -> TokenRecuperacion:
        return TokenRecuperacion.objects.create(usuario=usuario, token_hash=token_hash, vence_en=vence_en)

    @staticmethod
    def invalidar_pendientes(usuario) -> None:
        """Un enlace nuevo deja sin efecto los anteriores que no se usaron."""
        TokenRecuperacion.objects.filter(usuario=usuario, usado_en__isnull=True).update(usado_en=timezone.now())

    @staticmethod
    def hay_solicitud_reciente(usuario, segundos: int) -> bool:
        desde = timezone.now() - timedelta(seconds=segundos)
        return TokenRecuperacion.objects.filter(usuario=usuario, creado_en__gte=desde).exists()

    @staticmethod
    def obtener_vigente(token_hash: str):
        """El token si existe, no se usó y no ha vencido; si no, None."""
        return (TokenRecuperacion.objects.select_related("usuario")
                .filter(token_hash=token_hash, usado_en__isnull=True, vence_en__gt=timezone.now())
                .first())

    @staticmethod
    def marcar_usado(token: TokenRecuperacion) -> bool:
        """True solo para quien lo marca primero (evita usarlo dos veces a la vez)."""
        return TokenRecuperacion.objects.filter(pk=token.pk, usado_en__isnull=True).update(
            usado_en=timezone.now()) == 1
