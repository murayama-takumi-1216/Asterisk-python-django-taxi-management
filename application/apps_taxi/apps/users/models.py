from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.common.constants import (
    ROL_ADMINISTRADOR,
    ROL_ADMINOPERADOR,
    ROL_ADMINTAXI,
    ROL_OPERADOR,
    ROL_ROOT,
    ROL_TAXISTA,
)


class User(AbstractUser):
    """
    Default custom user model for apps.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_groups_set(self) -> {str}:
        return {name for name in self.groups.values_list("name", flat=True)}

    def has_permiso_operador(self):
        return True if ROL_OPERADOR in self.get_groups_set() else False

    def has_permiso_taxi(self):
        return True if ROL_TAXISTA in self.get_groups_set() else False

    def has_permiso_admin_operador(self):
        permitidos = {ROL_ADMINOPERADOR, ROL_ADMINISTRADOR, ROL_ROOT}
        setting = self.get_groups_set()
        return (
            True
            if len(setting) > 0 and len(permitidos - setting) < len(permitidos)
            else False
        )

    def has_permiso_admin_taxi(self):
        permitidos = {ROL_ADMINTAXI, ROL_ADMINISTRADOR, ROL_ROOT}
        setting = self.get_groups_set()
        return (
            True
            if len(setting) > 0 and len(permitidos - setting) < len(permitidos)
            else False
        )

    def has_permiso_administrador(self):
        permitidos = {ROL_ADMINISTRADOR, ROL_ROOT}
        setting = self.get_groups_set()
        return (
            True
            if len(setting) > 0 and len(permitidos - setting) < len(permitidos)
            else False
        )
