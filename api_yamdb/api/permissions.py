from rest_framework import permissions


class IsAuthorOrStuffOrReadOnly(permissions.BasePermission):
    # TODO уточнить обращение к пользователю
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.IsAuthenticated
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                )
