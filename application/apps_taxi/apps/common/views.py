import logging

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from django.views.generic.base import ContextMixin

from apps.common.authentication import BaseSessionAuthenticationApiView
from apps.common.permissions import (
    BasePermissionApiView,
    PermissionAdministradorApiView,
    PermissionOperadorApiView,
)
from apps.common.utils import DataLoginTurnoOperador

logger = logging.getLogger(__name__)


class BaseProtectedAppView(LoginRequiredMixin, ContextMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.login_url = reverse("core_apps:login")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BaseProtectedApiView(AccessMixin, View):
    authentication_classes = [BaseSessionAuthenticationApiView]
    permission_classes = [BasePermissionApiView]


class ProtectedOperadorApiView(BaseProtectedApiView):
    permission_classes = [PermissionOperadorApiView]

    def get_login_turno_operador(self) -> DataLoginTurnoOperador:
        return DataLoginTurnoOperador(self.request)


class ProtectedAdministradorApiView(BaseProtectedApiView):
    permission_classes = [PermissionAdministradorApiView]


class LoadPageView(BaseProtectedAppView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        if request.user.has_permiso_administrador():
            return redirect(reverse("core_apps:dashboard"))
        elif request.user.has_permiso_operador():
            return redirect(reverse("core_apps:process"))
        return redirect(reverse("core_apps:initial_page"))
