from rest_framework.permissions import BasePermission


class IsLoggedIn(BasePermission):
    """
    Allows access to only logged in users
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_author or request.user.is_superuser
        )
