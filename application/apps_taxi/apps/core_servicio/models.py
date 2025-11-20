from datetime import datetime

from django.db import models

from apps.common.models import AuditableModel, TimeStampedModel
from apps.core_cliente.models import Cliente
from apps.core_maestras.models import Horario
from apps.core_operador.models import Operador
from apps.core_servicio.constants import (
    FINALIZA_SERVICIO_CANCELCLIENTE,
    FINALIZA_SERVICIO_CANCELCONDUCTOR,
    FINALIZA_SERVICIO_REALIZADO,
    QUIEN_LLAMA_CLIENTE,
)
from apps.core_turno.models import TurnoConductor, TurnoOperador

from .constants import (
    ESTADO_LLAMADA_CHOICES,
    FINALIZA_SERVICIO_CHOICES,
    FINALIZA_SERVICIO_PENDIENTE,
)


class Llamada(AuditableModel, TimeStampedModel):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )
    operador_contesta = models.ForeignKey(
        Operador, on_delete=models.CASCADE, null=True, blank=True
    )
    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, blank=True, null=True
    )
    anio = models.IntegerField("Año")
    # Fecha hora de llamada
    fecha_llamada = models.DateField("Fecha llamada")  # TODO Eliminar
    hora_llamada = models.TimeField("Hora llamada")  # TODO Eliminar
    fecha_hora_llamada = models.DateTimeField(
        "Fecha hora llamada", blank=True, null=True
    )

    numero = models.CharField("Numero", max_length=20, blank=False, null=False)
    estado_llamada = models.CharField(
        "Estado llamada",
        max_length=2,
        blank=True,
        null=True,
        choices=ESTADO_LLAMADA_CHOICES,
        help_text="Estado de llamada",
    )
    tipo_quien_llama = models.CharField(
        "Quien llama",
        max_length=2,
        blank=True,
        null=True,
        default=QUIEN_LLAMA_CLIENTE,
        choices=ESTADO_LLAMADA_CHOICES,
    )
    cerrar_llamada = models.BooleanField("Cerrar llamada", default=False)
    # otra llamada son llamadas que no entra al servicio
    otra_llamada = models.BooleanField(
        "Otra llamada", default=False, blank=True, null=True
    )
    eliminado = models.BooleanField("Eliminado", default=False)

    # --- canales de llamada entrante
    channel = models.CharField("Channel", max_length=30, blank=True, null=True)
    channel_state_desc = models.CharField(
        "Channel State Desc", max_length=20, blank=True, null=True
    )
    callerid_num = models.CharField(
        "Caller ID Num", max_length=20, blank=True, null=True
    )
    callerid_name = models.CharField(
        "Caller ID Name", max_length=40, blank=True, null=True
    )
    uniqueid = models.CharField("Uniqueid", max_length=20, blank=True, null=True)
    context = models.CharField("Context", max_length=40, blank=True, null=True)

    # --- canales de llamada para extensión
    connected_channel = models.CharField(
        "Connected Channel", max_length=30, blank=True, null=True
    )
    connected_channel_state_desc = models.CharField(
        "Connected Channel State Desc", max_length=20, blank=True, null=True
    )
    connected_callerid_num = models.CharField(
        "Connected Num", max_length=20, blank=True, null=True
    )

    # --- llamadas
    bridgeid = models.CharField("Bridge Id", max_length=40, blank=True, null=True)
    linkedid = models.CharField("Linkedid", max_length=20, blank=True, null=True)
    duration = models.CharField("Duración", max_length=10, blank=True, null=True)

    marca_tiempo_ami = models.IntegerField(
        "Marca de tiempo", blank=True, null=True
    )  # TODO esto puede tener fallas al cambiar de año (1 a 2 segundos que pueden duplicarse números)

    class Meta:
        verbose_name = "Llamada"
        verbose_name_plural = "Llamadas"
        index_together = [
            "anio",
            "numero",
            "estado_llamada",
            "fecha_hora_llamada",
            "linkedid",
            "marca_tiempo_ami",
            "tipo_quien_llama",
        ]
        ordering = ["-id"]

    def __str__(self):
        if self.cliente:
            return self.cliente.nombre
        return self.numero

    @classmethod
    def generar_marca_tiempo_ami(cls):
        date = datetime.today()
        time_value = (
            int(date.strftime("%j")) * 86400
            + date.hour * 3600
            + date.minute * 60
            + date.second
        )
        return time_value, date.year, date

    @staticmethod
    def contar_llamadas_contestadas(
        turno_operador: TurnoOperador,
    ):  # TODO Falta implementar
        cantidad = Llamada.objects.filter(
            operador_contesta=turno_operador.operador,
            fecha_llamada=turno_operador.fecha_programacion,
            horario=turno_operador.horario,
            eliminado=False,
        )
        return cantidad.count()

    @staticmethod
    def contar_llamadas_otras(turno_operador: TurnoOperador):  # TODO Falta implementar
        cantidad = Llamada.objects.filter(
            operador_contesta=turno_operador.operador,
            otra_llamada=True,
            fecha_llamada=turno_operador.fecha_programacion,
            horario=turno_operador.horario,
            eliminado=False,
        )
        return cantidad.count()


