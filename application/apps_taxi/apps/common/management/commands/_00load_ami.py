import json
import logging

from django.conf import settings
from django.core.management import BaseCommand

from apps.localconfig.models import EnvironmentVariable


logger = logging.getLogger(__name__)

# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         file_name = "apps/localconfig/fixtures/variables.json"
#         variables_creadas = []
#         with open(file_name, "r") as json_file:
#             data = json.load(json_file)
#             for var in data:
#                 name_field = var.get("fields").get("name")
#                 variable = EnvironmentVariable.objects.filter(name=name_field).first()
#                 if not variable:
#                     variables_creadas.append(name_field)
#                     EnvironmentVariable.objects.create(**var.get("fields"))
#         if variables_creadas:
#             self.stdout.write(
#                 self.style.SUCCESS(
#                     "Se crearon las variables {} satisfactoriamente".format(
#                         ", ".join(variables_creadas)
#                     )
#                 )
#             )
#         else:
#             self.stdout.write(self.style.SUCCESS("Ninguna variable creada"))
#

# -----------------------
from asterisk.ami import AMIClient, AMIClientAdapter

def handle_event(event):
    event_type = event.get("Event", "")
    if event_type in ["Newchannel", "Dial", "Hangup"]:
        print(f"Evento filtrado ({event_type}):")
        print(event)

def main():
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

    except Exception as ex:
        mensaje = "Error en obtener datos de asterisk"
        logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})

    # client = AMIClient(address='127.0.0.1', port=5038)
    # client.login(username='monitor', secret='yourpassword')
    adapter = AMIClientAdapter(client)

    # Escuchar eventos
    client.add_event_listener(handle_event)

    print("Monitoreando eventos filtrados... Presiona Ctrl+C para salir.")
    try:
        adapter.run_forever()
    except KeyboardInterrupt:
        print("Desconectando...")
        client.logoff()

if __name__ == "__main__":
    main()
