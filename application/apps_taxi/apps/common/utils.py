import logging
from datetime import datetime, time, timedelta

from django.utils import timezone

from apps.core_app.constants import (
    ACTIVA_TUROPE_HORARIO_ANTERIOR,
    ACTIVA_TUROPE_HORARIO_PROXIMO,
    DESACTIVAR_TURNO_HORARIO_ANTIGUO,
    TUROPE_ACT_XTOLERANCIA_ANTES,
    TUROPE_ACT_XTOLERANCIA_DESPUES,
)
from apps.core_maestras.models import GrupoHorarioDetalle, Horario
from apps.core_operador.models import (
    CatHorarioOperardor,
    CatHorarioOperardorDetalle,
    Operador,
)
from apps.core_turno.constants import (
    ESTADO_TURNO_ACTIVO,
    ESTADO_TURNO_CONCLUIDO,
    ESTADO_TURNO_PROGRAMADO,
)
from apps.users.models import User

logger = logging.getLogger(__name__)


def obtener_fecha_hora_actual_sistema_str():
    return datetime.today().strftime("%Y-%m-%d %H:%M:%S")


# gestiona turno de operador
class DataLoginTurnoOperador:
    user: User = None
    existe_horarios: bool = False
    horario_anterior: Horario = None
    horario_actual: Horario = None
    horario_siguiente: Horario = None
    operador: Operador = None
    turno_operador = None
    fecha_actual: datetime = None

    def __init__(self, request):
        self.fecha_actual = datetime.today()
        self.user = request.user
        if self.user:
            self.existe_horarios = self.__obtener_horarios()
            self.__obtener_datos_operador()

    def __obtener_datos_operador(self):
        from apps.core_turno.models import TurnoOperador

        # obtener Operador
        operador = Operador.objects.filter(user=self.user).first()
        if not operador:
            return self
        self.operador = operador

        # horario actual
        if not self.existe_horarios:
            return self
        # obtener turno
        fecha_actual = self.fecha_actual
        fech_activ_ant = fecha_actual - timedelta(
            minutes=ACTIVA_TUROPE_HORARIO_ANTERIOR
        )
        fech_activ_prox = fecha_actual + timedelta(
            minutes=ACTIVA_TUROPE_HORARIO_PROXIMO
        )

        turnope_activo = TurnoOperador.objects.filter(
            operador_id=operador.codigo,
            estado_turno=ESTADO_TURNO_ACTIVO,
        ).first()

        # ---------------
        # turno activo está dentro del horario
        if (
            turnope_activo
            and turnope_activo.horario == self.horario_actual
            and turnope_activo.fecha_programacion
        ):
            if turnope_activo.fecha_programacion == fecha_actual.date():
                self.turno_operador = turnope_activo
                return self

        # verificar si turno es antiguo (para desactivar)
        if turnope_activo:
            text_fturno = turnope_activo.fecha_programacion.strftime("%Y-%m-%d")
            text_fturno_hora_ini = turnope_activo.hora_programacion.strftime("%H:%M:%S")
            fturno_ini = datetime.strptime(
                "{} {}".format(text_fturno, text_fturno_hora_ini), "%Y-%m-%d %H:%M:%S"
            )
            fturno_comprobar = fecha_actual - timedelta(
                hours=DESACTIVAR_TURNO_HORARIO_ANTIGUO
            )
            fturno_es_antiguo = True if (fturno_comprobar > fturno_ini) else False
            # turno antiguo (desactivar)
            if fturno_es_antiguo:
                turnope_activo.estado_turno = ESTADO_TURNO_CONCLUIDO
                turnope_activo.observacion = (
                    "Desactiva automaticamente por vencimiento de turno"
                )
                turnope_activo.save(update_fields=["estado_turno", "observacion"])
                turnope_activo = None

        # turno activo no existe
        if not turnope_activo:
            # proceso activar nuevos turnos
            turnope_new = TurnoOperador.objects.filter(
                operador_id=operador.codigo,
                horario=self.horario_actual,
                fecha_programacion=fecha_actual.date(),
            ).first()
            if turnope_new:
                if turnope_new.estado_turno == ESTADO_TURNO_ACTIVO:
                    return self
                turnope_new.estado_turno = ESTADO_TURNO_ACTIVO
                turnope_new.save(update_fields=["estado_turno"])
                self.turno_operador = turnope_new
                return self
            # verificar si tiene turno para programar
            cat_horario = CatHorarioOperardor.objects.filter(
                cat_horario=operador.grupo_horario, activo=True
            ).first()
            grupo_hor_detail = GrupoHorarioDetalle.objects.filter(
                grupo_horario=operador.grupo_horario,
                confirmado=True,
                dia_semana=int(self.fecha_actual.strftime("%u")),
                horario=self.horario_actual,
            ).first()
            cat_hora_det = CatHorarioOperardorDetalle.objects.filter(
                cat_horario=cat_horario,
                operador=operador,
                grupo_horario_detalle=grupo_hor_detail,
            ).first()
            if cat_hora_det:
                try:
                    default_data = {
                        "created_by": self.user.username,
                        "modified_by": self.user.username,
                        "hora_programacion": self.horario_actual.inicio_horario,
                        "hora_fin_programacion": self.horario_actual.fin_horario,
                        "hora_inicio": self.fecha_actual.time(),
                        "estado_turno": ESTADO_TURNO_ACTIVO,
                        "observacion": "creado automáticamente",
                    }
                    turnope_new, _status = TurnoOperador.objects.get_or_create(
                        operador=operador,
                        horario=self.horario_actual,
                        fecha_programacion=self.fecha_actual.date(),
                        defaults=default_data,
                    )
                    self.turno_operador = turnope_new
                    return self
                except Exception as ex:
                    mensaje = "Error al crear horario operador auntomaticamente"
                    logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})

            # horario proximo
            turnope_new = TurnoOperador.objects.filter(
                operador_id=operador.codigo,
                horario=self.horario_siguiente,
                fecha_programacion=fech_activ_prox.date(),
            ).first()
            if turnope_new:
                if turnope_new.estado_turno == ESTADO_TURNO_ACTIVO:
                    return self
                turnope_new.estado_turno = ESTADO_TURNO_ACTIVO
                turnope_new.save(update_fields=["estado_turno"])
                self.turno_operador = turnope_new
                return self
            # verificar si tiene turno próximo para programar
            grupo_hor_detail = GrupoHorarioDetalle.objects.filter(
                grupo_horario=operador.grupo_horario,
                confirmado=True,
                dia_semana=int(self.fecha_actual.strftime("%u")),
                horario=self.horario_siguiente,
            ).first()
            cat_hora_det = CatHorarioOperardorDetalle.objects.filter(
                cat_horario=cat_horario,
                operador=operador,
                grupo_horario_detalle=grupo_hor_detail,
            ).first()
            if cat_hora_det:
                try:
                    default_data = {
                        "created_by": self.user.username,
                        "modified_by": self.user.username,
                        "hora_programacion": self.horario_siguiente.inicio_horario,
                        "hora_fin_programacion": self.horario_siguiente.fin_horario,
                        "hora_inicio": self.fecha_actual.time(),
                        "estado_turno": ESTADO_TURNO_ACTIVO,
                        "observacion": "creado automáticamente",
                    }
                    turnope_new, _status = TurnoOperador.objects.get_or_create(
                        operador=operador,
                        horario=self.horario_siguiente,
                        fecha_programacion=self.fecha_actual.date(),
                        defaults=default_data,
                    )
                    self.turno_operador = turnope_new
                    return self
                except Exception as ex:
                    mensaje = "Error al crear horario operador automáticamente"
                    logger.warning(
                        mensaje, exc_info=True, extra={"error_data": str(ex)}
                    )

            # horario anterior
            turnope_new = TurnoOperador.objects.filter(
                operador_id=operador.codigo,
                horario=self.horario_anterior,
                fecha_programacion=fech_activ_ant.date(),
            ).first()
            if turnope_new:
                if turnope_new.estado_turno == ESTADO_TURNO_ACTIVO:
                    return self
                turnope_new.estado_turno = ESTADO_TURNO_ACTIVO
                turnope_new.save(update_fields=["estado_turno"])
                self.turno_operador = turnope_new
                return self
            return self

        # verificar si ya existe nuevo turno programado
        turnope_new = TurnoOperador.objects.filter(
            operador_id=operador.codigo,
            estado_turno=ESTADO_TURNO_PROGRAMADO,
            horario=self.horario_actual,
            fecha_programacion=fecha_actual.date(),
        ).first()
        if turnope_new:
            turnope_activo.estado_turno = ESTADO_TURNO_CONCLUIDO
            turnope_activo.observacion = (
                "Desactiva automaticamente. Se activará nuevo turno"
            )
            turnope_activo.save(update_fields=["estado_turno", "observacion"])
            # ---
            turnope_new.estado_turno = ESTADO_TURNO_ACTIVO
            turnope_new.save(update_fields=["estado_turno"])
            self.turno_operador = turnope_new
            return self
        # Turno activo por tolerancia
        fech_cons_ini = fecha_actual - timedelta(minutes=TUROPE_ACT_XTOLERANCIA_DESPUES)
        fech_cons_fin = fecha_actual + timedelta(minutes=TUROPE_ACT_XTOLERANCIA_ANTES)
        esta_en_el_rango_tolerancia = self.__esta_dentro_rango_fecha_hora(
            fech_cons_ini,
            fech_cons_fin,
            turnope_activo.fecha_programacion,
            turnope_activo.hora_programacion,
            turnope_activo.hora_fin_programacion,
        )
        if esta_en_el_rango_tolerancia:
            self.turno_operador = turnope_activo
        return self

    def __esta_dentro_rango_fecha_hora(
        self,
        fconsul_ini: datetime,
        fconsul_fin: datetime,
        fturno_prog: datetime,
        hturno_prog_ini,
        hturno_prog_fin,
    ) -> bool:
        valido = False
        text_fturno = fturno_prog.strftime("%Y-%m-%d")
        text_fturno_hora_ini = hturno_prog_ini.strftime("%H:%M:%S")
        aux_time_0 = time()
        if hturno_prog_fin < aux_time_0:
            hora_final = (
                (datetime.fromisoformat("2001-01-02")) - timedelta(microseconds=1)
            ).time()
        else:
            hora_final = hturno_prog_fin
        text_fturno_hora_fin = hora_final.strftime("%H:%M:%S")
        fturno_ini = datetime.strptime(
            "{} {}".format(text_fturno, text_fturno_hora_ini), "%Y-%m-%d %H:%M:%S"
        )
        fturno_fin = datetime.strptime(
            "{} {}".format(text_fturno, text_fturno_hora_fin), "%Y-%m-%d %H:%M:%S"
        )
        if fconsul_ini <= fturno_ini and fconsul_fin <= fturno_fin:
            valido = True
        return valido

    def __obtener_horarios(self) -> bool:
        horarios = Horario.objects.filter(horario_base=True).order_by("orden_view")
        if horarios.count() < 2:  # TODO falta implementar para horarios < 2
            return False
        # ordenar data
        horarios_dict = {}
        primero = 0
        ultimo = 0
        i = 2
        hora_actual = self.fecha_actual.time()
        for horario in horarios:
            horarios_dict.update({i: horario})
            if primero == 0:
                primero = i
                ultimo = i
            if ultimo < i:
                ultimo = i
            i += 1
        horarios_dict.update({1: horarios_dict.get(ultimo)})
        horarios_dict.update({i: horarios_dict.get(primero)})
        horarios_dict = dict(sorted(horarios_dict.items()))

        # encontrar horario actual
        actual = 0
        aux_time_0 = time()
        for key, value in horarios_dict.items():
            hora_final = value.fin_horario
            if value.fin_horario <= aux_time_0:
                hora_final = (
                    (datetime.fromisoformat("2001-01-02")) - timedelta(microseconds=1)
                ).time()
            if (
                actual == 0
                and key > 1
                and value.inicio_horario <= hora_actual < hora_final
            ):
                actual = key
                break
        # Asignar data
        self.horario_anterior = horarios_dict.get((actual - 1))
        self.horario_actual = horarios_dict.get(actual)
        self.horario_siguiente = horarios_dict.get((actual + 1))
        return True


def obtener_fecha_hora_actual():
    time = datetime.now()
    timez = timezone.now()
    current_tz = timezone.get_current_timezone()
    data = {
        "time": time.time(),
        "date": time.date(),
        "timez": timez.time(),
        "datez": timez.date(),
        "current_tz": str(current_tz),
    }
    return data
