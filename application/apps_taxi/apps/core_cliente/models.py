from django.db import models

from apps.common.models import AuditableModel, TimeStampedModel

from .constants import GENERO_CHOICES


class Cliente(AuditableModel, TimeStampedModel):
    codigo = models.SlugField("Código", max_length=12, blank=True, primary_key=True)
    telefono = models.CharField("Teléfono", max_length=15, blank=True, null=True)
    nombre = models.CharField("Nombre", max_length=60)
    apellido_paterno = models.CharField(
        "Apellido Paterno", max_length=50, blank=True, null=True
    )
    apellido_materno = models.CharField(
        "Apellido Materno", max_length=50, blank=True, null=True
    )
    correo = models.EmailField("Correo", max_length=80, blank=True, null=True)
    genero = models.CharField(
        "Genero", max_length=2, blank=True, null=True, choices=GENERO_CHOICES
    )
    estado = models.BooleanField("Estado", default=False)
    servicios_realizados = models.IntegerField("Servicios realizados", default=0)
    servicios_pendiente = models.IntegerField("Servicios pendientes", default=0)
    servicios_cancelados = models.IntegerField("Servicios cancelados", default=0)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return "[{}] {} {}".format(self.codigo, self.nombre, self.apellido_paterno)

    def save(self, *arg, **kwargs):
        if not self.codigo:
            self.codigo = self.__generar_codigo()
        super().save(*arg, **kwargs)

    def __generar_codigo(self):
        prefijo = "CLI"
        codigo_new = self.__generar_codigo_nuevo_numero(prefijo)
        return "{}{}".format(prefijo, str(codigo_new).zfill(9))

    def __generar_codigo_nuevo_numero(self, prefijo):
        anterior_inst = (
            Cliente.objects.values("codigo")
            .filter(codigo__istartswith=prefijo)
            .order_by("-codigo")
            .first()
        )
        codigo_new = 1
        if anterior_inst:
            codigo_ant = (
                anterior_inst.get("codigo", "")[3:]
                if anterior_inst.get("codigo")
                else "0"
            )
            codigo_new = int(codigo_ant) + 1
        return codigo_new


class CliRutaFrecuente(TimeStampedModel):
    rutas = models.JSONField("Rutas", blank=True, null=True)
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ruta_frecuente",
    )

    class Meta:
        verbose_name = "Ruta frecuente"
        verbose_name_plural = "Rutas frecuentes"


# Rutas [{"orden":1, "inicio":"", "fin":"", "veces":1}]
