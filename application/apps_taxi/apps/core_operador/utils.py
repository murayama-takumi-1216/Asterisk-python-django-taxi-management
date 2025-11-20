import logging
from datetime import datetime, timedelta

from apps.core_maestras.constants import DIA_SEMANA_CHOICES
from apps.core_maestras.models import Horario
from apps.core_operador.models import CatHorarioOperardor, CatHorarioOperardorDetalle
from apps.core_turno.constants import ESTADO_TURNO_PROGRAMADO
from apps.core_turno.models import TurnoOperador

logger = logging.getLogger(__name__)


def obtener_horario_view(
    cat_horario_activo: CatHorarioOperardor,
    horario_actual: Horario,
    dia_semana_actual: int,
):
    data = {}
    cat_hora_detalles = CatHorarioOperardorDetalle.objects.filter(
        cat_horario=cat_horario_activo
    ).order_by("grupo_horario_detalle__orden_view")
    # --- construir horario ------------->
    horario_base = Horario.objects.filter(horario_base=True).order_by("orden_view")
    dias_semana_dic = dict(DIA_SEMANA_CHOICES)
    data_horario_dic = {}
    for item_horario in horario_base:
        aux_turno = {"horario": item_horario, "data": {}}
        for dia_nro, dia_nombre in dias_semana_dic.items():
            aux_dia = {
                "nro": dia_nro,
                "nombre": dia_nombre,
                # "horario_turno": None,
                "horario_turno_data": [],
            }
            aux_turno.get("data").update({dia_nro: aux_dia})
        data_horario_dic.update({item_horario.cod_horario: aux_turno})
    # --- construir horario <-------------

    # --- obtener datos de turno ------------->
    for info_turno in cat_hora_detalles:
        aux_turno_es_activo = (
            horario_actual.cod_horario == info_turno.grupo_horario_detalle.horario_id
        ) and (dia_semana_actual == info_turno.grupo_horario_detalle.dia_semana)
        # Fixed: Access turno_activo from the correct nested level (day number)
        aux_data = (
            data_horario_dic.get(info_turno.grupo_horario_detalle.horario_id, {})
            .get("data", {})
            .get(info_turno.grupo_horario_detalle.dia_semana, {})
            .get("turno_activo")
        )
        if not aux_data and aux_turno_es_activo:
            data_horario_dic.get(info_turno.grupo_horario_detalle.horario_id, {}).get(
                "data", {}
            ).get(info_turno.grupo_horario_detalle.dia_semana, {}).update(
                {"turno_activo": aux_turno_es_activo}
            )
        # else:
        data_horario_dic.get(info_turno.grupo_horario_detalle.horario_id, {}).get(
            "data", {}
        ).get(info_turno.grupo_horario_detalle.dia_semana, {}).get(
            "horario_turno_data", []
        ).append(
            info_turno
        )

    # --- obtener datos de turno <-------------

    # --- construir horario view ------------->
    data_horario = [
        {
            "horario": item_horas.get("horario"),
            "data": [item_dia for item_dia in item_horas.get("data", {}).values()],
        }
        for item_horas in data_horario_dic.values()
    ]
    # --- construir horario view <-------------

    data.update(
        {
            "dias_semana": [
                {"codigo": num, "nombre": dia} for num, dia in dias_semana_dic.items()
            ],
            "data_horario": data_horario,
            "cat_horario": cat_horario_activo,
        }
    )
    return data


def obtener_horario_view_antigua(
    cat_horario_activo: CatHorarioOperardor,
    horario_actual: Horario,
    dia_semana_actual: int,
):
    data = {}
    cat_hora_detalles = CatHorarioOperardorDetalle.objects.filter(
        cat_horario=cat_horario_activo
    ).order_by("grupo_horario_detalle__orden_view")
    # --- construir horario ------------->
    horario_base = Horario.objects.filter(horario_base=True).order_by("orden_view")
    dias_semana_dic = dict(DIA_SEMANA_CHOICES)
    data_horario_dic = {}
    for item_horario in horario_base:
        aux_turno = {"horario": item_horario, "data": {}}
        for dia_nro, dia_nombre in dias_semana_dic.items():
            aux_dia = {
                "nro": dia_nro,
                "nombre": dia_nombre,
                "horario_turno": None,
            }
            aux_turno.get("data").update({dia_nro: aux_dia})
        data_horario_dic.update({item_horario.cod_horario: aux_turno})
    # --- construir horario <-------------

    # --- obtener datos de turno ------------->
    for info_turno in cat_hora_detalles:
        aux_turno_es_activo = (
            horario_actual.cod_horario == info_turno.grupo_horario_detalle.horario_id
        ) and (dia_semana_actual == info_turno.grupo_horario_detalle.dia_semana)
        data_horario_dic.get(info_turno.grupo_horario_detalle.horario_id, {}).get(
            "data", {}
        ).get(info_turno.grupo_horario_detalle.dia_semana, {}).update(
            {"horario_turno": info_turno, "turno_activo": aux_turno_es_activo}
        )

    # --- obtener datos de turno <-------------

    # --- construir horario view ------------->
    data_horario = [
        {
            "horario": item_horas.get("horario"),
            "data": [item_dia for item_dia in item_horas.get("data", {}).values()],
        }
        for item_horas in data_horario_dic.values()
    ]
    # --- construir horario view <-------------

    data.update(
        {
            "dias_semana": [
                {"codigo": num, "nombre": dia} for num, dia in dias_semana_dic.items()
            ],
            "data_horario": data_horario,
            "cat_horario": cat_horario_activo,
        }
    )
    return data


