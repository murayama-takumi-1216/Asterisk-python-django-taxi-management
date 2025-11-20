import logging

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from apps.core_servicio.models import Servicio

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Servicio)
def servicios_post_save(sender, instance, created, *args, **kwargs):
    if instance:
        if instance.cliente:
            value_pendientes = Servicio.objects.filter(
                cliente=instance.cliente, turno_conductor__isnull=True, eliminado=False
            ).count()
            value_realizados = Servicio.objects.filter(
                cliente=instance.cliente, turno_conductor__isnull=False, eliminado=False
            ).count()
            try:
                instance.cliente.servicios_pendiente = value_pendientes
                instance.cliente.servicios_realizados = value_realizados
                instance.cliente.save(
                    update_fields=["servicios_pendiente", "servicios_realizados"]
                )
            except Exception as ex:
                mensaje = "Error al actualizar servicios del cliente"
                logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
