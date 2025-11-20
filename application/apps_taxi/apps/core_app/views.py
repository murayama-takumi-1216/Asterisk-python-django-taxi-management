import json
import logging
from datetime import datetime, timedelta

from allauth.account.views import SignupView
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.views.generic import TemplateView

from apps.common.utils import DataLoginTurnoOperador
from apps.common.views import BaseProtectedAppView
from apps.core_app.constants import REFRESH_LLAMADAS_FRONT_OPERADOR
from apps.core_app.forms import UserRegistrationForm
from apps.core_operador.models import Operador
from apps.core_turno.constants import (
    ESTADO_TURNO_ACTIVO,
    ESTADO_TURNO_CONCLUIDO,
    ESTADO_TURNO_PROGRAMADO,
)
from apps.core_turno.models import TurnoOperador
from apps.localconfig.models import EnvironmentVariable

logger = logging.getLogger(__name__)
envs = EnvironmentVariable()


class InitialPageView(BaseProtectedAppView, TemplateView):
    template_name = "core_app/initial_page.html"

    def dispatch(self, request, *args, **kwargs):
        return super(InitialPageView, self).dispatch(request, *args, **kwargs)


class DashboardView(BaseProtectedAppView, TemplateView):
    template_name = "core_app/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)
        operadores = Operador.objects.filter(estado=True).order_by("nombre")

        data_operadores = []
        for operador in operadores:
            aux_data = {
                "llamadas_atendidos": "",
                "servicios_registradas": "",
                "servicios_asignadas": "",
                "operador": {
                    "codigo": operador.codigo,
                    "nombre": operador.nombre,
                    "apellido_paterno": operador.apellido_paterno,
                },
            }
            turnos = (
                TurnoOperador.objects.values(
                    "llamadas_atendidos",
                    "servicios_registradas",
                    "servicios_asignadas",
                )
                .filter(
                    operador=operador,
                    fecha_programacion__gte=fecha_inicial.date(),
                    fecha_programacion__lte=fecha_hoy.date(),
                    estado_turno=ESTADO_TURNO_CONCLUIDO,
                )
                .order_by("fecha_programacion", "hora_programacion")
            )
            aux_01 = ["0"]
            aux_02 = ["0"]
            aux_03 = ["0"]
            for turno in turnos:
                aux_01.append(str(turno.get("llamadas_atendidos", 0)))
                aux_02.append(str(turno.get("servicios_registradas", 0)))
                aux_03.append(str(turno.get("servicios_asignadas", 0)))
            aux_data.update({"llamadas_atendidos": ",".join(aux_01)})
            aux_data.update({"servicios_registradas": ",".join(aux_02)})
            aux_data.update({"servicios_asignadas": ",".join(aux_03)})
            data_operadores.append(aux_data)
        context.update(
            {
                "data_operadores": json.dumps(data_operadores, cls=DjangoJSONEncoder),
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context


class ProcessView(BaseProtectedAppView, TemplateView):
    template_name = "core_app/app_process.html"

    def get_context_data(self, **kwargs):
        # TODO mejorar el proceso de carga de esta página
        #  (eliminar variables no utilizadas - ejm turnos_operador_activar)
        context = super(ProcessView, self).get_context_data(**kwargs)
        # --- inicar sesion de operador ----->
        login_turno_operador = DataLoginTurnoOperador(self.request)
        # --- inicar sesion de operador <-----
        if not login_turno_operador.operador:
            self.template_name = "core_app/app_process_sesion.html"
            return context

        # --- obtener datos de turno ------------->
        fecha_hoy = login_turno_operador.fecha_actual
        fecha_inicial = fecha_hoy - timedelta(hours=9)
        fecha_final = fecha_hoy + timedelta(hours=2)
        if fecha_inicial.date() == fecha_final.date():
            turnos_operador_activar = TurnoOperador.objects.filter(
                fecha_programacion__gte=fecha_inicial.date(),
                hora_programacion__gte=fecha_inicial.time(),
                hora_programacion__lte=fecha_final.time(),
                operador_id=login_turno_operador.operador.codigo,
            ).order_by("fecha_programacion", "hora_programacion")
        else:
            turnos_operador_activar = (
                TurnoOperador.objects.filter(
                    operador_id=login_turno_operador.operador.codigo
                )
                .filter(
                    Q(
                        fecha_programacion=fecha_inicial.date(),
                        hora_programacion__gte=fecha_inicial.time(),
                    )
                    | Q(
                        fecha_programacion=fecha_final.date(),
                        hora_programacion__lte=fecha_final.time(),
                    )
                )
                .order_by("fecha_programacion", "hora_programacion")
            )

        # mostrar la lista horarios
        fecha_inicial_view = fecha_hoy - timedelta(hours=15)
        fecha_final_view = fecha_hoy + timedelta(days=3)
        if fecha_inicial_view.date() != fecha_hoy.date():
            turnos_operador_view = (
                TurnoOperador.objects.filter(
                    Q(
                        fecha_programacion=fecha_inicial_view.date(),
                        hora_programacion__gte=fecha_inicial_view.time(),
                    )
                    | Q(
                        fecha_programacion__gte=fecha_hoy.date(),
                    )
                )
                .filter(fecha_programacion__lte=fecha_final_view.date())
                .order_by("fecha_programacion", "hora_programacion")
            )
        else:
            turnos_operador_view = TurnoOperador.objects.filter(
                fecha_programacion__gte=fecha_inicial_view.date(),
                fecha_programacion__lte=fecha_final_view.date(),
            ).order_by("fecha_programacion", "hora_programacion")

        # ------

        turno_operador_seleccionado = None
        if turnos_operador_activar:
            for turno in turnos_operador_activar:
                if (
                    login_turno_operador.turno_operador
                    and turno.id == login_turno_operador.turno_operador.id
                ):
                    turno_operador_seleccionado = turno

        # refrescar llamadas de operador
        try:
            refresh_llamadas = envs.get_variable(
                "REFRESH_LLAMADAS_FRONT_OPERADOR", REFRESH_LLAMADAS_FRONT_OPERADOR
            )
            refresh_llamadas = int(refresh_llamadas)
        except Exception as ex:
            mensaje = "Error al recuperar REFRESH_LLAMADAS_FRONT_OPERADOR"
            logger.warning(mensaje, exc_info=True, extra={"error_data": str(ex)})
            refresh_llamadas = 5
        context.update(
            {
                "refresh_llamadas": refresh_llamadas,
                "turnos_operador_view": turnos_operador_view,
                "turnos_operador": turnos_operador_activar,
                "turno_operador_select": turno_operador_seleccionado,
            }
        )
        if not turno_operador_seleccionado:
            self.template_name = "core_app/app_process_sesion.html"
        # --- obtener datos de turno <-------------
        return context


class OperadorReporteTurnoView(BaseProtectedAppView, TemplateView):
    template_name = "core_app/app_process_reporte.html"

    def get_context_data(self, **kwargs):
        context = super(OperadorReporteTurnoView, self).get_context_data(**kwargs)
        # operador
        operador = Operador.objects.filter(user=self.request.user).first()
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=8)
        fecha_final = fecha_hoy + timedelta(hours=1)
        turnos_cerrados_operador = []
        if operador:
            turnos_cerrados_operador = TurnoOperador.objects.filter(
                fecha_programacion__gte=fecha_inicial.date(),
                fecha_programacion__lte=fecha_final.date(),
                operador=operador,
                estado_turno__in=[ESTADO_TURNO_ACTIVO, ESTADO_TURNO_CONCLUIDO],
            ).order_by("-fecha_programacion", "-hora_programacion")
        turnos_programados_operador = []
        fecha_inicial_prog = fecha_hoy - timedelta(hours=9)
        fecha_final_prog = fecha_hoy + timedelta(days=10)
        if operador:
            turnos_programados_operador = TurnoOperador.objects.filter(
                fecha_programacion__gte=fecha_inicial_prog.date(),
                fecha_programacion__lte=fecha_final_prog.date(),
                operador=operador,
                estado_turno__in=[ESTADO_TURNO_PROGRAMADO, ESTADO_TURNO_ACTIVO],
            ).order_by("fecha_programacion", "hora_programacion")

        context.update(
            {
                "turnos_cerrados_operador": turnos_cerrados_operador,
                "turnos_programados_operador": turnos_programados_operador,
            }
        )
        # --- obtener datos de turno <-------------
        return context


class loginView(TemplateView):
    template_name = "pages/login.html"


class registerView(SignupView):
    """
    Custom registration view using django-allauth's SignupView.
    This ensures proper email verification flow is followed.
    """

    template_name = "pages/register.html"
    form_class = UserRegistrationForm

    # The success_url is handled by allauth, which will redirect to:
    # - Email confirmation page if ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    # - Login page or success URL if email verification is optional/none