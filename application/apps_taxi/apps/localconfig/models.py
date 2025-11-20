from django.db import models

from apps.common.models import AuditableModel, TimeStampedModel


class EnvironmentVariable(AuditableModel, TimeStampedModel):
    name = models.SlugField("nombre de la variable", max_length=60, unique=True)
    value = models.CharField("valor de la variable", max_length=255)
    es_activo = models.BooleanField("Activo", default=False)

    class Meta:
        verbose_name = "variable de entorno"
        verbose_name_plural = "variables de entorno"

    def __str__(self):
        return self.name

    @classmethod
    def get_variable(cls, variable_name, defaul_value=None):
        try:
            return cls.objects.get(name=variable_name, es_activo=True).value
        except cls.DoesNotExist:
            if defaul_value:
                return defaul_value
            raise cls.DoesNotExist
