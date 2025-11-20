from django.contrib import admin

from apps.core_turno.models import TurnoConductor


@admin.register(TurnoConductor)
class TurnoConductorAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "programado_fecha_hora_inicio",
        "fecha_hora_inicio",
        "fecha_hora_fin",
        "horas_efectivas",
        "monto_generado",
        "dat_audit",
        "estado_turno",
    ]
    ordering = ["programado_fecha_hora_inicio"]
    readonly_fields = ["horas_efectivas"]
    search_fields = ["programado_fecha_hora_inicio"]
    list_filter = ["estado_turno"]

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
