from django.contrib import admin

from apps.localconfig.models import EnvironmentVariable


@admin.register(EnvironmentVariable)
class EnvironmentVariableAdmin(admin.ModelAdmin):
    """
    Modelo de administración de variables de entorno
    """

    list_display = (
        "name",
        "value",
        "created_by",
        "created",
        "modified_by",
        "modified",
    )
    search_fields = (
        "name",
        "value",
        "created_by",
        "modified_by",
    )

    list_per_page = 25

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user.username
        else:
            obj.created_by = obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)