def generar_programacion_operador_por_fecha(
    fecha: datetime = datetime.today(),
    fecha_actual: datetime = datetime.today(),
    toda_semana: bool = False,
    sumar_dias: int = 0,
) -> [{}]:
    f"""Permite generar programación del.

    Args:
        fecha (datetime): [fecha que se desea generar programación]
        toda_semana (bool): [True: programación de toda la semana / False: Solo de la fecha indicada]
        sumar_dias (int): [sumar número de días a la fecha indicada]

    Returns:
        list: [{"fecha", "horario", "operador", "error", "mensaje"}]
    """

    def generar_fechas_semana(
        fecha: datetime = datetime.today(), fecha_actual: datetime = datetime.today()
    ) -> [datetime]:
        fechas = []
        dia_semana = fecha.isoweekday()  # ISO 8601: Monday=1, Sunday=7
        # Calculate start of week (Monday)
        fecha_inicio = fecha - timedelta(days=dia_semana - 1)
        for i in range(0, 7):
            aux_fecha = fecha_inicio + timedelta(days=i)
            if aux_fecha.date() >= fecha_actual.date():
                fechas.append(aux_fecha)
        return fechas

    def crear_programacion_operador_por_fecha(
        fecha: datetime = datetime.today(),
    ) -> [{}]:
        insertar = []
        auxi_fecha_programacion = fecha.date()
        cat_horario_operador = CatHorarioOperardor.objects.filter(
            activo=True,
            fecha_inicio__lte=auxi_fecha_programacion,
            fecha_fin__gte=auxi_fecha_programacion,
        ).first()

        # Check if there's an active schedule catalog
        if not cat_horario_operador:
            logger.warning(
                f"No se encontró catálogo de horario activo para la fecha {auxi_fecha_programacion}"
            )
            return insertar  # Return empty list

        cat_horarios_det = CatHorarioOperardorDetalle.objects.filter(
            cat_horario_id=cat_horario_operador.codigo,
            grupo_horario_detalle__dia_semana=fecha.isoweekday(),
            grupo_horario_detalle__grupo_horario_id=cat_horario_operador.cat_horario_id,
        )
        for cat_horario_det in cat_horarios_det:
            auxi_operador_id = cat_horario_det.operador_id
            auxi_horario_id = cat_horario_det.grupo_horario_detalle.horario_id
            exist_programado = TurnoOperador.objects.filter(
                operador_id=auxi_operador_id,
                horario_id=auxi_horario_id,
                fecha_programacion=auxi_fecha_programacion,
            ).exists()
            aux_insertar = {
                "fecha": auxi_fecha_programacion,
                "horario": auxi_horario_id,
                "operador": auxi_operador_id,
                "error": None,
                "mensaje": None,
                "id": None,
            }
            if not exist_programado:
                default_data = {
                    "hora_programacion": cat_horario_det.grupo_horario_detalle.horario.inicio_horario,
                    "hora_fin_programacion": cat_horario_det.grupo_horario_detalle.horario.fin_horario,
                    "estado_turno": ESTADO_TURNO_PROGRAMADO,
                    "observacion": "programación autogenerada",
                }
                try:
                    turnope_new, _status = TurnoOperador.objects.get_or_create(
                        operador_id=auxi_operador_id,
                        horario_id=auxi_horario_id,
                        fecha_programacion=auxi_fecha_programacion,
                        defaults=default_data,
                    )
                    aux_insertar.update(
                        {"error": False, "mensaje": "ok", "id": turnope_new.id}
                    )
                except Exception as ex:
                    mensaje = "Error al crear horario operador (autogenerada)"
                    logger.warning(
                        mensaje, exc_info=True, extra={"error_data": str(ex)}
                    )
                    aux_insertar.update(
                        {"error": True, "mensaje": "No se ha generado horario operador"}
                    )
            else:
                aux_insertar.update(
                    {"error": False, "mensaje": "Se encuentra programado"}
                )
            insertar.append(aux_insertar)
        return insertar

    fechas_generar = []
    fecha_generar = fecha + timedelta(days=sumar_dias)
    if toda_semana:
        fechas_generar = generar_fechas_semana(fecha_generar, fecha_actual)
    else:
        fechas_generar.append(fecha_generar)
    # generar
    insertar = []
    for aux_fecha in fechas_generar:
        aux_insertar = crear_programacion_operador_por_fecha(aux_fecha)
        insertar += aux_insertar
    # ---
    return insertar
