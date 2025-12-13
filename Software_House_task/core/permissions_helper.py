from rest_framework.permissions import SAFE_METHODS, BasePermission

from accounts.models import UserRole


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == UserRole.ADMIN


class SalesPermission(BasePermission):
    message = "Sales users only."

    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role == UserRole.SALES)


class SalesReadOnly(SalesPermission):

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if request.user.role == UserRole.SALES:
            return request.method in SAFE_METHODS
        return True


class SalesCreateAndReadOnlyPermission(BasePermission):
    accepted_methods = SAFE_METHODS + ('POST',)

    def has_permission(self, request, view):
        if request.user.role == UserRole.SALES:
            return request.method in self.accepted_methods
        return False
