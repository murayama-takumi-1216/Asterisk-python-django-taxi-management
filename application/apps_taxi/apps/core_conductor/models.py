from django.db import models

from apps.common.models import AuditableModel, TimeStampedModel
from apps.core_conductor.constants import (
    CONDUCTOR_ESTADO_CHOICES,
    CONDUCTOR_ESTADO_PENDIENTE,
)


class Conductor(AuditableModel, TimeStampedModel):
    cod_conductor = models.CharField("Código", max_length=9, primary_key=True)
    nombre = models.CharField("Nombre", max_length=100)
    apellido_paterno = models.CharField(
        "Apellido Paterno", max_length=50, blank=True, null=True
    )
    apellido_materno = models.CharField(
        "Apellido Materno", max_length=50, blank=True, null=True
    )
    estado = models.CharField(
        "Estado",
        max_length=2,
        choices=CONDUCTOR_ESTADO_CHOICES,
        default=CONDUCTOR_ESTADO_PENDIENTE,
    )
    direccion = models.CharField("Direccion", max_length=100, blank=True, null=True)
    telefono = models.CharField("Telefono", max_length=20, blank=True, null=True)
    licencia = models.CharField("Licencia", max_length=15, blank=True, null=True)
    clase = models.CharField("Clase", max_length=1, blank=True, null=True)
    fecha_vencimiento = models.DateField("Vencimiento", blank=True, null=True)
    estado_eeuu = models.CharField("Estado EEUU", max_length=50, blank=True, null=True)
    alquileres_realizados = models.IntegerField("Alquiler realizados", default=0)
    alquileres_cancelados = models.IntegerField("Alquiler cancelado", default=0)

    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"
        index_together = ["estado", "nombre", "apellido_paterno"]

    def __str__(self):
        return "[{}] {} - {}".format(
            self.cod_conductor, self.nombre, self.apellido_paterno
        )

    def save(self, *arg, **kwargs):
        if not self.cod_conductor or self.cod_conductor == "vacio":
            self.cod_conductor = self.__generar_codigo()
        super().save(*arg, **kwargs)

    def __generar_codigo(self):
        prefijo = "DRI"
        codigo_new = self.__generar_codigo_nuevo_numero(prefijo)
        return "{}{}".format(prefijo, str(codigo_new).zfill(6))

    def __generar_codigo_nuevo_numero(self, prefijo):
        anterior_inst = (
            Conductor.objects.values("cod_conductor")
            .filter(cod_conductor__istartswith=prefijo)
            .order_by("-cod_conductor")
            .first()
        )
        codigo_new = 1
        if anterior_inst:
            codigo_ant = (
                anterior_inst.get("cod_conductor", "")[3:]
                if anterior_inst.get("cod_conductor")
                else "0"
            )
            codigo_new = int(codigo_ant) + 1
        return codigo_new

    @staticmethod
    def validar_licencia_unica(cod_conductor, licencia=""):
        existe = False
        if licencia:
            if cod_conductor:
                existe = (
                    Conductor.objects.filter(licencia=licencia)
                    .exclude(cod_conductor=cod_conductor)
                    .exists()
                )
            else:
                existe = Conductor.objects.filter(licencia=licencia).exists()
        return not existe

    @staticmethod
    def validar_nombre_unico(cod_conductor, nombre, apellido_paterno):
        """Validate unique name combination (nombre + apellido_paterno)"""
        if nombre and apellido_paterno:
            query = Conductor.objects.filter(
                nombre__iexact=nombre.strip(),
                apellido_paterno__iexact=apellido_paterno.strip(),
            )
            if cod_conductor:
                query = query.exclude(cod_conductor=cod_conductor)
            return not query.exists()
        return True
