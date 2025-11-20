import logging
#
# from django.conf import settings

# # -----------------------
# from asterisk.ami import AMIClient, AMIClientAdapter, Event
#
#
# # from asterisk.ami import Response as ResponsePbx
#
# def handle_event(event):
#     event_type = event.get("Event", "")
#     if event_type in ["Newchannel", "Dial", "Hangup"]:
#         print(f"Evento filtrado ({event_type}):")
#         print(event)
#
#
# def main():
#     try:
#         client = AMIClient(
#             # address=settings.ASTERISK_AMI_HOST, port=settings.ASTERISK_AMI_PORT
#             address="67.81.225.200", port=7777
#         )
#         client.login(
#             # username=settings.ASTERISK_AMI_USER,
#             # secret=settings.ASTERISK_AMI_PASSWORD,
#             username="taxipaterson",
#             secret="TaxiPaterson2024!",
#         )
#
#     except Exception as ex:
#         mensaje = "Error en obtener datos de asterisk"
#         print("errro ------------->", ex)
#         logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
#
#     # client = AMIClient(address='127.0.0.1', port=5038)
#     # client.login(username='monitor', secret='yourpassword')
#     adapter = AMIClientAdapter(client)
#
#     # Escuchar eventos
#     client.add_event_listener(handle_event)
#
#     print("Monitoreando eventos filtrados... Presiona Ctrl+C para salir.")
#     try:
#         adapter.run_forever()
#     except KeyboardInterrupt:
#         print("errro ------------->", ex)
#         print("Desconectando...")
#         client.logoff()
#
#
# if __name__ == "__main__":
#     main()


# ------------------------------------------------------------ --
from django.core.management.base import BaseCommand
from asterisk.ami import AMIClient, AMIClientAdapter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Monitorea eventos de llamadas en Asterisk usando AMI."

    def handle(self, *args, **kwargs):
        self.stdout.write("Conectando al AMI de Asterisk...")

        try:
            client = AMIClient(
                # address=settings.ASTERISK_AMI_HOST, port=settings.ASTERISK_AMI_PORT
                address="67.81.225.200", port=7777
            )
        except Exception as ex:
            mensaje = "Error en obtener datos de asterisk"
            print("errro ------------->", ex)
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})

        # client = AMIClient(address='127.0.0.1', port=5038)

        try:
            # client.login(username='monitor', secret='yourpassword')
            client.login(
                # username=settings.ASTERISK_AMI_USER,
                # secret=settings.ASTERISK_AMI_PASSWORD,
                username="taxipaterson",
                secret="TaxiPaterson2024!",
            )
            adapter = AMIClientAdapter(client)

            # Función para manejar eventos
            def handle_event(event):
                event_type = event.get("Event", "")
                if event_type in ["Newchannel", "Dial", "Hangup"]:
                    self.stdout.write(f"Evento filtrado ({event_type}): {event}")

                    # Procesa y guarda en base de datos (ejemplo)
                    # from myapp.models import CallEvent
                    # CallEvent.objects.create(event_type=event_type, data=event)

            # Escuchar eventos
            client.add_event_listener(handle_event)
            self.stdout.write("Monitoreando eventos... Presiona Ctrl+C para salir.")
            adapter.run_forever()

        except KeyboardInterrupt:
            self.stdout.write("Desconectando...")
            print("KeyboardInterrupt ------------->")
            client.logoff()

        except Exception as e:
            print("Exception ------------->", e)
            self.stderr.write(f"Error: {e}")
