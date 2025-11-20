from rest_framework import serializers

from apps.core_maestras.models import Horario
from apps.core_turno.models import TurnoConductor, TurnoOperador


class TurnoOperadorSerializer(serializers.ModelSerializer):
    operador_data = serializers.SerializerMethodField()

    class Meta:
        model = TurnoOperador
        fields = [
            "id",
            "operador",
            "horario",
            "extension_numero",
            "fecha_programacion",
            "hora_programacion",
            "hora_inicio",
            "hora_fin",
            "estado_turno",
            "llamadas_atendidos",
            "servicios_registradas",
            "servicios_asignadas",
            "operador_data",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_operador_data(self, obj):
        if obj.operador:
            return {
                "codigo": obj.operador.codigo,
                "nombre": obj.operador.nombre,
                "apellido_paterno": obj.operador.apellido_paterno,
                "apellido_materno": obj.operador.apellido_materno,
            }
        return None


class TurnoConductorSerializer(serializers.ModelSerializer):
    conductor_data = serializers.SerializerMethodField()
    vehiculo_data = serializers.SerializerMethodField()
    horario_data = serializers.SerializerMethodField()

    class Meta:
        model = TurnoConductor
        fields = [
            "id",
            "nombre",
            "vehiculo",
            "conductor",
            "horario_inicio",
            "fecha_programacion",
            "hora_programacion",
            "hora_inicio",
            "hora_fin",
            "estado_turno",
            "servicios_asignados",
            "servicios_atendidos",
            "servicios_cancelados",
            "conductor_data",
            "vehiculo_data",
            "horario_data",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_conductor_data(self, obj):
        if obj.conductor:
            return {
                "codigo": obj.conductor.cod_conductor,
                "nombre": obj.conductor.nombre,
                "apellido_paterno": obj.conductor.apellido_paterno,
                "apellido_materno": obj.conductor.apellido_materno,
                "alquileres_realizados": obj.conductor.alquileres_realizados,
                "alquileres_cancelados": obj.conductor.alquileres_cancelados,
                "direccion": obj.conductor.direccion,
                "telefono": obj.conductor.telefono,
            }
        return None

    def get_vehiculo_data(self, obj):
        if obj.vehiculo:
            return {
                "codigo": obj.vehiculo.cod_vehiculo,
                "nombre": obj.vehiculo.nom_vehiculo,
            }
        return None

    def get_horario_data(self, obj):
        if obj.horario_inicio:
            return {
                "codigo": obj.horario_inicio.cod_horario,
                "nombre": obj.horario_inicio.nom_horario,
            }
        return None


class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = [
            "cod_horario",
            "nom_horario",
            "inicio_horario",
            "fin_horario",
            "estado",
            "orden_view",
        ]

        datatables_always_serialize = [key for key in fields]
