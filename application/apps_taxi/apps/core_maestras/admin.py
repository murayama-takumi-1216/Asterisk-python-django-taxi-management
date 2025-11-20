from django.contrib import admin

from apps.core_maestras.models import GrupoHorario, GrupoHorarioDetalle, Horario


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = [
        "cod_horario",
        "nom_horario",
        "dat_rango",
        "dat_audit",
        "horario_base",
        "estado",
    ]
    ordering = ["cod_horario", "nom_horario"]
    search_fields = ["cod_horario", "nom_horario"]
    list_filter = ["estado"]

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

    def dat_rango(self, obj):
        inicio = "..."
        if obj.inicio_horario:
            inicio = obj.inicio_horario.strftime("%H:%M")
        fin = "..."
        if obj.fin_horario:
            fin = obj.fin_horario.strftime("%H:%M")
        return "[ {} - {} >".format(inicio, fin)

    dat_rango.short_description = "[Inicio - Fin>"


@admin.register(GrupoHorario)
class GrupoHorarioAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "nombre",
        "dat_audit",
        "confirmado",
        "estado",
    ]
    ordering = ["-codigo"]
    search_fields = ["codigo", "nombre"]
    list_filter = ["estado", "confirmado"]
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


@admin.register(GrupoHorarioDetalle)
class GrupoHorarioDetalleAdmin(admin.ModelAdmin):
    list_display = [
        "grupo_horario",
        "dia_semana",
        "horario",
        "orden_view",
        "dat_audit",
        "confirmado",
        "estado",
    ]
    ordering = ["-grupo_horario", "orden_view"]
    list_filter = ["estado", "confirmado", "dia_semana"]

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
