from rest_framework.permissions import BasePermission

from accounts.models import UserRole


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == UserRole.ADMIN


class SalesPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == UserRole.SALES
