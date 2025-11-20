from django.contrib import admin

from apps.core_servicio.models import Llamada, Servicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = [
        "operador_registra",
        "turno_conductor",
        "cliente",
        "dat_programacion",
        "fecha_hora_inicio",
        "fecha_hora_fin",
        "horas_efectivas",
        "monto_servicio",
        "dat_audit",
        "estado",
        "eliminado",
    ]
    ordering = ["-id", "-programado_fecha_hora_inicio"]
    readonly_fields = ["horas_efectivas", "dat_audit", "dat_programacion"]
    search_fields = ["programado_fecha_hora_inicio"]
    list_filter = ["estado", "eliminado"]

    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user.username
        else:
            obj.created_by = obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)

    def dat_audit(self, obj):
        modificacion = ""
        if obj.modified:
            modificacion = obj.modified.strftime("%Y-%m-%dH%H:%M")
        return "{} ({})".format(obj.modified_by, modificacion)

    dat_audit.short_description = "Modificación"

    def dat_programacion(self, obj):
        fecha = ""
        if obj.fecha_programacion:
            fecha = obj.programado_fecha_hora_inicio.strftime("%d/%m/%y")
        hora = ""
        if obj.hora_programacion:
            hora = obj.programado_fecha_hora_inicio.strftime("%H:%M")
        return "{} {}".format(fecha, hora)

    dat_programacion.short_description = "Programación"


@admin.register(Llamada)
class LlamadaAdmin(admin.ModelAdmin):
    list_display = [
        "cliente",
        "numero",
        "operador_contesta",
        "fecha_llamada",
        "hora_llamada",
        "fecha_hora_llamada",
        "dat_audit",
        "eliminado",
        "estado_llamada",
    ]
    ordering = ["-id", "-fecha_hora_llamada"]
    search_fields = ["fecha_hora_llamada"]
    list_filter = ["estado_llamada", "eliminado"]

    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user.username
        else:
            obj.created_by = obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)

    def dat_audit(self, obj):
        modificacion = ""
        if obj.modified:
            modificacion = obj.modified.strftime("%Y-%m-%dH%H:%M")
        return "{} ({})".format(obj.modified_by, modificacion)

    dat_audit.short_description = "Modificación"
