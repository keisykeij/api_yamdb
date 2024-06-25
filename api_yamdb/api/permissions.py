from rest_framework import permissions
from rest_framework.request import Request

from users.models import ROLES


class IsAppAdmin(permissions.BasePermission):
    """Доступ только пользователя с ролью "admin"."""
    def has_permission(self, request: Request, view):
        return (
            request.user.is_authenticated
            and request.user.role == ROLES.admin.value
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Доступ к внесению изменений от пользователей с ролями:
     "Author", "Moderator", "Admin", иначе только чтение."""

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
    """
    Правило позволяет доступ только для чтения (GET, HEAD, OPTIONS)
    для неавторизованных пользователей,
    а также для авторизованных пользователей,
    которые имеют роль администратора.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.role == ROLES.admin.value
            )
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
