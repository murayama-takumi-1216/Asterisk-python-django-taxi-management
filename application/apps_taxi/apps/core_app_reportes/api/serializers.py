from rest_framework import serializers

from apps.core_servicio.models import Servicio
from apps.core_turno.models import ServiciosDiaView, TurnoConductor, TurnoOperador


class TurnoConductorReporteSerializer(serializers.ModelSerializer):
    conductor_data = serializers.SerializerMethodField()
    horario_data = serializers.SerializerMethodField()
    vehiculo_data = serializers.SerializerMethodField()
    estado_turno_text = serializers.SerializerMethodField()
    fecha_programacion_view = serializers.SerializerMethodField()

    class Meta:
        model = TurnoConductor
        fields = [
            "id",
            "conductor",
            "vehiculo",
            "horario_inicio",
            "fecha_programacion",
            "fecha_programacion_view",
            "hora_programacion",
            "fecha_fin_programacion",
            "hora_fin_programacion",
            "hora_inicio",
            "hora_fin",
            "horas_efectivas",
            "monto_generado",
            "servicios_asignados",
            "servicios_atendidos",
            "servicios_cancelados",
            "servicios_cancel_conductor",
            "conductor_data",
            "horario_data",
            "vehiculo_data",
            "estado_turno",
            "estado_turno_text",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_turno_text(self, obj):
        if obj.estado_turno:
            return obj.get_estado_turno_display()
        return "-"

    def get_fecha_programacion_view(self, obj):
        if obj.fecha_programacion:
            return obj.fecha_programacion.strftime("%d/%m/%Y")
        return "-"

    def get_conductor_data(self, obj):
        conductor = {}
        if obj.conductor:
            conductor.update(
                {
                    "cod_conductor": obj.conductor.cod_conductor,
                    "nombre": obj.conductor.nombre,
                    "apellido_paterno": obj.conductor.apellido_paterno,
                    "apellido_materno": obj.conductor.apellido_materno,
                }
            )
            return conductor
        return None

    def get_vehiculo_data(self, obj):
        vehiculo = {}
        if obj.vehiculo:
            vehiculo.update(
                {
                    "codigo": obj.vehiculo.cod_vehiculo,
                    "nombre": obj.vehiculo.nom_vehiculo,
                    "marca": obj.vehiculo.marca,
                    "estado_alquilado": obj.vehiculo.estado_alquilado,
                    "estado_alquilado_text": obj.vehiculo.get_estado_alquilado_display(),
                }
            )
            return vehiculo
        return None

    def get_horario_data(self, obj):
        horario = {}
        if obj.horario_inicio:
            horario.update(
                {
                    "cod_conductor": obj.horario_inicio.cod_horario,
                    "nombre": obj.horario_inicio.nom_horario,
                    "inicio": obj.horario_inicio.inicio_horario,
                    "fin": obj.horario_inicio.fin_horario,
                }
            )
            return horario
        return None


class TurnoOperadorReporteSerializer(serializers.ModelSerializer):
    operador_data = serializers.SerializerMethodField()
    horario_data = serializers.SerializerMethodField()
    estado_turno_text = serializers.SerializerMethodField()
    fecha_programacion_view = serializers.SerializerMethodField()

    class Meta:
        model = TurnoOperador
        fields = [
            "id",
            "operador",
            "horario",
            "fecha_programacion",
            "fecha_programacion_view",
            "hora_programacion",
            "hora_fin_programacion",
            "hora_inicio",
            "hora_fin",
            "horas_efectivas",
            "llamadas_atendidos",
            "servicios_registradas",
            "servicios_asignadas",
            "operador_data",
            "horario_data",
            "estado_turno",
            "estado_turno_text",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_turno_text(self, obj):
        if obj.estado_turno:
            return obj.get_estado_turno_display()
        return "-"

    def get_fecha_programacion_view(self, obj):
        if obj.fecha_programacion:
            return obj.fecha_programacion.strftime("%d/%m/%Y")
        return "-"

    def get_operador_data(self, obj):
        operador = {}
        if obj.operador:
            operador.update(
                {
                    "cod_conductor": obj.operador.codigo,
                    "nombre": obj.operador.nombre,
                    "apellido_paterno": obj.operador.apellido_paterno,
                    "apellido_materno": obj.operador.apellido_materno,
                }
            )
            return operador
        return None

    def get_horario_data(self, obj):
        horario = {}
        if obj.horario:
            horario.update(
                {
                    "cod_conductor": obj.horario.cod_horario,
                    "nombre": obj.horario.nom_horario,
                    "inicio": obj.horario.inicio_horario,
                    "fin": obj.horario.fin_horario,
                }
            )
            return horario
        return None


class ServicioSerializer(serializers.ModelSerializer):
    cliente_data = serializers.SerializerMethodField()
    estado_atencion = serializers.SerializerMethodField()

    class Meta:
        model = Servicio
        fields = [
            "id",
            "cliente",
            "llamada",
            "operador_registra",
            "operador_asigna",
            "turno_conductor",
            "referencia_origen",
            "referencia_destino",
            "ubicacion_origen",
            "ubicacion_destino",
            "fecha_programacion",
            "hora_programacion",
            "pasajeros",
            "monto_servicio",
            "observacion_registro",
            "hora_inicio",
            "hora_fin",
            "estado",
            "estado_atencion",
            "cliente_data",
            "estado_finaliza_servicio",
        ]
        datatables_always_serialize = [key for key in fields]

    def get_cliente_data(self, obj):
        if obj.cliente:
            return {
                "codigo": obj.cliente.codigo,
                "telefono": obj.cliente.telefono,
                "nombre": obj.cliente.nombre,
                "apellido_paterno": obj.cliente.apellido_paterno,
                "apellido_materno": obj.cliente.apellido_materno,
                "correo": obj.cliente.correo,
                "genero": obj.cliente.genero,
                "servicios_realizados": obj.cliente.servicios_realizados,
                "servicios_pendiente": obj.cliente.servicios_pendiente,
            }
        return None

    def get_estado_atencion(self, obj):
        if obj.hora_inicio and obj.hora_fin:
            return "Finalizada"
        elif obj.hora_inicio:
            return "Iniciada"
        return "Pendiente"


class ServicioConDetalleSerializer(serializers.ModelSerializer):
    cliente_data = serializers.SerializerMethodField()
    turno_cond_data = serializers.SerializerMethodField()
    estado_atencion = serializers.SerializerMethodField()

    class Meta:
        model = Servicio
        fields = [
            "id",
            "cliente",
            "llamada",
            "operador_registra",
            "operador_asigna",
            "turno_conductor",
            "referencia_origen",
            "referencia_destino",
            "ubicacion_origen",
            "ubicacion_destino",
            "fecha_programacion",
            "hora_programacion",
            "pasajeros",
            "monto_servicio",
            "observacion_registro",
            "hora_inicio",
            "hora_fin",
            "estado",
            "estado_atencion",
            "cliente_data",
            "turno_cond_data",
            "estado_finaliza_servicio",
        ]
        datatables_always_serialize = [key for key in fields]

    def get_cliente_data(self, obj):
        if obj.cliente:
            return {
                "codigo": obj.cliente.codigo,
                "telefono": obj.cliente.telefono,
                "nombre": obj.cliente.nombre,
                "apellido_paterno": obj.cliente.apellido_paterno,
                "apellido_materno": obj.cliente.apellido_materno,
                "correo": obj.cliente.correo,
                "genero": obj.cliente.genero,
                "servicios_realizados": obj.cliente.servicios_realizados,
                "servicios_pendiente": obj.cliente.servicios_pendiente,
            }
        return None

    def get_turno_cond_data(self, obj):
        if obj.turno_conductor:
            conductor = {}
            if obj.turno_conductor.conductor:
                conductor.update(
                    {
                        "cod_conductor": obj.turno_conductor.conductor.cod_conductor,
                        "nombre": obj.turno_conductor.conductor.nombre,
                        "apellido_paterno": obj.turno_conductor.conductor.apellido_paterno,
                        "apellido_materno": obj.turno_conductor.conductor.apellido_materno,
                    }
                )
            return {
                "id": obj.turno_conductor.id,
                "fecha_programacion": obj.turno_conductor.fecha_programacion,
                "hora_programacion": obj.turno_conductor.hora_programacion,
                "hora_inicio": obj.turno_conductor.hora_inicio,
                "hora_fin": obj.turno_conductor.hora_fin,
                "estado_turno": obj.turno_conductor.estado_turno,
                "conductor_data": conductor,
            }
        return None

    def get_estado_atencion(self, obj):
        if obj.hora_inicio and obj.hora_fin:
            return "Finalizada"
        elif obj.hora_inicio:
            return "Iniciada"
        return "Pendiente"


class TurnoConductorViewSerializer(serializers.ModelSerializer):
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
                "licencia": obj.conductor.licencia,
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
                "matricula": obj.vehiculo.matricula,
            }
        return None

    def get_horario_data(self, obj):
        if obj.horario_inicio:
            return {
                "codigo": obj.horario_inicio.cod_horario,
                "nombre": obj.horario_inicio.nom_horario,
            }
        return None


class ServiciosDiaViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiciosDiaView
        fields = [
            "fecha",
            "llamadas_atendidas",
            "registrados",
            "asignados",
        ]

        datatables_always_serialize = [key for key in fields]


class DriverVigentesReporteSerializer(serializers.ModelSerializer):
    conductor_data = serializers.SerializerMethodField()
    horario_data = serializers.SerializerMethodField()
    vehiculo_data = serializers.SerializerMethodField()
    estado_turno_text = serializers.SerializerMethodField()
    fecha_program_ini_view = serializers.SerializerMethodField()
    fecha_program_fin_view = serializers.SerializerMethodField()

    class Meta:
        model = TurnoConductor
        fields = [
            "id",
            "conductor",
            "vehiculo",
            "horario_inicio",
            "fecha_programacion",
            "fecha_program_ini_view",
            "fecha_program_fin_view",
            "hora_programacion",
            "fecha_fin_programacion",
            "hora_fin_programacion",
            "hora_inicio",
            "hora_fin",
            "horas_efectivas",
            "conductor_data",
            "horario_data",
            "vehiculo_data",
            "estado_turno",
            "estado_turno_text",
        ]

        datatables_always_serialize = [key for key in fields]

    def get_estado_turno_text(self, obj):
        if obj.estado_turno:
            return obj.get_estado_turno_display()
        return "-"

    def get_fecha_program_ini_view(self, obj):
        if obj.fecha_programacion:
            return obj.fecha_programacion.strftime("%d/%m/%Y")
        return "-"

    def get_fecha_program_fin_view(self, obj):
        if obj.fecha_fin_programacion:
            return obj.fecha_fin_programacion.strftime("%d/%m/%Y")
        return "-"

    def get_conductor_data(self, obj):
        conductor = {}
        if obj.conductor:
            conductor.update(
                {
                    "cod_conductor": obj.conductor.cod_conductor,
                    "nombre": obj.conductor.nombre,
                    "apellido_paterno": obj.conductor.apellido_paterno,
                    "apellido_materno": obj.conductor.apellido_materno,
                    "telefono": obj.conductor.telefono,
                    "licencia": obj.conductor.licencia,
                }
            )
            return conductor
        return None

    def get_vehiculo_data(self, obj):
        vehiculo = {}
        if obj.vehiculo:
            vehiculo.update(
                {
                    "codigo": obj.vehiculo.cod_vehiculo,
                    "nombre": obj.vehiculo.nom_vehiculo,
                    "marca": obj.vehiculo.marca,
                    "matricula": obj.vehiculo.matricula,
                    "estado_alquilado": obj.vehiculo.estado_alquilado,
                    "estado_alquilado_text": obj.vehiculo.get_estado_alquilado_display(),
                }
            )
            return vehiculo
        return None

    def get_horario_data(self, obj):
        horario = {}
        if obj.horario_inicio:
            horario.update(
                {
                    "cod_conductor": obj.horario_inicio.cod_horario,
                    "nombre": obj.horario_inicio.nom_horario,
                    "inicio": obj.horario_inicio.inicio_horario,
                    "fin": obj.horario_inicio.fin_horario,
                }
            )
            return horario
        return None
