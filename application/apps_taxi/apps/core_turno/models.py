import datetime
import logging
from datetime import timedelta

from django.db import models
from django.db.models import Exists, OuterRef

from apps.common.models import AuditableModel, TimeStampedModel
from apps.common.utils import DataLoginTurnoOperador
from apps.core_conductor.models import Conductor
from apps.core_maestras.models import Horario
from apps.core_operador.models import Operador
from apps.core_turno.constants import (
    ESTADO_TURNO_ACTIVO,
    ESTADO_TURNO_CHOICES,
    ESTADO_TURNO_CONCLUIDO,
    ESTADO_TURNO_PENDIENTE,
)
from apps.core_vehiculo.constants import ESTADO_ALQUILER_ACTIVO
from apps.core_vehiculo.models import AlquilerVehiculo, Vehiculo

logger = logging.getLogger(__name__)


class TurnoConductor(AuditableModel, TimeStampedModel):
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    horario_inicio = models.ForeignKey(
        Horario, on_delete=models.CASCADE, blank=True, null=True
    )
    # programacion inicio
    fecha_programacion = models.DateField("Fecha programación")  # TODO Eliminar
    hora_programacion = models.TimeField("Hora programación")  # TODO Eliminar
    programado_fecha_hora_inicio = models.DateTimeField(
        "Programado fecha hora inicio", blank=True, null=True
    )
    # programacion Fin
    fecha_fin_programacion = models.DateField("Fecha fin programación")  # TODO Eliminar
    hora_fin_programacion = models.TimeField("Hora fin programación")  # TODO Eliminar
    programado_fecha_hora_fin = models.DateTimeField(
        "Programado fecha hora fin", blank=True, null=True
    )

    # Inicio
    hora_inicio = models.TimeField(
        "Hora inicio", blank=True, null=True
    )  # TODO Eliminar
    fecha_hora_inicio = models.DateTimeField("Fecha hora inicio", blank=True, null=True)
    # Fin
    hora_fin = models.TimeField("Hora fin", blank=True, null=True)  # TODO Eliminar
    fecha_hora_fin = models.DateTimeField("Fecha hora fin", blank=True, null=True)

    horas_efectivas = models.TimeField("Hora efectiva", blank=True, null=True)
    monto_generado = models.DecimalField(
        "Monto generado", max_digits=5, decimal_places=2, default=0
    )
    servicios_asignados = models.IntegerField(
        "Servicios asignados", default=0, blank=True, null=True
    )
    servicios_atendidos = models.IntegerField(
        "Servicios atendidos", default=0, blank=True, null=True
    )
    # Servicios cancelados, son cancelados por el cliente (es decir al recoger no encuentra al cliente)
    servicios_cancelados = models.IntegerField(
        "Servicios cancelados", default=0, blank=True, null=True
    )
    servicios_cancel_conductor = models.IntegerField(
        "Cancelado por conductor", default=0, blank=True, null=True
    )
    estado_turno = models.CharField(
        "Estado Turno",
        max_length=2,
        choices=ESTADO_TURNO_CHOICES,
        default=ESTADO_TURNO_PENDIENTE,
    )
    observacion = models.CharField(
        "Obs. servicio", max_length=250, blank=True, null=True
    )

    class Meta:
        verbose_name = "Turno conductor"
        verbose_name_plural = "Turnos conductores"
        index_together = [
            "estado_turno",
            "programado_fecha_hora_inicio",
            "programado_fecha_hora_fin",
            "fecha_hora_inicio",
            "fecha_hora_fin",
        ]

    def __str__(self):
        return self.nombre

    @property
    def nombre(self):
        return "[{}-{}]-{}".format(
            self.fecha_programacion, self.hora_programacion, self.vehiculo
        )

    @staticmethod
    def crear_automatico_turnos(data_login_turope: DataLoginTurnoOperador) -> bool:
        # Activar Turnos de conductor
        fecha_actual = data_login_turope.fecha_actual
        exist_subquery = TurnoConductor.objects.filter(
            vehiculo_id=OuterRef("vehiculo_id"),
            conductor_id=OuterRef("conductor_id"),
            fecha_programacion__gte=OuterRef("fecha_prog_inicio"),
            fecha_programacion=fecha_actual.date(),
            horario_inicio=data_login_turope.horario_actual,
        ).exclude(estado_turno=ESTADO_TURNO_CONCLUIDO)

        alquileres_sin_turno = AlquilerVehiculo.objects.filter(
            programacion_automatica=True,
            fecha_prog_inicio__lte=fecha_actual.date(),
            estado=ESTADO_ALQUILER_ACTIVO,
            entrega_radio=True,
        ).filter(~Exists(exist_subquery))
        if alquileres_sin_turno.exists():
            for alquiler in alquileres_sin_turno:
                try:
                    default_data = {
                        "created_by": data_login_turope.user.username,
                        "modified_by": data_login_turope.user.username,
                        "hora_programacion": data_login_turope.horario_actual.inicio_horario,
                        "fecha_fin_programacion": data_login_turope.fecha_actual.date(),
                        "hora_fin_programacion": data_login_turope.horario_actual.fin_horario,
                        "hora_inicio": data_login_turope.fecha_actual.time(),
                        "estado_turno": ESTADO_TURNO_ACTIVO,
                        "observacion": "creado automáticamente",
                    }
                    turno_new, _status = TurnoConductor.objects.update_or_create(
                        conductor=alquiler.conductor,
                        vehiculo=alquiler.vehiculo,
                        horario_inicio=data_login_turope.horario_actual,
                        fecha_programacion=data_login_turope.fecha_actual.date(),
                        defaults=default_data,
                    )
                except Exception as ex:
                    mensaje = "Error al crear horario conductor automáticamente"
                    logger.warning(
                        mensaje, exc_info=True, extra={"error_data": str(ex)}
                    )

    @staticmethod
    def cerrar_automatico_turnos(data_login_turope: DataLoginTurnoOperador) -> bool:
        # Inactivar Turnos de conductor
        fecha_actual = data_login_turope.fecha_actual
        fecha_horario_anterior = fecha_actual - timedelta(hours=8, minutes=1)
        turnos_antiguos_activos = TurnoConductor.objects.exclude(
            horario_inicio=data_login_turope.horario_actual,
            fecha_programacion__gte=fecha_horario_anterior.date(),
            fecha_programacion__lte=fecha_actual.date(),
        ).filter(
            estado_turno=ESTADO_TURNO_ACTIVO,
            fecha_programacion__lte=fecha_horario_anterior.date(),
        )
        if turnos_antiguos_activos.exists():
            turnos_antiguos_activos.update(
                hora_fin=fecha_actual.time(),
                estado_turno=ESTADO_TURNO_CONCLUIDO,
                observacion="cerrado automática",
            )

    @staticmethod
    def cerrar_turnos_alquiler_concluido(vehiculo: Vehiculo) -> bool:
        # Inactivar Turnos de conductor
        fecha_actual = datetime.datetime.today()
        fecha_horario_anterior = fecha_actual - timedelta(hours=9, minutes=1)
        turnos_antiguos_activos = TurnoConductor.objects.filter(
            estado_turno=ESTADO_TURNO_ACTIVO,
            fecha_programacion__gte=fecha_horario_anterior.date(),
            vehiculo=vehiculo,
        )
        if turnos_antiguos_activos.exists():
            turnos_antiguos_activos.update(
                hora_fin=fecha_actual.time(),
                estado_turno=ESTADO_TURNO_CONCLUIDO,
                observacion="cerrado automática - alquiler concluido",
            )


