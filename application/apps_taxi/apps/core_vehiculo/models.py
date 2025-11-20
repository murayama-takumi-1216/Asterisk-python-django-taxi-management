from django.db import models

from apps.common.models import AuditableModel, TimeStampedModel
from apps.core_conductor.models import Conductor
from apps.core_vehiculo.constants import (
    CAR_ESTADO_ALQUILER_CHOICES,
    CAR_ESTADO_ALQUILER_NOAPLICA,
    CAR_ESTADO_CHOICES,
    CAR_ESTADO_PENDIENTE,
    ESTADO_ALQUILER_CHOICES,
    ESTADO_ALQUILER_PENDIENTE,
)


class Vehiculo(AuditableModel, TimeStampedModel):
    cod_vehiculo = models.SlugField("Código", max_length=8, primary_key=True)
    nom_vehiculo = models.SmallIntegerField("Nombre", unique=True)
    descripcion = models.CharField("Descripción", max_length=200, null=True, blank=True)
    marca = models.CharField("Marca", max_length=50, null=True, blank=True)
    modelo = models.CharField("Modelo", max_length=50, null=True, blank=True)
    matricula = models.CharField("Matrícula", max_length=8, null=True, blank=True)
    numero_vin = models.CharField("VIN", max_length=20, null=True, blank=True)
    estado_vehiculo = models.CharField(
        "Estado vehículo",
        max_length=2,
        choices=CAR_ESTADO_CHOICES,
        default=CAR_ESTADO_PENDIENTE,
    )
    estado_alquilado = models.CharField(
        "Estado alquiler",
        max_length=2,
        choices=CAR_ESTADO_ALQUILER_CHOICES,
        default=CAR_ESTADO_ALQUILER_NOAPLICA,
    )
    observacion = models.CharField(
        "Observaciones", max_length=250, blank=True, null=True
    )
    para_alquiler = models.BooleanField("Para Alquilar", default=False)

    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"
        index_together = [
            "estado_vehiculo",
            "estado_alquilado",
            "para_alquiler",
            "nom_vehiculo",
        ]

    def __str__(self):
        return "[{}]-{}".format(self.cod_vehiculo, self.nom_vehiculo)

    def save(self, *arg, **kwargs):
        if not self.cod_vehiculo or self.cod_vehiculo == "vacio":
            self.cod_vehiculo = self.__generar_codigo()
        super().save(*arg, **kwargs)

    def __generar_codigo(self):
        prefijo = "CAR"
        codigo_new = self.__generar_codigo_nuevo_numero(prefijo)
        return "{}{}".format(prefijo, str(codigo_new).zfill(5))

    def __generar_codigo_nuevo_numero(self, prefijo):
        anterior_inst = (
            Vehiculo.objects.values("cod_vehiculo")
            .filter(cod_vehiculo__istartswith=prefijo)
            .order_by("-cod_vehiculo")
            .first()
        )
        codigo_new = 1
        if anterior_inst:
            codigo_ant = (
                anterior_inst.get("cod_vehiculo", "")[3:]
                if anterior_inst.get("cod_vehiculo")
                else "0"
            )
            codigo_new = int(codigo_ant) + 1
        return codigo_new

    @staticmethod
    def validar_matricula_unica(cod_vehiculo, matricula=""):
        existe = False
        if matricula:
            if cod_vehiculo:
                existe = (
                    Vehiculo.objects.filter(matricula=matricula)
                    .exclude(cod_vehiculo=cod_vehiculo)
                    .exists()
                )
            else:
                existe = Vehiculo.objects.filter(matricula=matricula).exists()
        return not existe


class AlquilerVehiculo(AuditableModel, TimeStampedModel):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)

    # Alquiler registro
    monto_alquiler = models.DecimalField(
        "Monto alquiler", max_digits=5, decimal_places=2, default=0
    )
    fecha_prog_inicio = models.DateField(
        "Fecha programación - Inicio", blank=True
    )  # TODO Eliminar
    hora_prog_inicio = models.TimeField(
        "Hora programación - Inicio", blank=True
    )  # TODO Eliminar
    prog_fecha_hora_inicio = models.DateTimeField(
        "Programación fecha hora inicio", blank=True, null=True
    )

    fecha_prog_fin = models.DateField(
        "Fecha programación - Fin", blank=True, null=True
    )  # TODO Eliminar
    hora_prog_fin = models.TimeField(
        "Hora programación - Fin", blank=True, null=True
    )  # TODO Eliminar
    prog_fecha_hora_fin = models.DateTimeField(
        "Programación fecha hora fin", blank=True, null=True
    )

    # Alquiler inicio
    fecha_inicio = models.DateField("Fecha Inicio", blank=True, null=True)
    hora_inicio = models.TimeField("Hora inicio", blank=True, null=True)
    fecha_hora_inicio = models.DateTimeField("Fecha hora inicio", blank=True, null=True)

    fecha_fin = models.DateField("Fecha Fin", blank=True, null=True)  # TODO Eliminar
    hora_fin = models.TimeField("Hora Fin", blank=True, null=True)  # TODO Eliminar
    fecha_hora_fin = models.DateTimeField("Fecha hora fin", blank=True, null=True)

    estado = models.CharField(
        "Estado",
        max_length=2,
        choices=ESTADO_ALQUILER_CHOICES,
        default=ESTADO_ALQUILER_PENDIENTE,
    )
    entrega_radio = models.BooleanField("Entrega radio", blank=True, default=True)
    programacion_automatica = models.BooleanField(
        "Programación automática", blank=True, default=True
    )
    observacion = models.CharField(
        "Obs. servicio", max_length=250, blank=True, null=True
    )

    class Meta:
        verbose_name = "Alquiler de Vehiculo"
        verbose_name_plural = "Alquiler de Vehiculos"
        index_together = [
            "estado",
            "prog_fecha_hora_inicio",
            "prog_fecha_hora_fin",
            "fecha_hora_inicio",
            "fecha_hora_fin",
        ]

    def __str__(self):
        return "[{}]-{}".format(self.vehiculo, self.conductor)
