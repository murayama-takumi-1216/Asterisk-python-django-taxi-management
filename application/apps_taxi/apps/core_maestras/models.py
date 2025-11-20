from django.db import models

from apps.common.models import AuditableModel, TimeStampedModel
from apps.core_maestras.constants import DIA_SEMANA_CHOICES


class Horario(AuditableModel, TimeStampedModel):
    cod_horario = models.CharField("Código", max_length=2, primary_key=True)
    nom_horario = models.CharField("Nombre", max_length=20)
    inicio_horario = models.TimeField("Incio", blank=True, null=True)
    fin_horario = models.TimeField("Fin", blank=True, null=True)
    orden_view = models.SmallIntegerField("Orden vista", blank=True, null=True)
    estado = models.BooleanField("Estado", default=False)
    horario_base = models.BooleanField("Horario Base", default=False)

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horario"
        index_together = ["estado", "horario_base"]

    def __str__(self):
        return "[{}-{}] {}".format(
            self.inicio_horario, self.fin_horario, self.nom_horario
        )


class GrupoHorario(AuditableModel, TimeStampedModel):
    codigo = models.CharField("Código", max_length=5, primary_key=True)
    nombre = models.CharField("Nombre", max_length=20, blank=True)
    descripcion = models.CharField("Descripción", max_length=250, blank=True, null=True)
    estado = models.BooleanField("Estado", default=False)
    confirmado = models.BooleanField("Confirmado", default=False)

    class Meta:
        verbose_name = "Grupo de Horario"
        verbose_name_plural = "Grupo de Horarios"
        index_together = ["estado", "confirmado"]

    def __str__(self):
        return "[{}]".format(self.codigo)

    def save(self, *arg, **kwargs):
        if not self.codigo:
            self.codigo = self.__generar_codigo()
        super().save(*arg, **kwargs)

    def __generar_codigo(self):
        prefijo = "GH"
        codigo_new = self.__generar_codigo_nuevo_numero(prefijo)
        return "{}{}".format(prefijo, str(codigo_new).zfill(3))

    def __generar_codigo_nuevo_numero(self, prefijo):
        anterior_inst = (
            GrupoHorario.objects.values("codigo")
            .filter(codigo__istartswith=prefijo)
            .order_by("-codigo")
            .first()
        )
        codigo_new = 1
        if anterior_inst:
            codigo_ant = (
                anterior_inst.get("codigo", "")[2:]
                if anterior_inst.get("codigo")
                else "0"
            )
            codigo_new = int(codigo_ant) + 1
        return codigo_new


class GrupoHorarioDetalle(AuditableModel, TimeStampedModel):
    grupo_horario = models.ForeignKey(GrupoHorario, on_delete=models.CASCADE)
    # dia de la semana comienza lunes (ISO ISO 8601)
    dia_semana = models.SmallIntegerField(
        "Dia de la semana", choices=DIA_SEMANA_CHOICES
    )
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    orden_view = models.SmallIntegerField("", blank=True, null=True)
    estado = models.BooleanField("Estado", default=False)
    confirmado = models.BooleanField("Confirmado", default=False)

    class Meta:
        verbose_name = "Grupo Horario detalle"
        verbose_name_plural = "Grupo Horarios detalle"
        index_together = ["estado", "grupo_horario"]
        unique_together = [["grupo_horario", "dia_semana", "horario"]]
        ordering = ["grupo_horario", "dia_semana", "orden_view"]

    def __str__(self):
        return "{}-{}-{}".format(
            self.grupo_horario, self.get_dia_semana_display(), self.horario
        )
