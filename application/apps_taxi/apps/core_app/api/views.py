import logging
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.exceptions import APIException, ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer

from apps.common.utils import obtener_fecha_hora_actual
from apps.common.views import ProtectedOperadorApiView
from apps.core_app.api.paginations import TurnoOperadorRSPagination
from apps.core_app.api.serializers import TurnoOperadorSerializer as TurOpeSerializer
from apps.core_operador.utils import generar_programacion_operador_por_fecha
from apps.core_servicio.models import Llamada, Servicio
from apps.core_turno.api.serializers import TurnoOperadorSerializer
from apps.core_turno.constants import ESTADO_TURNO_ACTIVO, ESTADO_TURNO_CONCLUIDO
from apps.core_turno.models import TurnoOperador

logger = logging.getLogger(__name__)


class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response({"jeje": "ok"}, status=HTTP_200_OK, content_type="json")

    def post(self, request, *args, **kwargs):
        data_response = {"codigo": "6000", "mensaje": "No se recibió datos", "datos": 0}
        try:
            data_request = request.data.copy()
        except Exception as ex:
            mensaje = "error al obtener información del cliente para atención"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
            data_response.update({"mensaje": mensaje})
            return Response(data_response, status=HTTP_400_BAD_REQUEST)
        try:
            username = data_request.get("user_name")
            password = data_request.get("user_password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    fecha_actual = datetime.today()
                    generar_programacion_operador_por_fecha(
                        fecha_actual, fecha_actual, True, 8
                    )
                except Exception as ex:
                    mensaje = (
                        "Error al generar automáticamente programación de operadores"
                    )
                    logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
                return Response({"login": True}, status=HTTP_200_OK)
        except Exception as ex:
            mensaje = "error al ingresar login"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response({"login": False}, status=HTTP_200_OK)


class logoutView(LoginRequiredMixin, APIView):

    def get(self, request):
        logout(request)

        return Response({"logout": True}, status=HTTP_200_OK)


class LoadTimeServerView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(obtener_fecha_hora_actual(), status=HTTP_200_OK)


class TurnoOperadorInicioTurnoViewSet(ProtectedOperadorApiView, ViewSet):

    def partial_update(self, request, *args, **kwargs):
        data_pk = kwargs.get("pk", "")
        data = request.data.copy()
        turno_codigo = data.get("codigo_turno", "")
        if data_pk == "" or data_pk != turno_codigo:
            mensaje = "No se permite realizar operacion"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        login_turno_operador = self.get_login_turno_operador()
        operador = login_turno_operador.operador
        if not operador:
            mensaje = "No se encuentra registro del operador"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        turno_operador = login_turno_operador.turno_operador
        if not turno_operador:
            turno_operador = TurnoOperador.objects.filter(id=turno_codigo).first()
        data_out = {}
        try:
            fecha_hoy = datetime.today()
            # actualizar turnos inactivos
            TurnoOperador.objects.filter(
                operador_id=turno_operador.operador_id, estado_turno=ESTADO_TURNO_ACTIVO
            ).update(
                hora_fin=fecha_hoy.time(),
                estado_turno=ESTADO_TURNO_CONCLUIDO,
                observacion="Se cerró forzado, inicio otro turno id={}".format(
                    turno_operador.id
                ),
            )
            # actualizar turno activo
            if turno_operador.estado_turno == ESTADO_TURNO_CONCLUIDO:
                turno_operador.hora_fin = None
                turno_operador.estado_turno = ESTADO_TURNO_ACTIVO
                turno_operador.save(update_fields=["hora_fin", "estado_turno"])
            else:
                turno_operador.hora_inicio = fecha_hoy.time()
                turno_operador.estado_turno = ESTADO_TURNO_ACTIVO
                turno_operador.save(update_fields=["hora_inicio", "estado_turno"])
            # session
            request.session["data.codigo_turno_operador"] = turno_operador.id
        except Exception as ex:
            mensaje = "Error al actualizar, vuelva intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = TurnoOperadorSerializer(turno_operador, many=False)
        data_out.update({"data": serializer.data, "message": "ok"})
        return Response(data_out, status=HTTP_200_OK)


class TurnoOperadorCerrarTurnoViewSet(ProtectedOperadorApiView, ViewSet):

    def partial_update(self, request, *args, **kwargs):
        data_pk = kwargs.get("pk", "")
        data = request.data.copy()
        turno_codigo = data.get("codigo_turno", "")
        if data_pk == "" or data_pk != turno_codigo:
            mensaje = "No se permite realizar operación"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        login_turno_operador = self.get_login_turno_operador()
        turno_operador = login_turno_operador.turno_operador
        if not turno_operador:
            mensaje = "No se encuentra registro de turno del operador"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        data_out = {}
        try:
            count_llamadas_atendidos = Llamada.contar_llamadas_contestadas(
                turno_operador
            )
            count_servicios_registradas = Servicio.contar_registros_operador(
                turno_operador
            )
            count_servicios_asignadas = Servicio.contar_asignados_operador(
                turno_operador
            )
            turno_operador.hora_fin = login_turno_operador.fecha_actual.time()
            turno_operador.llamadas_atendidos = count_llamadas_atendidos
            turno_operador.servicios_registradas = count_servicios_registradas
            turno_operador.servicios_asignadas = count_servicios_asignadas
            turno_operador.estado_turno = ESTADO_TURNO_CONCLUIDO
            turno_operador.observacion = "Se cerró correctamente el turno"
            turno_operador.save(
                update_fields=[
                    "hora_fin",
                    "llamadas_atendidos",
                    "servicios_registradas",
                    "servicios_asignadas",
                    "estado_turno",
                    "observacion",
                ]
            )
            # session
            request.session["data.codigo_turno_operador"] = None
        except Exception as ex:
            mensaje = "Error al actualizar, vuelva intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = TurnoOperadorSerializer(turno_operador, many=False)
        data_out.update({"data": serializer.data, "message": "ok"})
        return Response(data_out, status=HTTP_200_OK)


class TurnoOperadorModelViewSet(ProtectedOperadorApiView, ModelViewSet):
    serializer_class = TurOpeSerializer
    queryset = TurnoOperador.objects.all()
    pagination_class = TurnoOperadorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        usuario = self.request.user
        queryset = queryset.filter(operador__user=usuario)
        return queryset.order_by("-id")


class TurnoOperadorResumenApiView(ProtectedOperadorApiView, APIView):

    def get(self, request):
        login_turno_operador = self.get_login_turno_operador()
        turno_operador = login_turno_operador.turno_operador

        zrs_turnooperador = TurOpeSerializer(turno_operador, many=False)

        return Response(
            {"data": {"turno_operador": zrs_turnooperador.data}}, status=HTTP_200_OK
        )
