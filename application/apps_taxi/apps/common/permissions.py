from rest_framework.permissions import BasePermission


class BasePermissionApiView(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return True


class PermissionOperadorApiView(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.has_permiso_operador())

    def has_object_permission(self, request, view, obj):
        return True


class PermissionAdministradorApiView(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.has_permiso_administrador())

    def has_object_permission(self, request, view, obj):
        return True
