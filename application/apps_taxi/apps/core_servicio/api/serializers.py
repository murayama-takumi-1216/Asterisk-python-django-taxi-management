from rest_framework import serializers

from apps.core_servicio.models import Llamada, Servicio


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
            vehiculo = {}
            if obj.turno_conductor.vehiculo:
                vehiculo.update(
                    {
                        "nombre": obj.turno_conductor.vehiculo.nom_vehiculo,
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
                "vehiculo_data": vehiculo,
            }
        return None

    def get_estado_atencion(self, obj):
        if obj.hora_inicio and obj.hora_fin:
            return "Finalizada"
        elif obj.hora_inicio:
            return "Iniciada"
        return "Pendiente"


class ServicioConDetalleExtraSerializer(serializers.ModelSerializer):
    cliente_data = serializers.SerializerMethodField()
    turno_cond_data = serializers.SerializerMethodField()
    estado_atencion = serializers.SerializerMethodField()
    text_estado_finaliza_servicio = serializers.SerializerMethodField()
    text_horario = serializers.SerializerMethodField()

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
            "text_estado_finaliza_servicio",
            "text_horario",
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
            vehiculo = {}
            if obj.turno_conductor.vehiculo:
                vehiculo.update(
                    {
                        "cod_vehiculo": obj.turno_conductor.vehiculo.cod_vehiculo,
                        "nom_vehiculo": obj.turno_conductor.vehiculo.nom_vehiculo,
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
                "vehiculo_data": vehiculo,
            }
        return None

    def get_estado_atencion(self, obj):
        if obj.hora_inicio and obj.hora_fin:
            return "Finalizada"
        elif obj.hora_inicio:
            return "Iniciada"
        return "Pendiente"

    def get_text_estado_finaliza_servicio(self, obj):
        if obj.estado_finaliza_servicio:
            return obj.get_estado_finaliza_servicio_display()
        return "-"

    def get_text_horario(self, obj):
        if obj.horario:
            return obj.horario.nom_horario
        return "-"


class LlamadaSerializer(serializers.ModelSerializer):
    cliente_data = serializers.SerializerMethodField()

    class Meta:
        model = Llamada
        fields = [
            "id",
            "numero",
            "cliente",
            "fecha_llamada",
            "hora_llamada",
            "callerid_name",
            "estado_llamada",
            "cerrar_llamada",
            "marca_tiempo_ami",
            "cliente_data",
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
