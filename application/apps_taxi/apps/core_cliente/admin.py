from django.contrib import admin

from apps.core_cliente.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "servicios_realizados",
        "servicios_pendiente",
        "dat_audit",
        "estado",
    ]
    ordering = ["codigo", "nombre"]
    search_fields = ["codigo", "nombre"]
    list_filter = ["estado"]
    readonly_fields = ["codigo"]

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