class Servicio(AuditableModel, TimeStampedModel):
    llamada = models.ForeignKey(
        Llamada, on_delete=models.CASCADE, null=True, blank=True
    )
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )
    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, null=True, blank=True
    )
    operador_registra = models.ForeignKey(
        Operador,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="operador_registra",
    )
    operador_asigna = models.ForeignKey(
        Operador,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="operador_asigna",
    )
    turno_conductor = models.ForeignKey(
        TurnoConductor, on_delete=models.CASCADE, null=True, blank=True
    )
    referencia_origen = models.CharField(
        "Ref. origen", max_length=150, blank=True, null=True
    )
    referencia_destino = models.CharField(
        "Ref. destino", max_length=150, blank=True, null=True
    )
    ubicacion_origen = models.CharField(
        "Ubi. origen", max_length=30, blank=True, null=True
    )
    ubicacion_destino = models.CharField(
        "Ubi. destino", max_length=30, blank=True, null=True
    )
    # Fecha hora programada de inicio
    fecha_programacion = models.DateField(
        "Fecha programación", blank=True, null=True
    )  # TODO Eliminar
    hora_programacion = models.TimeField(
        "Hora programación", blank=True, null=True
    )  # TODO Eliminar
    programado_fecha_hora_inicio = models.DateTimeField(
        "Programado fecha hora inicio", blank=True, null=True
    )

    pasajeros = models.IntegerField("Pasajeros", default=0, blank=True, null=True)
    monto_servicio = models.DecimalField(
        "Monto servicio",
        max_digits=5,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
    )
    observacion_registro = models.CharField(
        "Obs. registro", max_length=250, blank=True, null=True
    )
    observacion_asignacion = models.CharField(
        "Obs. asignación", max_length=250, blank=True, null=True
    )
    observacion_servicio = models.CharField(
        "Obs. servicio", max_length=250, blank=True, null=True
    )
    # Fecha hora inicio
    hora_inicio = models.TimeField(
        "Hora inicio", blank=True, null=True
    )  # TODO Eliminar
    fecha_hora_inicio = models.DateTimeField("Fecha hora inicio", blank=True, null=True)
    # Fecha hora fin
    hora_fin = models.TimeField("Hora fin", blank=True, null=True)  # TODO Eliminar
    fecha_hora_fin = models.DateTimeField("Fecha hora fin", blank=True, null=True)

    horas_efectivas = models.TimeField("Hora efectiva", blank=True, null=True)
    estado = models.BooleanField("Estado", blank=True, default=False)
    estado_finaliza_servicio = models.CharField(
        "Estado finaliza servicio",
        max_length=2,
        choices=FINALIZA_SERVICIO_CHOICES,
        default=FINALIZA_SERVICIO_PENDIENTE,
        blank=True,
        null=True,
    )
    eliminado = models.BooleanField("Eliminado", blank=True, default=False)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        index_together = [
            "estado",
            "horario",
            "eliminado",
            "estado_finaliza_servicio",
            "programado_fecha_hora_inicio",
            "fecha_hora_inicio",
            "fecha_hora_fin",
            "operador_registra",
        ]

    def __str__(self):
        return self.nombre

    @property
    def nombre(self):
        return "[{}-{}]-{}".format(
            self.fecha_programacion, self.hora_programacion, self.cliente_id
        )

    @staticmethod
    def contar_registros_operador(
        turno_operador: TurnoOperador,
    ):  # TODO Falta implementar
        cantidad = Servicio.objects.filter(
            operador_registra=turno_operador.operador,
            fecha_programacion=turno_operador.fecha_programacion,
            horario=turno_operador.horario,
            eliminado=False,
        )
        return cantidad.count()

    @staticmethod
    def contar_asignados_operador(
        turno_operador: TurnoOperador,
    ):  # TODO Falta implementar
        cantidad = Servicio.objects.filter(
            operador_asigna=turno_operador.operador,
            fecha_programacion=turno_operador.fecha_programacion,
            horario=turno_operador.horario,
            turno_conductor__isnull=False,
            eliminado=False,
        )
        return cantidad.count()

    @staticmethod
    def contar_pendientes_conductor(
        turno_conductor: TurnoConductor,
    ):  # TODO Falta implementar
        cantidad = Servicio.objects.filter(
            turno_conductor=turno_conductor,
            estado_finaliza_servicio=FINALIZA_SERVICIO_PENDIENTE,
            eliminado=False,
        )
        return cantidad.count()

    @staticmethod
    def contar_atendidos_conductor(
        turno_conductor: TurnoConductor,
    ):  # TODO Falta implementar
        cantidad = Servicio.objects.filter(
            turno_conductor=turno_conductor,
            estado_finaliza_servicio=FINALIZA_SERVICIO_REALIZADO,
            eliminado=False,
        )
        return cantidad.count()

    @staticmethod
    def contar_cancelados(turno_conductor: TurnoConductor):  # TODO Falta implementar
        cantidad = Servicio.objects.filter(
            turno_conductor=turno_conductor,
            estado_finaliza_servicio=FINALIZA_SERVICIO_CANCELCLIENTE,
            eliminado=False,
        ).count()
        return cantidad

    @staticmethod
    def contar_cancel_conductor(
        turno_conductor: TurnoConductor,
    ):  # TODO Falta implementar
        cantidad = Servicio.objects.filter(
            turno_conductor=turno_conductor,
            estado_finaliza_servicio=FINALIZA_SERVICIO_CANCELCONDUCTOR,
            eliminado=False,
        )
        return cantidad.count()


