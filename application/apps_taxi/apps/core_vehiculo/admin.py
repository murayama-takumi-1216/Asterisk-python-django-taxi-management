from django.contrib import admin

from apps.core_vehiculo.models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = [
        "cod_vehiculo",
        "nom_vehiculo",
        "dat_audit",
        "estado_vehiculo",
    ]
    ordering = ["cod_vehiculo", "nom_vehiculo"]
    search_fields = ["cod_vehiculo", "nom_vehiculo"]
    list_filter = ["estado_vehiculo"]
    readonly_fields = ["cod_vehiculo"]

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
