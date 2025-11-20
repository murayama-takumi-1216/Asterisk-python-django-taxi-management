from django.contrib import admin
from django.db.models import Exists, OuterRef

from apps.core_maestras.models import GrupoHorarioDetalle
from apps.core_operador.models import (
    CatHorarioOperardor,
    CatHorarioOperardorDetalle,
    Operador,
)


@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "nombre",
        "apellido_paterno",
        "dat_audit",
        "dat_user",
        "estado",
    ]
    ordering = ["codigo", "nombre"]
    search_fields = ["codigo", "nombre"]
    list_filter = ["estado"]
    readonly_fields = ["codigo"]

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

    def dat_user(self, obj):
        if obj.user:
            return obj.user
        return "-"

    dat_user.short_description = "Usuario/Sistema"


class CatHorarioOperardorDetalleItemInline(admin.TabularInline):
    model = CatHorarioOperardorDetalle
    raw_id_fields = ["cat_horario"]
    readonly_fields = [field.name for field in CatHorarioOperardorDetalle._meta.fields]


@admin.register(CatHorarioOperardor)
class CatHorarioOperardorAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "cat_horario",
        "dat_fecha_inicio",
        "dat_fecha_fin",
        "dat_audit",
        "activo",
    ]
    ordering = ["-codigo"]
    search_fields = ["codigo"]
    list_filter = ["activo"]
    readonly_fields = ["codigo"]

    list_per_page = 25
    inlines = [CatHorarioOperardorDetalleItemInline]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user.username
        else:
            obj.created_by = obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)

    def dat_fecha_inicio(self, obj):
        if obj.fecha_inicio:
            return obj.fecha_inicio.strftime("%Y-%m-%d")
        return "-"

    dat_fecha_inicio.short_description = "fecha inicio"

    def dat_fecha_fin(self, obj):
        if obj.fecha_fin:
            return obj.fecha_fin.strftime("%Y-%m-%d")
        return "-"

    dat_fecha_fin.short_description = "fecha fin"

    def dat_audit(self, obj):
        modificacion = ""
        if obj.modified:
            modificacion = obj.modified.strftime("%Y-%m-%dH%H:%M")
        return "{} ({})".format(obj.modified_by, modificacion)


@admin.register(CatHorarioOperardorDetalle)
class CatHorarioOperardorDetalleAdmin(admin.ModelAdmin):
    list_display = [
        "grupo_horario_detalle",
        "cat_horario",
        "operador",
        "dat_fecha_inicio",
        "dat_fecha_fin",
        "dat_audit",
        "confirmado",
        "activo",
    ]
    ordering = ["cat_horario", "grupo_horario_detalle"]
    list_filter = ["activo", "confirmado"]

    list_per_page = 25

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "grupo_horario_detalle":
            exist_subquery = CatHorarioOperardorDetalle.objects.filter(
                activo=True, grupo_horario_detalle_id=OuterRef("id")
            )
            kwargs["queryset"] = GrupoHorarioDetalle.objects.filter(
                ~Exists(exist_subquery)
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user.username
        else:
            obj.created_by = obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)

    def dat_fecha_inicio(self, obj):
        if obj.fecha_inicio:
            return obj.fecha_inicio.strftime("%Y-%m-%d")
        return "-"

    dat_fecha_inicio.short_description = "fecha inicio"

    def dat_fecha_fin(self, obj):
        if obj.fecha_fin:
            return obj.fecha_fin.strftime("%Y-%m-%d")
        return "-"

    dat_fecha_fin.short_description = "fecha fin"

    def dat_audit(self, obj):
        modificacion = ""
        if obj.modified:
            modificacion = obj.modified.strftime("%Y-%m-%dH%H:%M")
        return "{} ({})".format(obj.modified_by, modificacion)
