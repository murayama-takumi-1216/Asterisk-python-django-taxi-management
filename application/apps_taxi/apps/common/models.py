import uuid

from django.db import models


class AuditableModel(models.Model):
    created_by = models.CharField(
        "creado por",
        max_length=20,
        editable=False,
    )
    modified_by = models.CharField(
        "modificado por",
        max_length=20,
        editable=False,
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        "fecha de creación",
        auto_now_add=True,
        editable=False,
    )
    modified = models.DateTimeField(
        "fecha de modificación",
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True
