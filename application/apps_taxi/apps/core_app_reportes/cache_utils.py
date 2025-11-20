"""Cache utilities for reports module."""
import logging
from datetime import datetime, timedelta

from django.core.cache import cache

logger = logging.getLogger(__name__)


def invalidate_operator_report_cache(fecha_programacion=None):
    """
    Invalidate operator shift report cache for a specific date.

    Args:
        fecha_programacion: Date to invalidate (datetime or str in YYYY-MM-DD format).
                          If None, invalidates current date.
    """
    if fecha_programacion is None:
        fecha_programacion = datetime.now().date()
    elif isinstance(fecha_programacion, datetime):
        fecha_programacion = fecha_programacion.date()

    cache_key = f"reporte_turno_operador_{fecha_programacion}"
    cache.delete(cache_key)
    logger.info(f"Invalidated operator report cache: {cache_key}")


def invalidate_operator_summary_cache(fecha=None):
    """
    Invalidate operator daily summary cache for a specific date.

    Args:
        fecha: Date to invalidate (datetime or str in YYYY-MM-DD format).
              If None, invalidates current date.
    """
    if fecha is None:
        fecha = datetime.now().date()
    elif isinstance(fecha, datetime):
        fecha = fecha.date()

    cache_key = f"reporte_resumen_operadores_{fecha}"
    cache.delete(cache_key)
    logger.info(f"Invalidated operator summary cache: {cache_key}")


def invalidate_conductor_report_cache(fecha_inicio=None, fecha_fin=None):
    """
    Invalidate driver shift report cache for a date range.

    Args:
        fecha_inicio: Start date
        fecha_fin: End date
    """
    # For driver reports, we invalidate based on date range patterns
    # This is a simple pattern-based invalidation
    if fecha_inicio and fecha_fin:
        cache.delete_pattern(f"reporte_turno_conductor_*")
        logger.info("Invalidated all driver report caches")


def clear_all_report_caches():
    """Clear all report-related caches. Use with caution."""
    patterns = [
        "reporte_turno_operador_*",
        "reporte_resumen_operadores_*",
        "reporte_turno_conductor_*",
    ]
    for pattern in patterns:
        try:
            cache.delete_pattern(pattern)
            logger.info(f"Cleared cache pattern: {pattern}")
        except AttributeError:
            # delete_pattern not available in all cache backends
            logger.warning(f"Cache backend does not support delete_pattern for: {pattern}")
