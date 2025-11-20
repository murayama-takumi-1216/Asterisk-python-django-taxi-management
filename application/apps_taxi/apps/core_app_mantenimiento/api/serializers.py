from rest_framework import serializers

from apps.core_conductor.models import Conductor
from apps.core_operador.models import Operador
from apps.core_vehiculo.models import Vehiculo


class ConductorSerializer(serializers.ModelSerializer):
    estado_text = serializers.SerializerMethodField()

    class Meta:
        model = Conductor
        fields = [
            "cod_conductor",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "estado",
            "direccion",
            "telefono",
            "modified",
            "modified_by",
            "alquileres_realizados",
            "alquileres_cancelados",
            "estado_text",
            "licencia",
            "clase",
            "fecha_vencimiento",
            "estado_eeuu",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_text(self, obj):
        return obj.get_estado_display() if obj.estado else ""


class VehiculoSerializer(serializers.ModelSerializer):
    estado_vehiculo_text = serializers.SerializerMethodField()
    estado_alquilado_text = serializers.SerializerMethodField()

    class Meta:
        model = Vehiculo
        fields = [
            "cod_vehiculo",
            "nom_vehiculo",
            "descripcion",
            "marca",
            "numero_vin",
            "modelo",
            "matricula",
            "estado_vehiculo",
            "estado_alquilado",
            "observacion",
            "para_alquiler",
            "estado_vehiculo_text",
            "estado_alquilado_text",
            "modified",
            "modified_by",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_vehiculo_text(self, obj):
        return obj.get_estado_vehiculo_display() if obj.estado_vehiculo else ""

    def get_estado_alquilado_text(self, obj):
        return obj.get_estado_alquilado_display() if obj.estado_alquilado else ""


class OperadorSerializer(serializers.ModelSerializer):
    estado_text = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Operador
        fields = [
            "codigo",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "alias",
            "extension",
            "estado",
            "estado_text",
            "rogramacion_automatica",
            "user",
            "user_name",
            "sesion_turno_activa",
            "grupo_horario",
            "modified",
            "modified_by",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_text(self, obj):
        return "Activo" if obj.estado else "Inactivo"

    def get_user_name(self, obj):
        if obj.user:
            return obj.user.username
        return ""