class ServicioModificado(AuditableModel, TimeStampedModel):
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="servicio_modificado",
    )
    operador_asigna = models.ForeignKey(
        Operador,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="operador_asigna_modificado",
    )
    turno_conductor = models.ForeignKey(
        TurnoConductor, on_delete=models.CASCADE, null=True, blank=True
    )
    referencia_origen = models.CharField(
        "Ref. origen", max_length=150, blank=True, null=True
    )
    referencia_destino = models.CharField(
        "Ref. destino", max_length=150, blank=True, null=True
    )
    ubicacion_origen = models.CharField(
        "Ubi. origen", max_length=30, blank=True, null=True
    )
    ubicacion_destino = models.CharField(
        "Ubi. destino", max_length=30, blank=True, null=True
    )
    # Fecha hora programada de inicio
    programado_fecha_hora_inicio = models.DateTimeField(
        "Programado fecha hora inicio", blank=True, null=True
    )

    pasajeros = models.IntegerField("Pasajeros", default=0, blank=True, null=True)
    observacion_asignacion = models.CharField(
        "Obs. asignación", max_length=250, blank=True, null=True
    )
    observacion_servicio = models.CharField(
        "Obs. servicio", max_length=250, blank=True, null=True
    )
    # Fecha hora inicio
    fecha_hora_inicio = models.DateTimeField("Fecha hora inicio", blank=True, null=True)
    # Fecha hora fin
    fecha_hora_fin = models.DateTimeField("Fecha hora fin", blank=True, null=True)

    class Meta:
        verbose_name = "Servicio Modificado"
        verbose_name_plural = "Servicios Modificados"
        index_together = [
            "programado_fecha_hora_inicio",
            "fecha_hora_inicio",
            "fecha_hora_fin",
        ]

    def __str__(self):
        return self.servicio.nombre if self.servicio else self.turno_conductor