class TurnoOperador(AuditableModel, TimeStampedModel):
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, blank=True, null=True
    )
    extension_numero = models.CharField(
        "Extensión", max_length=20, blank=True, null=True
    )
    # programacion inicio
    fecha_programacion = models.DateField("Fecha programación")  # TODO Eliminar
    hora_programacion = models.TimeField("Hora programación")  # TODO Eliminar
    programado_fecha_hora_inicio = models.DateTimeField(
        "Programado fecha hora inicio", blank=True, null=True
    )

    # programacion Fin
    hora_fin_programacion = models.TimeField("Hora fin programación")  # TODO Eliminar
    programado_fecha_hora_fin = models.DateTimeField(
        "Programado fecha hora fin", blank=True, null=True
    )

    # Inicio
    hora_inicio = models.TimeField(
        "Hora inicio", blank=True, null=True
    )  # TODO Eliminar
    fecha_hora_inicio = models.DateTimeField("Fecha hora inicio", blank=True, null=True)

    # Fin
    hora_fin = models.TimeField("Hora fin", blank=True, null=True)  # TODO Eliminar
    fecha_hora_fin = models.DateTimeField("Fecha hora fin", blank=True, null=True)

    horas_efectivas = models.TimeField("Hora efectiva", blank=True, null=True)
    llamadas_atendidos = models.IntegerField("llamdas atendidos", blank=True, default=0)
    # Contabiliza llamadas otras
    llamadas_otras = models.IntegerField("llamdas Otras", blank=True, default=0)
    servicios_registradas = models.IntegerField(
        "Servicios registradas", blank=True, default=0
    )
    servicios_asignadas = models.IntegerField(
        "Servicios asignadas", blank=True, default=0
    )
    estado_turno = models.CharField(
        "Estado Turno",
        max_length=2,
        choices=ESTADO_TURNO_CHOICES,
        default=ESTADO_TURNO_PENDIENTE,
        blank=True,
    )
    observacion = models.CharField(
        "Obs. servicio", max_length=250, blank=True, null=True
    )

    class Meta:
        verbose_name = "Turno operador"
        verbose_name_plural = "Turnos operadores"
        index_together = [
            "estado_turno",
            "programado_fecha_hora_inicio",
            "programado_fecha_hora_fin",
            "fecha_hora_inicio",
            "fecha_hora_fin",
        ]

    def __str__(self):
        return self.nombre

    @property
    def nombre(self):
        return "[{}-{}]-{}".format(
            self.fecha_programacion, self.hora_programacion, self.operador
        )


class ServiciosDiaView(models.Model):
    fecha = models.DateField(primary_key=True)  # Asegúrate de que 'id' está en la vista
    llamadas_atendidas = models.IntegerField(null=True, blank=True)
    registrados = models.IntegerField(null=True, blank=True)
    asignados = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "core_turno_serviciosrview"
