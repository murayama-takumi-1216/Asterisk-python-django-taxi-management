"""Signal handlers for automatic cache invalidation."""
import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.core_turno.models import TurnoConductor, TurnoOperador

from .cache_utils import (
    invalidate_conductor_report_cache,
    invalidate_operator_report_cache,
    invalidate_operator_summary_cache,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=TurnoOperador)
@receiver(post_delete, sender=TurnoOperador)
def invalidate_operator_cache_on_change(sender, instance, **kwargs):
    """Invalidate operator report caches when shift data changes."""
    try:
        # Invalidate operator shift report
        invalidate_operator_report_cache(instance.fecha_programacion)

        # Invalidate daily summary
        invalidate_operator_summary_cache(instance.fecha_programacion)

        logger.debug(
            f"Invalidated operator caches for date: {instance.fecha_programacion}"
        )
    except Exception as e:
        logger.error(
            f"Error invalidating operator cache: {e}", exc_info=True
        )


@receiver(post_save, sender=TurnoConductor)
@receiver(post_delete, sender=TurnoConductor)
def invalidate_conductor_cache_on_change(sender, instance, **kwargs):
    """Invalidate driver report caches when shift data changes."""
    try:
        # Invalidate driver shift reports for the date range
        invalidate_conductor_report_cache(
            instance.fecha_programacion, instance.fecha_fin_programacion
        )

        logger.debug(
            f"Invalidated driver caches for date: {instance.fecha_programacion}"
        )
    except Exception as e:
        logger.error(
            f"Error invalidating driver cache: {e}", exc_info=True
        )
