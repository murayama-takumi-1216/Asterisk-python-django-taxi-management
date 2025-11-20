from rest_framework import serializers

from apps.core_operador.models import Operador


class OperadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operador
        fields = [
            "codigo",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "extension",
            "alias",
            "user",
            "estado",
        ]

        datatables_always_serialize = [key for key in fields]
