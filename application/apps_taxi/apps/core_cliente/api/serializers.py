from rest_framework import serializers

from apps.core_cliente.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            "codigo",
            "telefono",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "correo",
            "genero",
            "estado",
            "servicios_realizados",
            "servicios_pendiente",
        ]
        datatables_always_serialize = [key for key in fields]
