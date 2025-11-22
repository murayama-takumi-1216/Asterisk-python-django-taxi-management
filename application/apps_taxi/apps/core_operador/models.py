from django.conf import settings
from django.db import models

from apps.common.models import AuditableModel, TimeStampedModel
from apps.core_maestras.models import GrupoHorario, GrupoHorarioDetalle


class Operador(AuditableModel, TimeStampedModel):
    codigo = models.SlugField("Código", max_length=9, primary_key=True)
    nombre = models.CharField("Nombre", max_length=60)
    apellido_paterno = models.CharField(
        "Apellido Paterno", max_length=50, blank=True, null=True
    )
    apellido_materno = models.CharField(
        "Apellido Materno", max_length=50, blank=True, null=True
    )
    alias = models.CharField("Alias", max_length=50, blank=True)
    extension = models.CharField("Extensión", max_length=20, blank=True, null=True)
    estado = models.BooleanField("Estado", default=False)
    rogramacion_automatica = models.BooleanField(
        "Programación automática", blank=True, default=True
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    sesion_turno_activa = models.IntegerField(
        "Sesión id turno activo", null=True, blank=True
    )

    grupo_horario = models.ForeignKey(
        GrupoHorario, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"

    def __str__(self):
        return "[{}] {} {} ({})".format(
            self.codigo, self.nombre, self.apellido_paterno, self.alias
        )

    def save(self, *arg, **kwargs):
        if not self.codigo or self.codigo == "vacio":
            self.codigo = self.__generar_codigo()
        super().save(*arg, **kwargs)

    def __generar_codigo(self):
        prefijo = "OPE"
        codigo_new = self.__generar_codigo_nuevo_numero(prefijo)
        return "{}{}".format(prefijo, str(codigo_new).zfill(6))

    def __generar_codigo_nuevo_numero(self, prefijo):
        anterior_inst = (
            Operador.objects.values("codigo")
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

    @staticmethod
    def validar_nombre_unico(codigo, nombre, apellido_paterno):
        """Validate unique name combination (nombre + apellido_paterno)"""
        if nombre and apellido_paterno:
            query = Operador.objects.filter(
                nombre__iexact=nombre.strip(),
                apellido_paterno__iexact=apellido_paterno.strip(),
            )
            if codigo:
                query = query.exclude(codigo=codigo)
            return not query.exists()
        return True


class CatHorarioOperardor(AuditableModel, TimeStampedModel):
    codigo = models.SlugField("Código", max_length=9, primary_key=True)
    cat_horario = models.ForeignKey(
        GrupoHorario, on_delete=models.CASCADE, null=True, blank=True
    )
    fecha_inicio = models.DateField("Fecha inicio", null=True, blank=True)
    fecha_fin = models.DateField("Fecha fin", null=True, blank=True)
    activo = models.BooleanField("Activo", default=False)

    class Meta:
        verbose_name = "Catalogo de horario del operador"
        verbose_name_plural = "Catalogo de horarios del operador"

    def __str__(self):
        return self.codigo

    def save(self, *arg, **kwargs):
        if not self.codigo:
            self.codigo = self.__generar_codigo()
        super().save(*arg, **kwargs)

    def __generar_codigo(self):
        prefijo = "{}_".format(self.cat_horario.codigo)
        codigo_new = self.__generar_codigo_nuevo_numero(prefijo)
        return "{}{}".format(prefijo, str(codigo_new).zfill(3))

    def __generar_codigo_nuevo_numero(self, prefijo):
        longitud_preijo = len(prefijo)
        anterior_inst = (
            Operador.objects.values("codigo")
            .filter(codigo__istartswith=prefijo)
            .order_by("-codigo")
            .first()
        )
        codigo_new = 1
        if anterior_inst:
            codigo_ant = (
                anterior_inst.get("codigo", "")[longitud_preijo:]
                if anterior_inst.get("codigo")
                else "0"
            )
            codigo_new = int(codigo_ant) + 1
        return codigo_new


class CatHorarioOperardorDetalle(AuditableModel, TimeStampedModel):
    fecha_inicio = models.DateTimeField(
        "Fecha hora inicio", blank=True, null=True
    )  # TODO verificar
    fecha_fin = models.DateTimeField(
        "Fecha hora fin", blank=True, null=True
    )  # TODO verificar
    activo = models.BooleanField("Activo", default=False)
    confirmado = models.BooleanField("Confirmado", default=False)

    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    cat_horario = models.ForeignKey(CatHorarioOperardor, on_delete=models.CASCADE)
    grupo_horario_detalle = models.ForeignKey(
        GrupoHorarioDetalle, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Detalle de catalogo de horario"
        verbose_name_plural = "Detalles de catalogo de horario"
        unique_together = [["cat_horario", "grupo_horario_detalle", "operador"]]
