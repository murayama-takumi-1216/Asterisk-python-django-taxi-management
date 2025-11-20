from django.contrib import admin

from apps.core_conductor.models import Conductor


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = [
        "cod_conductor",
        "nombre",
        "apellido_paterno",
        "dat_audit",
        "estado",
    ]
    ordering = ["cod_conductor", "nombre", "apellido_paterno"]
    search_fields = ["cod_conductor", "nombre", "apellido_paterno"]
    list_filter = ["estado"]
    readonly_fields = ["cod_conductor"]

    list_per_page = 25

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
