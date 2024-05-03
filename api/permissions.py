from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Пользовательское разрешение - разрешать только автору."""

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return ((request.method in permissions.SAFE_METHODS)
                    or (obj.user == request.user))
        elif hasattr(obj, 'author'):
            return ((request.method in permissions.SAFE_METHODS)
                    or (obj.author == request.user))
        return False
