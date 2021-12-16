from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Permission to only allow admins to edit.
    """

    def has_permission(self, request, view):
        # we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # user must be admin
        return getattr(request.user, "is_admin", False)
