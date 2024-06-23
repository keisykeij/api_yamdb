from rest_framework import permissions
from rest_framework.request import Request

from users.models import ROLES


class IsAppAdmin(permissions.BasePermission):
    """Доступ только пользователя с ролью "admin"."""
    def has_permission(self, request: Request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role == ROLES.admin.value
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request: Request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user == obj.author
            or request.user.role in (
                ROLES.moderator.value, ROLES.admin.value
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == ROLES.admin.value
        )

    def has_object_permission(self, request, view, obj):
        return request.user.role == ROLES.admin.value
