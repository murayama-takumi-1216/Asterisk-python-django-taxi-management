from rest_framework import serializers

from apps.core_conductor.models import Conductor


class ConductorSerializer(serializers.ModelSerializer):
    estado_text = serializers.SerializerMethodField()

    class Meta:
        model = Conductor
        fields = [
            "cod_conductor",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "direccion",
            "telefono",
            "estado",
            "alquileres_realizados",
            "alquileres_cancelados",
            "estado_text",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_text(self, obj):
        return obj.get_estado_display() if obj.estado else ""
