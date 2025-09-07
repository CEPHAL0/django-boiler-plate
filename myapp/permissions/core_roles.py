from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from myapp.enums.role_names import RoleNameEnum


class IsSuperAdmin(BasePermission):
    message = "User is not Super Admin"

    def has_permission(self, request, view):
        return request.user.is_superuser