from rest_framework import serializers

from apps.core_turno.constants import (
    ESTADO_TURNO_ACTIVO,
    ESTADO_TURNO_PENDIENTE,
    ESTADO_TURNO_PROGRAMADO,
)
from apps.core_turno.models import TurnoConductor
from apps.core_vehiculo.constants import (
    ESTADO_ALQUILER_ACTIVO,
    ESTADO_ALQUILER_PENDIENTE,
    ESTADO_ALQUILER_PROGRAMADO,
)
from apps.core_vehiculo.models import AlquilerVehiculo, Vehiculo


class VehiculoParaAlquilerSerializer(serializers.ModelSerializer):
    estado_vehiculo_text = serializers.SerializerMethodField()
    estado_alquilado_text = serializers.SerializerMethodField()
    alquiler_data = serializers.SerializerMethodField()

    class Meta:
        model = Vehiculo
        fields = [
            "cod_vehiculo",
            "nom_vehiculo",
            "descripcion",
            "estado_vehiculo",
            "estado_alquilado",
            "estado_vehiculo_text",
            "estado_alquilado_text",
            "marca",
            "numero_vin",
            "alquiler_data",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_vehiculo_text(self, obj):
        return obj.get_estado_vehiculo_display() if obj.estado_vehiculo else ""

    def get_estado_alquilado_text(self, obj):
        return obj.get_estado_alquilado_display() if obj.estado_alquilado else ""

    def get_alquiler_data(self, obj):
        data_out = []
        alquileres = AlquilerVehiculo.objects.filter(
            vehiculo_id=obj.cod_vehiculo,
            estado__in=[
                ESTADO_ALQUILER_PENDIENTE,
                ESTADO_ALQUILER_PROGRAMADO,
                ESTADO_ALQUILER_ACTIVO,
            ],
        ).order_by("-fecha_prog_inicio")
        if alquileres:
            data_out = [
                {
                    "codigo": alquiler.id,
                    "fecha_prog_inicio": alquiler.fecha_prog_inicio,
                    "fecha_prog_fin": alquiler.fecha_prog_fin,
                    "fecha_inicio": alquiler.fecha_inicio,
                    "fecha_fin": alquiler.fecha_fin,
                    "entrega_radio": alquiler.entrega_radio,
                    "estado": alquiler.estado,
                    "estado_text": alquiler.get_estado_display(),
                    "conductor": (
                        {
                            "cod_conductor": alquiler.conductor.cod_conductor,
                            "nombre": alquiler.conductor.nombre,
                            "apellido_paterno": alquiler.conductor.apellido_paterno,
                            "apellido_materno": alquiler.conductor.apellido_materno,
                            "estado_text": alquiler.conductor.get_estado_display(),
                        }
                        if alquiler.conductor
                        else {}
                    ),
                }
                for alquiler in alquileres
            ]
        return data_out


class AlquilerVehiculoParaAlquilerSerializer(serializers.ModelSerializer):
    conductor_data = serializers.SerializerMethodField()
    vehiculo_data = serializers.SerializerMethodField()

    class Meta:
        model = AlquilerVehiculo
        fields = [
            "vehiculo",
            "conductor",
            "monto_alquiler",
            "fecha_prog_inicio",
            "hora_prog_inicio",
            "fecha_prog_fin",
            "hora_prog_fin",
            "fecha_inicio",
            "hora_inicio",
            "fecha_fin",
            "hora_fin",
            "estado",
            "observacion",
            "entrega_radio",
            "conductor_data",
            "vehiculo_data",
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
            }
        return None

    def get_vehiculo_data(self, obj):
        if obj.vehiculo:
            return {
                "codigo": obj.vehiculo.cod_vehiculo,
                "nombre": obj.vehiculo.nom_vehiculo,
                "marca": obj.vehiculo.marca,
                "modelo": obj.vehiculo.modelo,
            }
        return None


class VehiculoParaTurnoConductorSerializer(serializers.ModelSerializer):
    estado_vehiculo_text = serializers.SerializerMethodField()
    estado_alquilado_text = serializers.SerializerMethodField()
    alquiler_data = serializers.SerializerMethodField()
    turno_data = serializers.SerializerMethodField()

    class Meta:
        model = Vehiculo
        fields = [
            "cod_vehiculo",
            "nom_vehiculo",
            "descripcion",
            "estado_vehiculo",
            "estado_alquilado",
            "estado_vehiculo_text",
            "estado_alquilado_text",
            "marca",
            "numero_vin",
            "alquiler_data",
            "turno_data",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_vehiculo_text(self, obj):
        return obj.get_estado_vehiculo_display() if obj.estado_vehiculo else ""

    def get_estado_alquilado_text(self, obj):
        return obj.get_estado_alquilado_display() if obj.estado_alquilado else ""

    def get_alquiler_data(self, obj):
        data_out = []
        alquileres = AlquilerVehiculo.objects.filter(
            vehiculo_id=obj.cod_vehiculo,
            estado__in=[
                ESTADO_ALQUILER_PENDIENTE,
                ESTADO_ALQUILER_PROGRAMADO,
                ESTADO_ALQUILER_ACTIVO,
            ],
        ).order_by("-fecha_prog_inicio")
        if alquileres:
            data_out = [
                {
                    "codigo": alquiler.id,
                    "fecha_prog_inicio": alquiler.fecha_prog_inicio,
                    "fecha_prog_fin": alquiler.fecha_prog_fin,
                    "fecha_inicio": alquiler.fecha_inicio,
                    "fecha_fin": alquiler.fecha_fin,
                    "entrega_radio": alquiler.entrega_radio,
                    "estado": alquiler.estado,
                    "estado_text": alquiler.get_estado_display(),
                    "conductor": (
                        {
                            "cod_conductor": alquiler.conductor.cod_conductor,
                            "nombre": alquiler.conductor.nombre,
                            "apellido_paterno": alquiler.conductor.apellido_paterno,
                            "apellido_materno": alquiler.conductor.apellido_materno,
                            "estado_text": alquiler.conductor.get_estado_display(),
                        }
                        if alquiler.conductor
                        else {}
                    ),
                }
                for alquiler in alquileres
            ]
        return data_out

    def get_turno_data(self, obj):
        data_out = []
        turno_conductores = TurnoConductor.objects.filter(
            vehiculo_id=obj.cod_vehiculo,
            estado_turno__in=[
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_ACTIVO,
            ],
        ).order_by("-fecha_programacion", "-hora_programacion")
        if turno_conductores:
            data_out = [
                {
                    "codigo": turno_conductor.id,
                    "horario": turno_conductor.horario_inicio_id,
                    "horario_nombre": turno_conductor.horario_inicio.nom_horario,
                    "fecha_programacion": turno_conductor.fecha_programacion,
                    "hora_programacion": turno_conductor.hora_programacion,
                    "hora_inicio": turno_conductor.hora_inicio,
                    "hora_fin": turno_conductor.hora_fin,
                    "estado_turno": turno_conductor.estado_turno,
                    "estado_turno_text": turno_conductor.get_estado_turno_display(),
                }
                for turno_conductor in turno_conductores
            ]
        return data_out
