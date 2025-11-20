import logging
from time import sleep

from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ViewSet

from apps.common.constants import AMI_ID_ACTION_IN_CALL_WH
from apps.core_servicio.constants import (
    AMI_CHANNEL_ST_TO_ESTADOS_DB,
    ESTADO_LLAMADA_ENTRANTE,
)
from apps.core_servicio.models import Llamada

logger = logging.getLogger(__name__)


class LlamadaClienteBackViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    def list(self, request, *args, **kwargs):
        ast_data = {
            "data": [],
            "message": None,
            "error": None,
            "response": None,
            "action": {},
        }
        # ------------------- forma 1 ----------->>
        data_asterisk = {}
        data_asterisk2 = {}
        status_response = HTTP_400_BAD_REQUEST
        try:
            from asterisk.ami import AMIClient, Event
            from asterisk.ami import Response as ResponsePbx

            client = AMIClient(
                address=settings.ASTERISK_AMI_HOST, port=settings.ASTERISK_AMI_PORT
            )
            client.login(
                username=settings.ASTERISK_AMI_USER,
                secret=settings.ASTERISK_AMI_PASSWORD,
            )
            from asterisk.ami import SimpleAction

            action = SimpleAction(
                "CoreShowChannels",
                ActionID=AMI_ID_ACTION_IN_CALL_WH,
            )
            ast_data.update({"action": {"name": action.name, "keys": action.keys}})

            def event_listener(event: Event, **kwargs):
                if event.keys.get("ActionID", "") == AMI_ID_ACTION_IN_CALL_WH:
                    if event.name not in data_asterisk.keys():
                        data_asterisk.update({event.name: []})
                    data_asterisk.get(event.name, []).append(event.keys)
                    # ---
                    telf_caller = event.keys.get("CallerIDNum", "")
                    telf_connect = event.keys.get("ConnectedLineNum", "")
                    telf_llamada = (
                        telf_caller
                        if len(telf_caller) > len(telf_connect)
                        else telf_connect
                    )
                    if telf_llamada:
                        if telf_llamada not in data_asterisk2.keys():
                            data_asterisk2.update({telf_llamada: []})
                        data_asterisk2.get(telf_llamada, []).append(event.keys)

            client.add_event_listener(event_listener)
            future = client.send_action(action)
            sleep(settings.ASTERISK_AMI_DELAY)
            response: ResponsePbx = future.response
            if response.is_error():
                ast_data.update({"message": "Error en obtener data"})
            ast_data.update(
                {
                    # "data": data_asterisk,
                    "data2": data_asterisk2,
                    "response": response.__dict__,
                }
            )
            status_response = HTTP_200_OK
        except Exception as ex:
            mensaje = "Error en obtener datos de asterisk"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
            ast_data.update({"asterisk": {"error": str(ex), "mensaje": mensaje}})
        finally:
            client.logoff()
        # ------------------- forma 1 <<-----------

        # --------- save froma 2 ---->
        test_data = {}
        if data_asterisk2.keys():  # TODO en prueba que funcione correctamente
            for sv_telefono in data_asterisk2:
                test_data.update({sv_telefono: {}})
                grupo = data_asterisk2[sv_telefono]
                entrante = {}
                contesta = {}
                for channel in grupo:
                    aux_channel = channel.get("Channel", "")
                    aux_bridgeid = channel.get("BridgeId", "")
                    aux_linkedid = channel.get("Linkedid", "")
                    aux_uniqueid = channel.get("Uniqueid", "")
                    if aux_linkedid == aux_uniqueid:
                        if aux_channel.startswith(
                            settings.ASTERISK_AMI_FILTERCHANNEL_EX
                        ):
                            entrante = channel
                    else:
                        if aux_bridgeid and aux_channel.startswith(
                            settings.ASTERISK_AMI_FILTERCHANNEL_IN
                        ):
                            contesta = channel
                # ---
                if not entrante:
                    continue
                # ---
                test_data.get(sv_telefono, {}).update(
                    {"contesta": contesta, "entrante": entrante}
                )
                sv_linkedid = (
                    entrante.get("Linkedid")
                    if entrante.get("Linkedid")
                    else contesta.get("Linkedid", "")
                )

                sv_channel = entrante.get("Channel", "")
                sv_channel_state_desc = entrante.get("ChannelStateDesc", "")
                sv_callerid_num = entrante.get("CallerIDNum", "")
                sv_callerid_name = entrante.get("CallerIDName", "")
                sv_uniqueid = entrante.get("Uniqueid", "")
                sv_context = entrante.get("Context", "")

                sv_connected_channel = ""
                sv_connected_channel_state_desc = ""
                sv_connected_callerid_num = ""
                sv_duration = ""

                if contesta:
                    sv_connected_channel = contesta.get("Channel", "")
                    sv_connected_channel_state_desc = contesta.get(
                        "ChannelStateDesc", ""
                    )
                    sv_connected_callerid_num = contesta.get("CallerIDNum", "")
                    sv_duration = contesta.get("Duration", "")

                sv_bridgeid = (
                    entrante.get("BridgeId")
                    if entrante.get("BridgeId")
                    else contesta.get("BridgeId", "")
                )

                marca_ami_time, marca_ami_anio, marca_ami_datetime = (
                    Llamada.generar_marca_tiempo_ami()
                )
                consultar_marca_ami_time = (
                    marca_ami_time - 180
                )  # duración máxima de llamada 180 segundos (3 minutos)

                sv_estado_llamada = AMI_CHANNEL_ST_TO_ESTADOS_DB.get(
                    sv_connected_channel_state_desc, ESTADO_LLAMADA_ENTRANTE
                )
                qs_llamada_existe = Llamada.objects.filter(
                    numero=sv_telefono,
                    linkedid=sv_linkedid,
                    anio=marca_ami_anio,
                    marca_tiempo_ami__gt=consultar_marca_ami_time,
                )
                if qs_llamada_existe.exists():
                    test_data.get(sv_telefono, {}).update(
                        {"flujo1.0": "entra actualiza"}
                    )
                    llamada = qs_llamada_existe.order_by("-id").first()
                    if not llamada.bridgeid:
                        llamada.channel_state_desc = sv_channel_state_desc
                        llamada.connected_channel = sv_connected_channel
                        llamada.connected_channel_state_desc = (
                            sv_connected_channel_state_desc
                        )
                        llamada.connected_callerid_num = sv_connected_callerid_num
                        llamada.estado_llamada = sv_estado_llamada
                        llamada.bridgeid = sv_bridgeid
                        llamada.duration = sv_duration
                        llamada.save(
                            update_fields=[
                                "channel_state_desc",
                                "connected_channel",
                                "connected_channel_state_desc",
                                "connected_callerid_num",
                                "estado_llamada",
                                "bridgeid",
                                "duration",
                            ]
                        )
                        test_data.get(sv_telefono, {}).update({"flujo1.1": "actualizó"})
                    else:
                        llamada.duration = sv_duration
                        llamada.save(update_fields=["duration"])
                else:
                    test_data.get(sv_telefono, {}).update(
                        {"flujo2.0": "Crea nuevo registro"}
                    )
                    llamada = Llamada(
                        anio=marca_ami_anio,
                        fecha_llamada=marca_ami_datetime.date(),
                        hora_llamada=marca_ami_datetime.time(),
                        numero=sv_telefono,
                        estado_llamada=sv_estado_llamada,
                        channel=sv_channel,
                        channel_state_desc=sv_channel_state_desc,
                        callerid_num=sv_callerid_num,
                        callerid_name=sv_callerid_name,
                        uniqueid=sv_uniqueid,
                        context=sv_context,
                        connected_channel=sv_connected_channel,
                        connected_channel_state_desc=sv_connected_channel_state_desc,
                        connected_callerid_num=sv_connected_callerid_num,
                        bridgeid=sv_bridgeid,
                        duration=sv_duration,
                        linkedid=sv_linkedid,
                        marca_tiempo_ami=marca_ami_time,
                    )
                    llamada.save()
        # --------- save froma 2 <----

        return Response(ast_data, status=status_response)
