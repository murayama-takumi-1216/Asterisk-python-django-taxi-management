from rest_framework import serializers

from apps.core_turno.models import TurnoOperador


class TurnoOperadorSerializer(serializers.ModelSerializer):
    operador_data = serializers.SerializerMethodField()
    estado_turno_text = serializers.SerializerMethodField()
    horario_data = serializers.SerializerMethodField()

    class Meta:
        model = TurnoOperador
        fields = [
            "id",
            "operador",
            "horario",
            "extension_numero",
            "fecha_programacion",
            "hora_programacion",
            "hora_fin_programacion",
            "hora_inicio",
            "hora_fin",
            "estado_turno",
            "llamadas_atendidos",
            "servicios_registradas",
            "servicios_asignadas",
            "operador_data",
            "estado_turno_text",
            "horario_data",
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

    def get_estado_turno_text(self, obj):
        if obj.estado_turno:
            return obj.get_estado_turno_display()
        return None

    def get_horario_data(self, obj):
        if obj.horario:
            return {
                "codigo": obj.horario.cod_horario,
                "nombre": obj.horario.nom_horario,
                "inicio": obj.horario.inicio_horario,
                "fin": obj.horario.fin_horario,
            }
        return None
